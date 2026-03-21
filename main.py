from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from datetime import datetime
from config import HOST, PORT, DEBUG
from database import init_db
from api.routes import router
from api.ui import router as ui_router
from contextlib import asynccontextmanager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup
    logger.info("Starting SipatGov Backend API")
    try:
        # Initialize database
        init_db()
        logger.info("Database initialized successfully")
        
        # Initialize models if needed
        from processors.ocr import OCRProcessor
        from processors.nlp import NLPProcessor
        from processors.crosscheck import CrossCheckProcessor
        
        logger.info("Loading AI models...")
        # Note: Models will be loaded on first use to save startup time
        logger.info("Startup complete")
    except Exception as e:
        logger.warning(f"Startup warning: {str(e)}")
        logger.info("Continuing without database - API will still work")
    
    yield
    
    # Shutdown
    logger.info("Shutting down SipatGov Backend API")

# Create FastAPI app with lifespan
app = FastAPI(
    title="SipatGov Backend API",
    description="AI-powered government data crawling and promise verification system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# CORS Middleware - Allow React frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)
app.include_router(ui_router, prefix="/ui")

# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting server on {HOST}:{PORT}")
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        reload=DEBUG,
        log_level="info"
    )
