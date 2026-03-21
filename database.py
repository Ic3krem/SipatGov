from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Text, ForeignKey, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class LGU(Base):
    __tablename__ = "lgus"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    url = Column(String, unique=True)
    contact_info = Column(String, nullable=True)
    budget_endpoint = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    projects = relationship("Project", back_populates="lgu", cascade="all, delete-orphan")
    reports = relationship("BrokenPromiseReport", back_populates="lgu", cascade="all, delete-orphan")
    
class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    lgu_id = Column(Integer, ForeignKey("lgus.id"))
    name = Column(String, index=True)
    description = Column(Text)
    budget = Column(Float)
    status = Column(String)  # ongoing, completed, planned
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    promises = Column(JSON)  # structured promises extracted via NLP
    accomplishments = Column(JSON)  # structured accomplishments extracted via NLP
    source_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    lgu = relationship("LGU", back_populates="projects")
    reports = relationship("BrokenPromiseReport", back_populates="project", cascade="all, delete-orphan")
    
class BrokenPromiseReport(Base):
    __tablename__ = "broken_promise_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    lgu_id = Column(Integer, ForeignKey("lgus.id"))
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    promise = Column(Text)
    promised_date = Column(DateTime)
    accomplishment_date = Column(DateTime, nullable=True)
    status = Column(String)  # broken, delayed, fulfilled
    severity = Column(String)  # critical, high, medium, low
    anomaly_score = Column(Float)  # 0.0 to 1.0
    details = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    lgu = relationship("LGU", back_populates="reports")
    project = relationship("Project", back_populates="reports")
    
class DashboardSummary(Base):
    __tablename__ = "dashboard_summary"
    
    id = Column(Integer, primary_key=True, index=True)
    total_lgus = Column(Integer)
    total_projects = Column(Integer)
    total_budget = Column(Float)
    fulfilled_promises = Column(Integer)
    broken_promises = Column(Integer)
    delayed_promises = Column(Integer)
    average_anomaly_score = Column(Float)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
class CrawlLog(Base):
    __tablename__ = "crawl_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    lgu_id = Column(Integer, ForeignKey("lgus.id"), nullable=True)
    source = Column(String)  # philgeps, coa, lgu_website
    status = Column(String)  # running, completed, failed
    urls_processed = Column(Integer)
    items_found = Column(Integer)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
