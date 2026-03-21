# Production Deployment Guide

This guide covers deploying SipatGov Backend API to production environments.

## Pre-Deployment Checklist

- [ ] All tests pass locally
- [ ] GPU drivers and CUDA verified
- [ ] Database backups configured
- [ ] SSL certificates ready
- [ ] Domain name configured
- [ ] Environment variables set
- [ ] Monitoring and logging configured
- [ ] Firewall rules configured

## Deployment Options

### Option 1: Linux Server (Recommended)

#### Prerequisites
- Ubuntu 20.04 LTS or later
- 32+ GB RAM, 16 GB VRAM (GPU)
- Python 3.10+
- PostgreSQL 13+
- NGINX reverse proxy
- SSL certificate (Let's Encrypt or commercial)

#### Step 1: Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.10 python3-pip python3-venv \
  postgresql postgresql-contrib nginx \
  git curl wget htop

# Install CUDA (for GPU)
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-repo-ubuntu2004_12.1.0-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu2004_12.1.0-1_amd64.deb
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub
sudo apt update
sudo apt install -y cuda-12-1
```

#### Step 2: PostgreSQL Setup

```bash
# Create database and user
sudo -u postgres psql <<EOF
CREATE DATABASE sipatgov_db;
CREATE USER sipatgov_user WITH PASSWORD 'your_secure_password_here';
ALTER ROLE sipatgov_user SET client_encoding TO 'utf8';
ALTER ROLE sipatgov_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE sipatgov_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE sipatgov_db TO sipatgov_user;
\q
EOF

# Enable PostgreSQL to start on boot
sudo systemctl enable postgresql
sudo systemctl start postgresql
```

#### Step 3: Application Setup

```bash
# Create application user
sudo useradd -m -s /bin/bash sipatgov

# Clone repository
sudo -u sipatgov git clone <repo-url> /home/sipatgov/app
cd /home/sipatgov/app

# Create virtual environment
sudo -u sipatgov python3.10 -m venv venv
sudo -u sipatgov venv/bin/pip install --upgrade pip
sudo -u sipatgov venv/bin/pip install -r requirements.txt

# Configure environment
sudo -u sipatgov cp .env.example .env
# Edit .env with production settings
```

#### Step 4: Systemd Service

Create `/etc/systemd/system/sipatgov.service`:

```ini
[Unit]
Description=SipatGov Backend API
After=network.target postgres.service

[Service]
Type=notify
User=sipatgov
WorkingDirectory=/home/sipatgov/app
Environment="PATH=/home/sipatgov/app/venv/bin"
Environment="PYTHONUNBUFFERED=1"
Environment="PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512"
ExecStart=/home/sipatgov/app/venv/bin/gunicorn \
  main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 127.0.0.1:8000 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable sipatgov
sudo systemctl start sipatgov
sudo systemctl status sipatgov
```

#### Step 5: NGINX Configuration

Create `/etc/nginx/sites-available/sipatgov`:

```nginx
upstream sipatgov_backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your_domain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your_domain.com;

    # SSL certificates (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/your_domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your_domain.com/privkey.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;

    # Gzip compression
    gzip on;
    gzip_types text/plain application/json application/javascript;

    client_max_body_size 100M;

    location / {
        proxy_pass http://sipatgov_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/sipatgov /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### Step 6: SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d your_domain.com
```

### Option 2: Docker Deployment

#### Dockerfile

```dockerfile
FROM nvidia/cuda:12.1.1-devel-ubuntu22.04

WORKDIR /app

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Environment
ENV PYTHONUNBUFFERED=1
ENV PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512

# Expose port
EXPOSE 8000

# Run server
CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

#### Docker Compose

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: sipatgov_db
      POSTGRES_USER: sipatgov_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U sipatgov_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build: .
    environment:
      DATABASE_URL: postgresql://sipatgov_user:${DB_PASSWORD}@db:5432/sipatgov_db
      USE_GPU: "true"
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./logs:/app/logs
      - ./downloads:/app/downloads
    restart: unless-stopped
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

volumes:
  postgres_data:
```

Run:

```bash
docker-compose up -d
```

### Option 3: Cloud Platforms

#### AWS EC2 with GPU

1. **Launch instance** (g4dn.xlarge or higher)
2. **Security group**: Open ports 80, 443
3. **Follow Linux setup above**

#### Google Cloud Compute Engine

1. **Create VM instance** with GPU
2. **Setup** same as Linux
3. **Configure firewall** for HTTP/HTTPS

#### Azure Virtual Machines

1. **GPU VM (N-series)**
2. **Linux setup as above**
3. Use **Application Gateway** for SSL termination

## Monitoring & Logging

### Health Checks

```bash
# Monitor service
curl https://your_domain.com/health

# View logs
sudo journalctl -u sipatgov -f

# PostgreSQL monitoring
sudo -u postgres psql -c "SELECT * FROM pg_stat_activity;"
```

### Prometheus Metrics (Optional)

Add to `main.py`:

```python
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response

api_requests = Counter('api_requests_total', 'Total API requests', ['method', 'endpoint'])
api_latency = Histogram('api_request_duration_seconds', 'API request latency')

@app.middleware("http")
async def add_metrics(request, call_next):
    api_requests.labels(method=request.method, endpoint=request.url.path).inc()
    with api_latency.time():
        response = await call_next(request)
    return response

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

## Backup Strategy

### PostgreSQL Backups

```bash
# Daily backup
0 2 * * * pg_dump -h localhost -U sipatgov_user sipatgov_db | gzip > /backup/sipatgov_db_$(date +\%Y\%m\%d).sql.gz

# Keep 30 days
find /backup -name "sipatgov_db_*.sql.gz" -mtime +30 -delete
```

## Security Best Practices

1. **Environment variables**: Never commit `.env` to git
2. **CORS**: Restrict origins to your React domain
3. **Rate limiting**: Add rate limiting middleware
4. **HTTPS**: Always use SSL/TLS
5. **Database**: Use strong passwords, regular backups
6. **Firewalls**: Restrict access by IP
7. **Monitoring**: Set up alerts for errors
8. **Updates**: Keep dependencies updated

## Scaling

For high traffic:

1. **Load balancer**: Use NGINX, HAProxy, or cloud LB
2. **Database replication**: PostgreSQL streaming replication
3. **Caching**: Add Redis for caching
4. **CDN**: CloudFlare, AWS CloudFront for static assets
5. **Horizontal scaling**: Multiple API instances

## Rollback Plan

```bash
# If deployment fails
git log --oneline
git checkout <previous-commit>
systemctl restart sipatgov
```

## Support

For deployment issues, check:
- Application logs: `/home/sipatgov/app/logs/`
- System logs: `journalctl -u sipatgov -f`
- PostgreSQL: `psql -U sipatgov_user -d sipatgov_db`
