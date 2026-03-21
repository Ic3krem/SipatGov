# SipatGov Backend API

AI-powered government data crawling and promise verification system. Automatically crawls government portals, extracts promises and accomplishments, and uses cross-check AI models to generate broken promise reports and anomaly risk scores.

## Features

- **Web Crawling**: Automated crawling of Philippine government portals (PhilGEPS, COA, LGU websites)
- **OCR Processing**: Extracts text from PDFs and images using PyTorch models
- **NLP Extraction**: Identifies promises, budget allocations, project timelines, and entities
- **Cross-Check AI**: Compares promises against accomplishments, generates anomaly scores
- **REST API**: FastAPI server with CORS support for React frontend
- **GPU Acceleration**: Optimized for NVIDIA RTX 5060 Ti (16GB VRAM)
- **Database**: PostgreSQL support with optional MongoDB
- **Monitoring**: Logging, crawl status tracking, health checks

## System Requirements

- Python 3.10+
- NVIDIA CUDA 12.1 (for GPU acceleration)
- PostgreSQL 13+ (or MongoDB)
- 32 GB RAM, 16 GB VRAM (RTX 5060 Ti recommended)
- 50 GB disk space for models and crawled data

## Quick Start on Windows

### 1. Download and Setup

```bash
# Clone or extract the project
cd SipatGovBackendApi

# Copy environment template
copy .env.example .env

# Edit .env with your database credentials
```

### 2. Launch Server

**Option A: Double-Click Launcher (Recommended)**
```
run_server.bat
```

**Option B: Manual Setup**
```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start server
python main.py
```

Server runs at: `http://localhost:8000`
API Docs: `http://localhost:8000/docs`

## Installation

### Local Development Setup

1. **Clone the repository**
```bash
git clone <repo-url>
cd SipatGovBackendApi
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup database**
```bash
# PostgreSQL (recommended)
# Create database and user:
psql -U postgres -c "CREATE DATABASE sipatgov_db;"
psql -U postgres -c "CREATE USER sipatgov_user WITH PASSWORD 'your_password';"
```

5. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

6. **Run migrations**
```bash
# Database tables are created automatically on first run
python main.py
```

## Configuration

Edit `.env` file:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/sipatgov_db

# GPU
USE_GPU=True
GPU_ID=0

# Server
HOST=0.0.0.0
PORT=8000

# Crawling limits (demo mode)
MAX_URLS_PER_LGU=5
CRAWL_RETRY_ATTEMPTS=3
```

## Database Schema

### Tables

- **lgus**: Local government units
- **projects**: Government projects and programs
- **broken_promise_reports**: Promise vs accomplishment comparisons
- **dashboard_summary**: Aggregated statistics
- **crawl_logs**: Crawling operation history

## API Endpoints

### LGUs
- `GET /lgus` - List all LGUs
- `GET /lgus/{lgu_id}` - Get specific LGU
- `GET /projects?lgu_id=xxx` - Get projects for LGU
- `GET /reports?lgu_id=xxx` - Get reports for LGU

### Projects
- `GET /projects` - List all projects
- `GET /projects/{project_id}` - Get project details

### Reports
- `GET /reports` - List all reports
- `GET /reports/{report_id}` - Get report details
- `GET /reports?severity=critical` - Filter by severity

### Dashboard
- `GET /dashboard-summary` - Aggregated statistics

### Monitoring
- `GET /health` - Health check
- `GET /crawl-logs` - Crawling logs
- `POST /crawl` - Trigger manual crawl

## Example API Responses

### GET /lgus
```json
[
  {
    "id": 1,
    "name": "City of Manila",
    "url": "https://manila.gov.ph",
    "contact_info": "contact@manila.gov.ph",
    "created_at": "2024-01-15T10:30:00"
  }
]
```

### GET /dashboard-summary
```json
{
  "total_lgus": 3,
  "total_projects": 45,
  "total_budget": 2500000000.0,
  "fulfilled_promises": 32,
  "broken_promises": 8,
  "delayed_promises": 5,
  "average_anomaly_score": 0.35,
  "last_updated": "2024-01-15T12:00:00"
}
```

### GET /reports?severity=critical
```json
[
  {
    "id": 1,
    "promise": "Complete water supply system by December 2023",
    "status": "broken",
    "severity": "critical",
    "anomaly_score": 0.92,
    "created_at": "2024-01-10T08:00:00"
  }
]
```

## GPU Acceleration Setup

### Requirements
- NVIDIA CUDA 12.1
- NVIDIA cuDNN 9.0
- NVIDIA GPU with 8GB+ VRAM (RTX 5060 Ti = 16GB)

### Installation

1. **Install CUDA Toolkit 12.1**
   - Download: https://developer.nvidia.com/cuda-12-1-1-download-archive
   - Install with Visual Studio integration

2. **Install cuDNN**
   - Download: https://developer.nvidia.com/cudnn
   - Extract to CUDA installation directory

3. **Verify GPU setup**
```bash
python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
```

4. **Environment variables** (set in .env)
```
USE_GPU=True
GPU_ID=0
PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
```

## Performance Optimization

For RTX 5060 Ti (16 GB VRAM, 32 GB RAM):

1. **Batch Processing**
   - OCR_BATCH_SIZE=4
   - MAX_URLS_PER_LGU=5 (demo limit)

2. **Memory Management**
   ```python
   PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
   ```

3. **Model Loading**
   - Models lazy-loaded on first use
   - ~8GB VRAM for full pipeline

## Running with React Frontend

### CORS Configuration

The API includes CORS middleware. Configure in `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### React Integration

```javascript
// Example: Fetch LGUs
const response = await fetch('http://localhost:8000/lgus');
const lgus = await response.json();

// Example: Fetch dashboard summary
const summary = await fetch('http://localhost:8000/dashboard-summary');
const stats = await summary.json();
```

## Project Structure

```
SipatGovBackendApi/
├── main.py                 # FastAPI app entry point
├── config.py              # Configuration management
├── database.py            # SQLAlchemy models
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── run_server.bat        # Windows launcher
├── api/
│   └── routes.py         # API endpoints
├── crawlers/
│   └── __init__.py       # Web crawlers
├── processors/
│   ├── ocr.py            # OCR processing
│   ├── nlp.py            # NLP extraction
│   └── crosscheck.py     # Cross-check AI model
├── models/               # PyTorch models (safetensors)
├── downloads/            # Crawled files
├── processed_data/       # Processed outputs
└── logs/                 # Application logs
```

## Crawling Demo Data

Example demo crawls 3 LGUs and extracts:
- 5 projects per LGU (limited for demo)
- PDFs, images, structured data
- Budget allocations
- Project timelines

Configure in `config.py`:
```python
EXAMPLE_LGUS = [
    {"name": "City of Manila", "url": "https://manila.gov.ph", ...},
    {"name": "Municipality of Binan", "url": "https://binan.gov.ph", ...},
    {"name": "Province of Laguna", "url": "https://laguna.gov.ph", ...},
]
```

## Models

### OCR Models
- **PaddleOCR**: Default, supports English/Filipino
- **Tesseract**: Fallback option

### NLP Models
- **facebook/bart-large-mnli**: Promise classification
- **dbmdz/bert-base-multilingual***: Entity extraction

Models auto-download on first use (~2-3 GB).

## Troubleshooting

### "CUDA out of memory"
- Reduce OCR_BATCH_SIZE: `OCR_BATCH_SIZE=2`
- Reduce MAX_WORKERS
- Close other GPU applications

### "Models failed to load"
- Check internet connection (models download from Hugging Face)
- Check disk space (50GB recommended)
- Verify CUDA installation: `nvidia-smi`

### "Database connection error"
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify credentials

### "Crawler timeout"
- Increase CRAWL_TIMEOUT: `CRAWL_TIMEOUT=60`
- Check internet connection
- Verify target URLs are accessible

## Logging

Logs are saved to `logs/server.log` and displayed in console.

View logs:
```bash
# Windows
type logs/server.log

# Linux/Mac
tail -f logs/server.log
```

## Production Deployment

For production deployment:

1. Use PostgreSQL with backups
2. Set `DEBUG=False` in .env
3. Configure appropriate CORS origins
4. Use reverse proxy (nginx/Apache)
5. Enable HTTPS
6. Run with production ASGI server (Gunicorn):

```bash
pip install gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Contributing

To add new AI models or processors:

1. Create new processor in `processors/`
2. Add configuration to `config.py`
3. Integrate into API routes
4. Update documentation

## License

Licensed under MIT License - see LICENSE file

## Support

For issues and questions, please create an issue in the repository.
