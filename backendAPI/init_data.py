"""
Demo data initialization script for SipatGov Backend API
Populates the database with example LGUs, projects, and reports for testing
"""

import asyncio
from datetime import datetime, timedelta
from database import SessionLocal, LGU, Project, BrokenPromiseReport, DashboardSummary, init_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sample data
SAMPLE_LGUS = [
    {
        "name": "City of Manila",
        "url": "https://manila.gov.ph",
        "contact_info": "contact@manila.gov.ph",
        "budget_endpoint": "https://data.gov.ph/api/datasets/manila-budget"
    },
    {
        "name": "Municipality of Binan",
        "url": "https://binan.gov.ph",
        "contact_info": "info@binan.gov.ph",
        "budget_endpoint": "https://data.gov.ph/api/datasets/binan-budget"
    },
    {
        "name": "Province of Laguna",
        "url": "https://laguna.gov.ph",
        "contact_info": "contact@laguna.gov.ph",
        "budget_endpoint": "https://data.gov.ph/api/datasets/laguna-budget"
    }
]

SAMPLE_PROJECTS = [
    {
        "lgu_id": 1,
        "name": "Water Supply System Upgrade",
        "description": "Expansion of water distribution network to underserved areas",
        "budget": 50000000.0,
        "status": "ongoing",
        "start_date": datetime(2023, 6, 1),
        "end_date": datetime(2024, 12, 31),
        "promises": [
            "Complete Phase 1 by Q3 2024",
            "Serve 50,000 households",
            "Install smart meters in all connections"
        ],
        "accomplishments": [
            "Phase 1 partial completion 40%",
            "Served 20,000 households",
            "Smart meter installation incomplete"
        ],
        "source_url": "https://manila.gov.ph/projects/water-supply"
    },
    {
        "lgu_id": 1,
        "name": "Road Rehabilitation Program",
        "description": "Repair and asphalt overlay of municipal roads",
        "budget": 75000000.0,
        "status": "completed",
        "start_date": datetime(2023, 1, 15),
        "end_date": datetime(2023, 10, 30),
        "promises": [
            "Rehabilitate 50 km of roads",
            "Completion by October 2023"
        ],
        "accomplishments": [
            "Rehabilitated 48 km of roads",
            "Project completed on schedule"
        ],
        "source_url": "https://manila.gov.ph/projects/road-rehab"
    },
    {
        "lgu_id": 1,
        "name": "Public Market Modernization",
        "description": "Renovation and digitalization of city public market",
        "budget": 25000000.0,
        "status": "ongoing",
        "start_date": datetime(2024, 1, 1),
        "end_date": datetime(2024, 6, 30),
        "promises": [
            "Complete market renovation by June 2024",
            "Implement digital payment system",
            "Create 500 vendor stalls"
        ],
        "accomplishments": [
            "Market renovation 60% complete",
            "Digital payment system launched",
            "400 vendor stalls created"
        ],
        "source_url": "https://manila.gov.ph/projects/market-mod"
    },
    {
        "lgu_id": 2,
        "name": "Community Health Center Expansion",
        "description": "Expansion of municipal health center facilities",
        "budget": 15000000.0,
        "status": "ongoing",
        "start_date": datetime(2023, 9, 1),
        "end_date": datetime(2024, 12, 31),
        "promises": [
            "Add 30 additional beds by December 2024",
            "Provide 24/7 emergency services",
            "Training for 50 healthcare workers"
        ],
        "accomplishments": [
            "Added 20 beds",
            "24/7 services operational",
            "Training incomplete - only 30 workers trained"
        ],
        "source_url": "https://binan.gov.ph/projects/health-center"
    },
    {
        "lgu_id": 3,
        "name": "Metro Tagaytay Integrated Transport",
        "description": "Development of integrated public transportation system",
        "budget": 500000000.0,
        "status": "ongoing",
        "start_date": datetime(2023, 3, 1),
        "end_date": datetime(2025, 6, 30),
        "promises": [
            "Complete Phase 1 by June 2024",
            "Acquire 200 buses",
            "Integrate 5 transport modes"
        ],
        "accomplishments": [
            "Phase 1 significantly delayed - only 30% complete",
            "60 buses acquired",
            "Only 2 transport modes integrated"
        ],
        "source_url": "https://laguna.gov.ph/projects/transport"
    }
]

SAMPLE_REPORTS = [
    {
        "lgu_id": 1,
        "project_id": 1,
        "promise": "Complete water supply system by December 2023",
        "promised_date": datetime(2023, 12, 31),
        "accomplishment_date": datetime(2024, 6, 30),
        "status": "delayed",
        "severity": "high",
        "anomaly_score": 0.78,
        "details": {
            "promised": "System fully operational by December 2023",
            "actual": "System 40% complete as of June 2024",
            "delay": "6 months",
            "impact": "15,000 households still without service"
        }
    },
    {
        "lgu_id": 1,
        "project_id": 2,
        "promise": "Rehabilitate 50 km of roads",
        "promised_date": datetime(2023, 10, 31),
        "accomplishment_date": datetime(2023, 10, 30),
        "status": "fulfilled",
        "severity": "low",
        "anomaly_score": 0.15,
        "details": {
            "promised": "50 km rehabilitation",
            "actual": "48 km rehabilitated",
            "status": "Nearly complete, minor variance acceptable"
        }
    },
    {
        "lgu_id": 3,
        "project_id": 5,
        "promise": "Complete Phase 1 integrated transport by June 2024",
        "promised_date": datetime(2024, 6, 30),
        "accomplishment_date": None,
        "status": "broken",
        "severity": "critical",
        "anomaly_score": 0.92,
        "details": {
            "promised": "Phase 1 complete by June 2024",
            "actual": "Only 30% complete as of current date",
            "delay": "12+ months expected",
            "impact": "Public transportation crisis continues",
            "budget_impact": "Infrastructure investment stalled"
        }
    },
    {
        "lgu_id": 2,
        "project_id": 4,
        "promise": "Train 50 healthcare workers by December 2024",
        "promised_date": datetime(2024, 12, 31),
        "accomplishment_date": None,
        "status": "delayed",
        "severity": "medium",
        "anomaly_score": 0.65,
        "details": {
            "promised": "50 healthcare workers trained",
            "actual": "30 workers trained so far",
            "status": "Behind schedule - 60% complete"
        }
    },
    {
        "lgu_id": 1,
        "project_id": 3,
        "promise": "Implement digital payment system by Q2 2024",
        "promised_date": datetime(2024, 6, 30),
        "accomplishment_date": datetime(2024, 5, 15),
        "status": "fulfilled",
        "severity": "low",
        "anomaly_score": 0.08,
        "details": {
            "promised": "Digital payment system online",
            "actual": "System launched ahead of schedule",
            "early_delivery": "45 days early"
        }
    }
]

def init_sample_data():
    """Initialize database with sample data"""
    try:
        # Initialize database
        init_db()
        logger.info("Database initialized")
        
        db = SessionLocal()
        
        # Check if data already exists
        existing_lgus = db.query(LGU).count()
        if existing_lgus > 0:
            logger.info("Sample data already exists, skipping initialization")
            return
        
        # Add LGUs
        lgus = []
        for lgu_data in SAMPLE_LGUS:
            lgu = LGU(**lgu_data)
            db.add(lgu)
            lgus.append(lgu)
        
        db.commit()
        logger.info(f"Added {len(lgus)} LGUs")
        
        # Add projects
        projects = []
        for project_data in SAMPLE_PROJECTS:
            proj_data = project_data.copy()
            promises = proj_data.pop("promises", [])
            accomplishments = proj_data.pop("accomplishments", [])
            
            project = Project(
                **proj_data,
                promises={"list": promises},
                accomplishments={"list": accomplishments}
            )
            db.add(project)
            projects.append(project)
        
        db.commit()
        logger.info(f"Added {len(projects)} projects")
        
        # Add reports
        reports = []
        for report_data in SAMPLE_REPORTS:
            report = BrokenPromiseReport(**report_data)
            db.add(report)
            reports.append(report)
        
        db.commit()
        logger.info(f"Added {len(reports)} broken promise reports")
        
        # Create dashboard summary
        summary = DashboardSummary(
            total_lgus=len(lgus),
            total_projects=len(projects),
            total_budget=sum(p.budget for p in projects),
            fulfilled_promises=sum(1 for r in reports if r.status == "fulfilled"),
            broken_promises=sum(1 for r in reports if r.status == "broken"),
            delayed_promises=sum(1 for r in reports if r.status == "delayed"),
            average_anomaly_score=sum(r.anomaly_score for r in reports) / len(reports) if reports else 0.0
        )
        db.add(summary)
        db.commit()
        logger.info("Dashboard summary created")
        
        db.close()
        logger.info("Sample data initialization complete!")
        
    except Exception as e:
        logger.error(f"Error initializing sample data: {str(e)}")
        raise

if __name__ == "__main__":
    init_sample_data()
