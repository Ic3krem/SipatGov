# Example API Responses - SipatGov Backend API

Reference guide for React frontend integration with example JSON responses.

## 1. LGU Management

### GET /lgus
**Get list of all LGUs**

```bash
curl http://localhost:8000/lgus
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "City of Manila",
    "url": "https://manila.gov.ph",
    "contact_info": "contact@manila.gov.ph",
    "created_at": "2024-01-15T10:30:00"
  },
  {
    "id": 2,
    "name": "Municipality of Binan",
    "url": "https://binan.gov.ph",
    "contact_info": "info@binan.gov.ph",
    "created_at": "2024-01-15T10:35:00"
  },
  {
    "id": 3,
    "name": "Province of Laguna",
    "url": "https://laguna.gov.ph",
    "contact_info": "contact@laguna.gov.ph",
    "created_at": "2024-01-15T10:40:00"
  }
]
```

### GET /lgus/{lgu_id}
**Get specific LGU details**

```bash
curl http://localhost:8000/lgus/1
```

**Response:**
```json
{
  "id": 1,
  "name": "City of Manila",
  "url": "https://manila.gov.ph",
  "contact_info": "contact@manila.gov.ph",
  "created_at": "2024-01-15T10:30:00"
}
```

## 2. Project Management

### GET /projects
**Get all projects**

```bash
curl http://localhost:8000/projects
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Water Supply System Upgrade",
    "description": "Expansion of water distribution network to underserved areas",
    "budget": 50000000.0,
    "status": "ongoing",
    "start_date": "2023-06-01T00:00:00",
    "end_date": "2024-12-31T00:00:00",
    "source_url": "https://manila.gov.ph/projects/water-supply"
  },
  {
    "id": 2,
    "name": "Road Rehabilitation Program",
    "description": "Repair and asphalt overlay of municipal roads",
    "budget": 75000000.0,
    "status": "completed",
    "start_date": "2023-01-15T00:00:00",
    "end_date": "2023-10-30T00:00:00",
    "source_url": "https://manila.gov.ph/projects/road-rehab"
  }
]
```

### GET /projects?lgu_id=1
**Get projects for specific LGU**

```bash
curl "http://localhost:8000/projects?lgu_id=1"
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Water Supply System Upgrade",
    "description": "Expansion of water distribution network to underserved areas",
    "budget": 50000000.0,
    "status": "ongoing",
    "start_date": "2023-06-01T00:00:00",
    "end_date": "2024-12-31T00:00:00",
    "source_url": "https://manila.gov.ph/projects/water-supply"
  },
  {
    "id": 3,
    "name": "Public Market Modernization",
    "description": "Renovation and digitalization of city public market",
    "budget": 25000000.0,
    "status": "ongoing",
    "start_date": "2024-01-01T00:00:00",
    "end_date": "2024-06-30T00:00:00",
    "source_url": "https://manila.gov.ph/projects/market-mod"
  }
]
```

### GET /projects?status=completed
**Filter projects by status**

```bash
curl "http://localhost:8000/projects?status=completed"
```

**Response:**
```json
[
  {
    "id": 2,
    "name": "Road Rehabilitation Program",
    "description": "Repair and asphalt overlay of municipal roads",
    "budget": 75000000.0,
    "status": "completed",
    "start_date": "2023-01-15T00:00:00",
    "end_date": "2023-10-30T00:00:00",
    "source_url": "https://manila.gov.ph/projects/road-rehab"
  }
]
```

### GET /projects/{project_id}
**Get specific project details**

```bash
curl http://localhost:8000/projects/1
```

**Response:**
```json
{
  "id": 1,
  "name": "Water Supply System Upgrade",
  "description": "Expansion of water distribution network to underserved areas",
  "budget": 50000000.0,
  "status": "ongoing",
  "start_date": "2023-06-01T00:00:00",
  "end_date": "2024-12-31T00:00:00",
  "source_url": "https://manila.gov.ph/projects/water-supply"
}
```

## 3. Broken Promise Reports

### GET /reports
**Get all broken promise reports**

```bash
curl http://localhost:8000/reports
```

**Response:**
```json
[
  {
    "id": 1,
    "promise": "Complete water supply system by December 2023",
    "status": "broken",
    "severity": "critical",
    "anomaly_score": 0.92,
    "created_at": "2024-01-10T08:00:00"
  },
  {
    "id": 2,
    "promise": "Allocate 500M pesos for road repair",
    "status": "delayed",
    "severity": "high",
    "anomaly_score": 0.78,
    "created_at": "2024-01-12T09:30:00"
  },
  {
    "id": 3,
    "promise": "Distribute free medicine to health centers",
    "status": "fulfilled",
    "severity": "low",
    "anomaly_score": 0.15,
    "created_at": "2024-01-08T14:20:00"
  }
]
```

### GET /reports?lgu_id=1
**Get reports for specific LGU**

```bash
curl "http://localhost:8000/reports?lgu_id=1"
```

**Response:**
```json
[
  {
    "id": 1,
    "promise": "Complete water supply system by December 2023",
    "status": "broken",
    "severity": "critical",
    "anomaly_score": 0.92,
    "created_at": "2024-01-10T08:00:00"
  },
  {
    "id": 2,
    "promise": "Allocate 500M pesos for road repair",
    "status": "delayed",
    "severity": "high",
    "anomaly_score": 0.78,
    "created_at": "2024-01-12T09:30:00"
  }
]
```

### GET /reports?severity=critical
**Filter reports by severity**

```bash
curl "http://localhost:8000/reports?severity=critical"
```

**Response:**
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

### GET /reports/{report_id}
**Get specific report**

```bash
curl http://localhost:8000/reports/1
```

**Response:**
```json
{
  "id": 1,
  "promise": "Complete water supply system by December 2023",
  "status": "broken",
  "severity": "critical",
  "anomaly_score": 0.92,
  "created_at": "2024-01-10T08:00:00"
}
```

## 4. Dashboard Summary

### GET /dashboard-summary
**Get aggregated statistics for dashboard**

```bash
curl http://localhost:8000/dashboard-summary
```

**Response:**
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

## 5. Monitoring & Status

### GET /health
**Health check**

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T12:35:42.123456",
  "message": "SipatGov Backend API is running"
}
```

### GET /crawl-logs
**Get crawling history**

```bash
curl http://localhost:8000/crawl-logs
```

**Response:**
```json
[
  {
    "id": 5,
    "source": "manual_trigger",
    "status": "running",
    "urls_processed": 12,
    "items_found": 8,
    "started_at": "2024-01-15T12:30:00",
    "completed_at": null,
    "error_message": null
  },
  {
    "id": 4,
    "source": "philgeps",
    "status": "completed",
    "urls_processed": 25,
    "items_found": 20,
    "started_at": "2024-01-15T10:00:00",
    "completed_at": "2024-01-15T10:45:00",
    "error_message": null
  },
  {
    "id": 3,
    "source": "coa",
    "status": "failed",
    "urls_processed": 15,
    "items_found": 10,
    "started_at": "2024-01-15T09:00:00",
    "completed_at": "2024-01-15T09:30:00",
    "error_message": "Connection timeout after 3 retries"
  }
]
```

### POST /crawl
**Trigger manual crawl**

```bash
curl -X POST http://localhost:8000/crawl?lgu_id=1
```

**Response:**
```json
{
  "status": "crawl_started",
  "log_id": 6,
  "message": "Crawl operation initiated"
}
```

## React Integration Examples

### Fetch LGUs
```javascript
async function fetchLGUs() {
  const response = await fetch('http://localhost:8000/lgus');
  const lgus = await response.json();
  return lgus;
}
```

### Fetch Dashboard Summary
```javascript
async function fetchDashboard() {
  const response = await fetch('http://localhost:8000/dashboard-summary');
  const summary = await response.json();
  return summary;
}
```

### Fetch Reports with Filters
```javascript
async function fetchReportsForLGU(lguId, severity = null) {
  let url = `http://localhost:8000/reports?lgu_id=${lguId}`;
  if (severity) {
    url += `&severity=${severity}`;
  }
  const response = await fetch(url);
  const reports = await response.json();
  return reports;
}
```

### Create Display Components
```javascript
// React component example
function DashboardWidget() {
  const [data, setData] = useState(null);
  
  useEffect(() => {
    fetchDashboard().then(setData);
  }, []);
  
  if (!data) return <div>Loading...</div>;
  
  return (
    <div className="dashboard">
      <h1>Government Accountability Dashboard</h1>
      <div className="stats">
        <div className="stat">
          <h2>{data.total_lgus}</h2>
          <p>LGUs Monitored</p>
        </div>
        <div className="stat">
          <h2>{data.total_projects}</h2>
          <p>Projects Tracked</p>
        </div>
        <div className="stat">
          <h2>{data.broken_promises}</h2>
          <p>Broken Promises</p>
        </div>
        <div className="stat">
          <h2>{data.average_anomaly_score.toFixed(2)}</h2>
          <p>Average Anomaly Score</p>
        </div>
      </div>
    </div>
  );
}
```

## Error Responses

### 404 Not Found
```json
{
  "detail": "LGU not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## API Documentation

Full interactive documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
