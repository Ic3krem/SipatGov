import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/sipatgov_db"
)
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/sipatgov_db")

# Use PostgreSQL as primary, with option for MongoDB
DB_TYPE = os.getenv("DB_TYPE", "postgresql")  # "postgresql" or "mongodb"

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
RELOAD = os.getenv("RELOAD", "True").lower() == "true"

# GPU Configuration
USE_GPU = os.getenv("USE_GPU", "True").lower() == "true"
DEVICE = "cuda" if USE_GPU else "cpu"
GPU_ID = int(os.getenv("GPU_ID", 0))

# OCR Configuration
OCR_BATCH_SIZE = int(os.getenv("OCR_BATCH_SIZE", 4))
OCR_MODEL = os.getenv("OCR_MODEL", "paddleocr")  # paddleocr or pytesseract

# NLP Configuration
NLP_MODEL = os.getenv("NLP_MODEL", "facebook/bart-large-mnli")
ENTITY_MODEL = os.getenv("ENTITY_MODEL", "dbmdz/bert-base-multilingual-cased-ner-wnut17")

# Crawling Configuration
CRAWL_TIMEOUT = int(os.getenv("CRAWL_TIMEOUT", 30))
CRAWL_RETRY_ATTEMPTS = int(os.getenv("CRAWL_RETRY_ATTEMPTS", 3))
MAX_URLS_PER_LGU = int(os.getenv("MAX_URLS_PER_LGU", 5))

# Example LGUs to Crawl (Demo)
EXAMPLE_LGUS = [
    {
        "name": "City of Manila",
        "url": "https://manila.gov.ph",
        "budget_endpoint": "https://data.gov.ph/api/action/datastore_search?resource_id=xxx",
    },
    {
        "name": "Municipality of Binan",
        "url": "https://binan.gov.ph",
        "budget_endpoint": "https://data.gov.ph/api/action/datastore_search?resource_id=yyy",
    },
    {
        "name": "Province of Laguna",
        "url": "https://laguna.gov.ph",
        "budget_endpoint": "https://data.gov.ph/api/action/datastore_search?resource_id=zzz",
    },
]

# Data Sources
PHILGEPS_API = "https://www.philgeps.gov.ph/api"
COA_API = "https://www.coa.gov.ph/api"
DATA_GOV_PH_API = "https://data.gov.ph/api"

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/server.log")

# Temporary Directories
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "downloads/")
PROCESSED_DIR = os.getenv("PROCESSED_DIR", "processed_data/")

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs("logs/", exist_ok=True)
