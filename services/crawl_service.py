import asyncio
import logging
from typing import Optional, List
from datetime import datetime
import aiohttp
from sqlalchemy.orm import Session
from database import LGU, Project, CrawlLog
from config import CRAWL_TIMEOUT, CRAWL_RETRY_ATTEMPTS, MAX_URLS_PER_LGU
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

logger = logging.getLogger(__name__)

class CrawlService:
    """Service for crawling government websites and extracting project data"""
    
    @staticmethod
    async def crawl_lgu_website(lgu_id: int, db: Session) -> dict:
        """Crawl a specific LGU website"""
        try:
            lgu = db.query(LGU).filter(LGU.id == lgu_id).first()
            if not lgu:
                return {"status": "failed", "message": "LGU not found"}
            
            # Create crawl log
            log = CrawlLog(
                lgu_id=lgu_id,
                source=f"lgu_website: {lgu.url}",
                status="running",
                urls_processed=0,
                items_found=0,
                started_at=datetime.utcnow()
            )
            db.add(log)
            db.commit()
            
            # Perform crawl and get extracted projects
            result = await CrawlService._fetch_and_parse_lgu(lgu)
            
            # Save extracted projects to database
            if result.get("projects"):
                for project_data in result["projects"]:
                    # Check if project already exists
                    existing = db.query(Project).filter(
                        Project.lgu_id == lgu_id,
                        Project.name == project_data["name"]
                    ).first()
                    
                    if not existing:
                        project = Project(
                            lgu_id=lgu_id,
                            name=project_data.get("name", "Unknown Project"),
                            description=project_data.get("description", ""),
                            budget=project_data.get("budget", 0.0),
                            status=project_data.get("status", "ongoing"),
                            start_date=datetime.utcnow(),
                            end_date=None,
                            source_url=lgu.url,
                            promises=project_data.get("promises", {}),
                            accomplishments=project_data.get("accomplishments", {})
                        )
                        db.add(project)
                
                db.commit()
            
            # Update crawl log
            log.status = "completed" if result["success"] else "failed"
            log.urls_processed = result["urls_processed"]
            log.items_found = result["items_found"]
            log.completed_at = datetime.utcnow()
            
            if not result["success"]:
                log.error_message = result.get("error", "Unknown error")
            
            db.commit()
            
            return {
                "status": "success",
                "log_id": log.id,
                "urls_processed": result["urls_processed"],
                "items_found": result["items_found"],
                "message": f"Crawled {result['items_found']} projects from {lgu.name}"
            }
        
        except Exception as e:
            logger.error(f"Error crawling LGU {lgu_id}: {str(e)}")
            return {"status": "failed", "message": str(e)}
    
    @staticmethod
    async def _fetch_and_parse_lgu(lgu: LGU) -> dict:
        """Fetch and parse LGU website using Selenium for JavaScript rendering"""
        result = {
            "success": False,
            "urls_processed": 0,
            "items_found": 0,
            "projects": [],
            "error": None
        }
        
        driver = None
        try:
            # Setup Chrome options
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Run in background
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            
            # Initialize WebDriver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Try main URL
            html = await CrawlService._fetch_with_selenium(driver, lgu.url)
            if html:
                result["urls_processed"] += 1
                projects = CrawlService._parse_projects_from_html(html)
                result["items_found"] += len(projects)
                result["projects"] = projects
                result["success"] = True
                logger.info(f"Successfully crawled {lgu.name}: found {len(projects)} projects")
                return result
            
            # Try common project/budget paths
            common_paths = [
                "/projects",
                "/programs",
                "/budget",
                "/about/projects",
                "/services/projects",
                "/news",
                "/announcements"
            ]
            
            for path in common_paths:
                test_url = lgu.url.rstrip('/') + path
                html = await CrawlService._fetch_with_selenium(driver, test_url)
                if html:
                    result["urls_processed"] += 1
                    projects = CrawlService._parse_projects_from_html(html)
                    result["items_found"] += len(projects)
                    if projects:
                        result["projects"] = projects
                        result["success"] = True
                        logger.info(f"Found {len(projects)} projects on {path}")
                        return result
            
            result["success"] = result["urls_processed"] > 0
            if not result["success"]:
                result["error"] = "Could not fetch content from any URLs"
        
        except Exception as e:
            result["error"] = str(e)
            logger.error(f"Error fetching LGU {lgu.name} with Selenium: {str(e)}")
        
        finally:
            if driver:
                driver.quit()
        
        return result
    
    @staticmethod
    async def _fetch_with_selenium(driver, url: str) -> Optional[str]:
        """Fetch URL using Selenium with JavaScript rendering"""
        try:
            logger.info(f"Fetching with Selenium: {url}")
            driver.get(url)
            
            # Wait for page to load (up to 10 seconds)
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "body"))
                )
            except:
                logger.warning(f"Timeout waiting for {url} to load")
            
            # Wait for dynamic content
            time.sleep(2)
            
            # Get rendered HTML
            html = driver.page_source
            
            if html and len(html) > 100:  # Ensure we got meaningful content
                logger.info(f"Successfully fetched {len(html)} bytes from {url}")
                return html
            else:
                logger.warning(f"Got empty or minimal content from {url}")
                return None
        
        except Exception as e:
            logger.warning(f"Selenium error fetching {url}: {str(e)}")
            return None
    
    @staticmethod
    def _parse_projects_from_html(html: str) -> List[dict]:
        """Parse project information from HTML"""
        projects = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Look for common project indicators in multiple patterns
            project_indicators = [
                'project', 'program', 'infrastructure', 'development',
                'initiative', 'activity', 'service', 'facility'
            ]
            
            # Strategy 1: Look for elements with project/program classes or ids
            project_elements = soup.find_all(
                ['div', 'article', 'section', 'li'],
                class_=lambda x: x and any(ind in x.lower() for ind in project_indicators)
            )
            
            # Strategy 2: Look for heading+description combinations
            for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                text = heading.get_text(strip=True)
                if len(text) > 5 and len(text) < 200:
                    parent = heading.parent
                    if parent:
                        project_elements.append(parent)
            
            # Extract projects from elements
            seen_titles = set()
            for element in project_elements[:MAX_URLS_PER_LGU]:
                try:
                    project = {
                        'name': '',
                        'description': '',
                        'status': 'ongoing',
                        'budget': 0.0,
                        'source_url': '',
                    }
                    
                    # Extract name - prefer heading or first text
                    title_elem = element.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                    if title_elem:
                        project['name'] = title_elem.get_text(strip=True)[:100]
                    else:
                        text = element.get_text(strip=True)[:100]
                        if text:
                            project['name'] = text
                    
                    # Skip if we've seen this name
                    if project['name'] in seen_titles or not project['name']:
                        continue
                    
                    seen_titles.add(project['name'])
                    
                    # Extract description - get longer text
                    desc_parts = []
                    for p in element.find_all(['p', 'span', 'div']):
                        text = p.get_text(strip=True)
                        if text and len(text) > 10:
                            desc_parts.append(text)
                    
                    project['description'] = ' '.join(desc_parts)[:500]
                    
                    # Determine status from text indicators
                    full_text = element.get_text().lower()
                    if 'completed' in full_text or 'done' in full_text or 'finished' in full_text:
                        project['status'] = 'completed'
                    elif 'ongoing' in full_text or 'in progress' in full_text or 'implementation' in full_text:
                        project['status'] = 'ongoing'
                    elif 'planned' in full_text or 'upcoming' in full_text or 'proposed' in full_text:
                        project['status'] = 'planned'
                    
                    # Look for budget info - extract numbers
                    import re
                    budget_pattern = r'[₱P]*\s*([0-9,]+(?:\.[0-9]{2})?)'
                    budget_match = re.search(budget_pattern, element.get_text())
                    if budget_match:
                        try:
                            budget_str = budget_match.group(1).replace(',', '')
                            project['budget'] = float(budget_str)
                        except:
                            pass
                    
                    if project['name']:  # Only add if there's a name
                        projects.append(project)
                
                except Exception as e:
                    logger.debug(f"Error parsing individual project element: {str(e)}")
                    continue
            
            # If no projects found, try a more generic approach
            if not projects:
                text_elements = soup.find_all(['p', 'li'], limit=10)
                for elem in text_elements:
                    text = elem.get_text(strip=True)
                    if len(text) > 20 and len(text) < 500:
                        projects.append({
                            'name': f"Content from {elem.name}",
                            'description': text,
                            'status': 'ongoing',
                            'budget': 0.0,
                            'source_url': ''
                        })
        
        except Exception as e:
            logger.error(f"Error parsing HTML for projects: {str(e)}")
        
        return projects
    
    @staticmethod
    async def crawl_all_lgus(db: Session) -> dict:
        """Crawl all LGUs"""
        try:
            lgus = db.query(LGU).all()
            
            if not lgus:
                return {"status": "failed", "message": "No LGUs found"}
            
            results = []
            for lgu in lgus:
                result = await CrawlService.crawl_lgu_website(lgu.id, db)
                results.append(result)
            
            total_items = sum(r.get("items_found", 0) for r in results)
            successful = sum(1 for r in results if r.get("status") == "success")
            
            return {
                "status": "completed",
                "lgus_crawled": successful,
                "total_items_found": total_items,
                "results": results,
                "message": f"Crawled {successful} LGUs, found {total_items} total items"
            }
        
        except Exception as e:
            logger.error(f"Error in batch crawl: {str(e)}")
            return {"status": "failed", "message": str(e)}
