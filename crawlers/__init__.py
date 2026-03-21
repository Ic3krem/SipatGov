import os
import requests
import logging
from typing import List, Dict
from datetime import datetime
import json
import aiohttp
import asyncio
from config import (
    CRAWL_TIMEOUT, CRAWL_RETRY_ATTEMPTS, 
    MAX_URLS_PER_LGU, DOWNLOAD_DIR, 
    PHILGEPS_API, COA_API, DATA_GOV_PH_API
)

logger = logging.getLogger(__name__)

class GovernmentDataCrawler:
    """Base crawler for government portals"""
    
    def __init__(self):
        self.session = None
        self.download_dir = DOWNLOAD_DIR
        os.makedirs(self.download_dir, exist_ok=True)
    
    async def fetch_url(self, url: str, timeout: int = 30) -> dict:
        """Fetch a URL with retry logic"""
        for attempt in range(CRAWL_RETRY_ATTEMPTS):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, timeout=timeout) as response:
                        if response.status == 200:
                            content_type = response.headers.get('content-type', '')
                            if 'application/pdf' in content_type or 'image' in content_type:
                                data = await response.read()
                                return {
                                    'status': 'success',
                                    'data': data,
                                    'content_type': content_type,
                                    'url': url
                                }
                            elif 'json' in content_type:
                                data = await response.json()
                                return {
                                    'status': 'success',
                                    'data': data,
                                    'content_type': content_type,
                                    'url': url
                                }
                            else:
                                text = await response.text()
                                return {
                                    'status': 'success',
                                    'data': text,
                                    'content_type': content_type,
                                    'url': url
                                }
                        else:
                            logger.warning(f"URL fetch failed: {url} (status: {response.status})")
            except asyncio.TimeoutError:
                logger.warning(f"Timeout on {url}, attempt {attempt + 1}")
            except Exception as e:
                logger.error(f"Error fetching {url}: {str(e)}")
            
            if attempt < CRAWL_RETRY_ATTEMPTS - 1:
                await asyncio.sleep(2 ** attempt)
        
        return {'status': 'failed', 'url': url, 'error': 'Max retries exceeded'}
    
    async def download_file(self, url: str, filename: str = None) -> str:
        """Download and save a file"""
        result = await self.fetch_url(url)
        if result['status'] == 'success':
            if filename is None:
                filename = url.split('/')[-1][:50] + '_' + str(datetime.now().timestamp()).split('.')[0]
            
            filepath = os.path.join(self.download_dir, filename)
            
            if isinstance(result['data'], bytes):
                with open(filepath, 'wb') as f:
                    f.write(result['data'])
            else:
                with open(filepath, 'w') as f:
                    f.write(str(result['data']))
            
            logger.info(f"Downloaded: {filepath}")
            return filepath
        
        return None

class PhilGEPSCrawler(GovernmentDataCrawler):
    """Crawler for PhilGEPS (Philippine Government Electronic Procurement System)"""
    
    async def crawl_procurements(self, query: str = "supplies") -> List[Dict]:
        """Crawl procurement data"""
        results = []
        try:
            # Example: PhilGEPS API call
            url = f"{PHILGEPS_API}/procurements?search={query}"
            result = await self.fetch_url(url)
            
            if result['status'] == 'success':
                # Parse and structure the data
                data = result['data']
                if isinstance(data, str):
                    data = json.loads(data)
                
                results = self._parse_procurements(data)
                logger.info(f"Crawled {len(results)} procurements from PhilGEPS")
        except Exception as e:
            logger.error(f"Error crawling PhilGEPS: {str(e)}")
        
        return results[:MAX_URLS_PER_LGU]
    
    def _parse_procurements(self, data: dict) -> List[Dict]:
        """Parse procurement data"""
        procurements = []
        try:
            items = data.get('results', data.get('data', []))
            if isinstance(items, list):
                for item in items[:MAX_URLS_PER_LGU]:
                    procurements.append({
                        'title': item.get('title', ''),
                        'description': item.get('description', ''),
                        'budget': item.get('amount', 0),
                        'status': item.get('status', ''),
                        'date': item.get('date', ''),
                        'source': 'philgeps',
                        'url': item.get('url', '')
                    })
        except Exception as e:
            logger.error(f"Error parsing procurements: {str(e)}")
        
        return procurements

class COACrawler(GovernmentDataCrawler):
    """Crawler for COA (Commission on Audit) Reports"""
    
    async def crawl_audit_reports(self, entity: str = None) -> List[Dict]:
        """Crawl audit reports"""
        results = []
        try:
            url = f"{COA_API}/audit_reports"
            if entity:
                url += f"?entity={entity}"
            
            result = await self.fetch_url(url)
            
            if result['status'] == 'success':
                data = result['data']
                if isinstance(data, str):
                    data = json.loads(data)
                
                results = self._parse_reports(data)
                logger.info(f"Crawled {len(results)} audit reports from COA")
        except Exception as e:
            logger.error(f"Error crawling COA: {str(e)}")
        
        return results[:MAX_URLS_PER_LGU]
    
    def _parse_reports(self, data: dict) -> List[Dict]:
        """Parse audit report data"""
        reports = []
        try:
            items = data.get('results', data.get('data', []))
            if isinstance(items, list):
                for item in items[:MAX_URLS_PER_LGU]:
                    reports.append({
                        'title': item.get('title', ''),
                        'entity': item.get('entity', ''),
                        'audit_year': item.get('year', ''),
                        'findings': item.get('findings', []),
                        'source': 'coa',
                        'url': item.get('file_url', '')
                    })
        except Exception as e:
            logger.error(f"Error parsing audit reports: {str(e)}")
        
        return reports

class LGUWebsiteCrawler(GovernmentDataCrawler):
    """Generic crawler for LGU websites"""
    
    async def crawl_lgu_website(self, lgu_url: str, keywords: List[str] = None) -> List[Dict]:
        """Crawl LGU website for projects and documents"""
        if keywords is None:
            keywords = ['project', 'budget', 'budget allocation', 'procurement']
        
        results = []
        try:
            result = await self.fetch_url(lgu_url)
            
            if result['status'] == 'success':
                results = self._extract_links_and_data(result['data'], lgu_url)
                logger.info(f"Crawled LGU website: {lgu_url}, found {len(results)} items")
        except Exception as e:
            logger.error(f"Error crawling LGU website {lgu_url}: {str(e)}")
        
        return results[:MAX_URLS_PER_LGU]
    
    def _extract_links_and_data(self, html: str, base_url: str) -> List[Dict]:
        """Extract links and data from HTML"""
        from bs4 import BeautifulSoup
        
        results = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract PDFs
            for link in soup.find_all('a', href=True):
                href = link['href']
                if any(ext in href.lower() for ext in ['.pdf', '.xlsx', '.xls', '.csv']):
                    results.append({
                        'type': 'document',
                        'title': link.get_text()[:100],
                        'url': href,
                        'source': 'lgu_website'
                    })
            
            # Extract paragraphs with keywords
            for para in soup.find_all(['p', 'div']):
                text = para.get_text()
                if any(kw in text.lower() for kw in ['project', 'budget', 'allocation']):
                    results.append({
                        'type': 'text_content',
                        'content': text[:500],
                        'source': 'lgu_website'
                    })
        except Exception as e:
            logger.error(f"Error extracting links: {str(e)}")
        
        return results[:MAX_URLS_PER_LGU]
