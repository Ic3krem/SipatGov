from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db, LGU, Project, BrokenPromiseReport, DashboardSummary, CrawlLog
from pydantic import BaseModel
from datetime import datetime
import logging
from services.crawl_service import CrawlService

logger = logging.getLogger(__name__)

router = APIRouter()

# Pydantic Models for Response
class LGUResponse(BaseModel):
    id: int
    name: str
    url: str
    contact_info: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    budget: float
    status: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    source_url: str
    
    class Config:
        from_attributes = True

class ReportResponse(BaseModel):
    id: int
    promise: str
    status: str
    severity: str
    anomaly_score: float
    created_at: datetime
    
    class Config:
        from_attributes = True

class DashboardSummaryResponse(BaseModel):
    total_lgus: int
    total_projects: int
    total_budget: float
    fulfilled_promises: int
    broken_promises: int
    delayed_promises: int
    average_anomaly_score: float
    last_updated: datetime
    
    class Config:
        from_attributes = True

# Routes

@router.get("/health", tags=["Status"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "message": "SipatGov Backend API is running"
    }

@router.get("/lgus", response_model=List[LGUResponse], tags=["LGUs"])
async def get_lgus(db: Session = Depends(get_db)):
    """Get list of all LGUs"""
    try:
        lgus = db.query(LGU).all()
        return lgus
    except Exception as e:
        logger.error(f"Error fetching LGUs: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching LGUs")

@router.get("/lgus/{lgu_id}", response_model=LGUResponse, tags=["LGUs"])
async def get_lgu(lgu_id: int, db: Session = Depends(get_db)):
    """Get specific LGU by ID"""
    try:
        lgu = db.query(LGU).filter(LGU.id == lgu_id).first()
        if not lgu:
            raise HTTPException(status_code=404, detail="LGU not found")
        return lgu
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching LGU {lgu_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching LGU")

@router.get("/projects", response_model=List[ProjectResponse], tags=["Projects"])
async def get_projects(
    lgu_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get projects, optionally filtered by LGU or status"""
    try:
        query = db.query(Project)
        
        if lgu_id:
            query = query.filter(Project.lgu_id == lgu_id)
        if status:
            query = query.filter(Project.status == status)
        
        projects = query.all()
        return projects
    except Exception as e:
        logger.error(f"Error fetching projects: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching projects")

@router.get("/projects/{project_id}", response_model=ProjectResponse, tags=["Projects"])
async def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get specific project by ID"""
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching project {project_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching project")

@router.get("/reports", response_model=List[ReportResponse], tags=["Reports"])
async def get_reports(
    lgu_id: Optional[int] = Query(None),
    severity: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get broken promise reports, optionally filtered"""
    try:
        query = db.query(BrokenPromiseReport)
        
        if lgu_id:
            query = query.filter(BrokenPromiseReport.lgu_id == lgu_id)
        if severity:
            query = query.filter(BrokenPromiseReport.severity == severity)
        
        reports = query.all()
        return reports
    except Exception as e:
        logger.error(f"Error fetching reports: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching reports")

@router.get("/reports/{report_id}", response_model=ReportResponse, tags=["Reports"])
async def get_report(report_id: int, db: Session = Depends(get_db)):
    """Get specific report by ID"""
    try:
        report = db.query(BrokenPromiseReport).filter(BrokenPromiseReport.id == report_id).first()
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        return report
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching report {report_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching report")

@router.get("/dashboard-summary", response_model=DashboardSummaryResponse, tags=["Dashboard"])
async def get_dashboard_summary(db: Session = Depends(get_db)):
    """Get aggregated dashboard statistics"""
    try:
        # Calculate from database
        total_lgus = db.query(LGU).count()
        total_projects = db.query(Project).count()
        total_budget = db.query(Project).with_entities(db.func.sum(Project.budget)).scalar() or 0.0
        
        fulfilled = db.query(BrokenPromiseReport).filter(BrokenPromiseReport.status == "fulfilled").count()
        broken = db.query(BrokenPromiseReport).filter(BrokenPromiseReport.status == "broken").count()
        delayed = db.query(BrokenPromiseReport).filter(BrokenPromiseReport.status == "delayed").count()
        
        avg_anomaly = db.query(db.func.avg(BrokenPromiseReport.anomaly_score)).scalar() or 0.0
        
        # Get or create summary
        summary = db.query(DashboardSummary).first()
        if not summary:
            summary = DashboardSummary(
                total_lgus=total_lgus,
                total_projects=total_projects,
                total_budget=float(total_budget),
                fulfilled_promises=fulfilled,
                broken_promises=broken,
                delayed_promises=delayed,
                average_anomaly_score=float(avg_anomaly)
            )
            db.add(summary)
            db.commit()
        else:
            summary.total_lgus = total_lgus
            summary.total_projects = total_projects
            summary.total_budget = float(total_budget)
            summary.fulfilled_promises = fulfilled
            summary.broken_promises = broken
            summary.delayed_promises = delayed
            summary.average_anomaly_score = float(avg_anomaly)
            db.commit()
        
        return summary
    except Exception as e:
        logger.error(f"Error fetching dashboard summary: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching dashboard summary")

@router.get("/crawl-logs", tags=["Monitoring"])
async def get_crawl_logs(
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get crawling logs"""
    try:
        query = db.query(CrawlLog)
        
        if status:
            query = query.filter(CrawlLog.status == status)
        
        logs = query.order_by(CrawlLog.started_at.desc()).limit(100).all()
        
        return [
            {
                'id': log.id,
                'source': log.source,
                'status': log.status,
                'urls_processed': log.urls_processed,
                'items_found': log.items_found,
                'started_at': log.started_at,
                'completed_at': log.completed_at,
                'error_message': log.error_message
            }
            for log in logs
        ]
    except Exception as e:
        logger.error(f"Error fetching crawl logs: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching crawl logs")

@router.post("/crawl", tags=["Admin"])
async def trigger_crawl(
    lgu_id: Optional[int] = None,
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """Trigger a crawl operation for one or all LGUs"""
    try:
        if lgu_id:
            # Crawl specific LGU
            result = await CrawlService.crawl_lgu_website(lgu_id, db)
            if result["status"] == "success":
                return {
                    "status": "crawl_completed",
                    "log_id": result.get("log_id"),
                    "message": result.get("message"),
                    "items_found": result.get("items_found", 0)
                }
            else:
                raise HTTPException(status_code=400, detail=result.get("message"))
        else:
            # Crawl all LGUs - run in background
            result = await CrawlService.crawl_all_lgus(db)
            return {
                "status": result.get("status"),
                "message": result.get("message"),
                "lgus_crawled": result.get("lgus_crawled", 0),
                "total_items_found": result.get("total_items_found", 0)
            }
    except Exception as e:
        logger.error(f"Error triggering crawl: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error triggering crawl: {str(e)}")
