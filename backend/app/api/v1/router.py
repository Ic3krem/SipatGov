from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    budgets,
    crawler,
    dashboard,
    documents,
    lgus,
    projects,
    promises,
    regions,
    reports,
    scheduler,
    search,
)

api_v1_router = APIRouter()

api_v1_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_v1_router.include_router(regions.router, prefix="/regions", tags=["Regions"])
api_v1_router.include_router(lgus.router, prefix="/lgus", tags=["LGUs"])
api_v1_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
api_v1_router.include_router(budgets.router, prefix="/budgets", tags=["Budgets"])
api_v1_router.include_router(promises.router, prefix="/promises", tags=["Promises"])
api_v1_router.include_router(reports.router, prefix="/reports", tags=["Community Reports"])
api_v1_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
api_v1_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_v1_router.include_router(search.router, prefix="/search", tags=["Search"])
api_v1_router.include_router(crawler.router, prefix="/crawler", tags=["Crawler"])
api_v1_router.include_router(scheduler.router, prefix="/scheduler", tags=["Scheduler"])
