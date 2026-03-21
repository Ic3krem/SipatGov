from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from database import get_db, LGU, Project, BrokenPromiseReport, DashboardSummary, CrawlLog
from sqlalchemy import func, inspect
import json

router = APIRouter(tags=["UI"])

# HTML Dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SipatGov Admin Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        header {
            background: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        }
        
        header h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        header p {
            color: #666;
            font-size: 1.1em;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
            border-left: 5px solid #667eea;
        }
        
        .stat-label {
            color: #999;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }
        
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }
        
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        
        .tab-btn {
            background: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            font-weight: 500;
            color: #666;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        
        .tab-btn:hover {
            background: #f5f5f5;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .tab-btn.active {
            background: #667eea;
            color: white;
        }
        
        .content {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        
        thead {
            background: #f8f9fa;
            border-bottom: 2px solid #667eea;
        }
        
        th {
            padding: 15px;
            text-align: left;
            font-weight: 600;
            color: #667eea;
        }
        
        td {
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }
        
        tr:hover {
            background: #f8f9fa;
        }
        
        .status-badge {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            text-transform: capitalize;
        }
        
        .status-fulfilled {
            background: #d4edda;
            color: #155724;
        }
        
        .status-broken {
            background: #f8d7da;
            color: #721c24;
        }
        
        .status-delayed {
            background: #fff3cd;
            color: #856404;
        }
        
        .status-ongoing {
            background: #d1ecf1;
            color: #0c5460;
        }
        
        .status-completed {
            background: #d4edda;
            color: #155724;
        }
        
        .empty-state {
            text-align: center;
            padding: 40px 20px;
            color: #999;
        }
        
        .empty-state svg {
            width: 100px;
            height: 100px;
            margin-bottom: 20px;
            opacity: 0.5;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #667eea;
        }
        
        .spinner {
            display: inline-block;
            width: 40px;
            height: 40px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .severity-critical { color: #dc3545; font-weight: bold; }
        .severity-high { color: #fd7e14; font-weight: bold; }
        .severity-medium { color: #ffc107; font-weight: bold; }
        .severity-low { color: #28a745; font-weight: bold; }
        
        .score-badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            background: #f0f0f0;
            font-family: monospace;
            font-weight: 600;
        }
        
        .text-muted {
            color: #999;
            font-size: 0.9em;
        }
        
        .detail-row {
            display: grid;
            grid-template-columns: 150px 1fr;
            gap: 20px;
            margin-bottom: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        
        .detail-label {
            font-weight: 600;
            color: #667eea;
        }
        
        .detail-value {
            word-break: break-word;
        }
        
        @media (max-width: 768px) {
            header h1 {
                font-size: 1.8em;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
            
            table {
                font-size: 0.9em;
            }
            
            th, td {
                padding: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 SipatGov Database Admin</h1>
            <p>Real-time database monitoring and data inspection</p>
        </header>
        
        <div id="stats" class="stats-grid"></div>
        
        <div class="tabs">
            <button class="tab-btn active" onclick="switchTab('overview')">Overview</button>
            <button class="tab-btn" onclick="switchTab('lgus')">LGUs</button>
            <button class="tab-btn" onclick="switchTab('projects')">Projects</button>
            <button class="tab-btn" onclick="switchTab('reports')">Broken Promises</button>
            <button class="tab-btn" onclick="switchTab('crawl_logs')">Crawl Logs</button>
        </div>
        
        <div class="content">
            <!-- Overview Tab -->
            <div id="overview" class="tab-content active">
                <h2>Database Summary</h2>
                <div id="overview-content" class="loading">
                    <div class="spinner"></div>
                    <p style="margin-top: 10px;">Loading data...</p>
                </div>
            </div>
            
            <!-- LGUs Tab -->
            <div id="lgus" class="tab-content">
                <h2>Local Government Units (LGUs)</h2>
                <div id="lgus-content" class="loading">
                    <div class="spinner"></div>
                    <p style="margin-top: 10px;">Loading LGUs...</p>
                </div>
            </div>
            
            <!-- Projects Tab -->
            <div id="projects" class="tab-content">
                <h2>Projects</h2>
                <div id="projects-content" class="loading">
                    <div class="spinner"></div>
                    <p style="margin-top: 10px;">Loading projects...</p>
                </div>
            </div>
            
            <!-- Broken Promises Tab -->
            <div id="reports" class="tab-content">
                <h2>Broken Promise Reports</h2>
                <div id="reports-content" class="loading">
                    <div class="spinner"></div>
                    <p style="margin-top: 10px;">Loading reports...</p>
                </div>
            </div>
            
            <!-- Crawl Logs Tab -->
            <div id="crawl_logs" class="tab-content">
                <h2>Crawl Logs</h2>
                <div id="crawl_logs-content" class="loading">
                    <div class="spinner"></div>
                    <p style="margin-top: 10px;">Loading crawl logs...</p>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Fetch and display data
        async function loadData() {
            try {
                const response = await fetch('/ui/db-stats');
                const data = await response.json();
                displayStats(data.stats);
                displayOverview(data);
            } catch (error) {
                console.error('Error loading data:', error);
            }
        }
        
        function displayStats(stats) {
            const statsHtml = Object.entries(stats).map(([key, value]) => `
                <div class="stat-card">
                    <div class="stat-label">${formatLabel(key)}</div>
                    <div class="stat-value">${value}</div>
                </div>
            `).join('');
            document.getElementById('stats').innerHTML = statsHtml;
        }
        
        function formatLabel(str) {
            return str.replace(/_/g, ' ').split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
        }
        
        function displayOverview(data) {
            const html = `
                <div>
                    <h3 style="margin-bottom: 20px; color: #667eea;">Database Status</h3>
                    <div class="detail-row">
                        <div class="detail-label">Total Tables</div>
                        <div class="detail-value">${data.table_count}</div>
                    </div>
                    <div class="detail-row">
                        <div class="detail-label">Total Records</div>
                        <div class="detail-value">${data.total_records}</div>
                    </div>
                    <div class="detail-row">
                        <div class="detail-label">Last Updated</div>
                        <div class="detail-value">${new Date().toLocaleString()}</div>
                    </div>
                </div>
            `;
            document.getElementById('overview-content').innerHTML = html;
        }
        
        function switchTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
            
            // Load data for tab
            loadTabData(tabName);
        }
        
        async function loadTabData(tabName) {
            const endpoint = `/ui/${tabName}`;
            try {
                const response = await fetch(endpoint);
                const data = await response.json();
                displayTabData(tabName, data);
            } catch (error) {
                console.error(`Error loading ${tabName}:`, error);
                document.getElementById(`${tabName}-content`).innerHTML = 
                    '<p style="color: red;">Error loading data</p>';
            }
        }
        
        function displayTabData(tabName, data) {
            let html = '';
            
            if (!data.records || data.records.length === 0) {
                html = '<div class="empty-state"><p>No data available</p></div>';
            } else {
                if (tabName === 'lgus') {
                    html = buildLGUsTable(data.records);
                } else if (tabName === 'projects') {
                    html = buildProjectsTable(data.records);
                } else if (tabName === 'reports') {
                    html = buildReportsTable(data.records);
                } else if (tabName === 'crawl_logs') {
                    html = buildCrawlLogsTable(data.records);
                }
            }
            
            document.getElementById(`${tabName}-content`).innerHTML = html;
        }
        
        function buildLGUsTable(lgus) {
            let html = '<table><thead><tr><th>ID</th><th>Name</th><th>URL</th><th>Contact</th><th>Created</th></tr></thead><tbody>';
            lgus.forEach(lgu => {
                const created = new Date(lgu.created_at).toLocaleDateString();
                html += `
                    <tr>
                        <td>${lgu.id}</td>
                        <td><strong>${lgu.name}</strong></td>
                        <td><a href="${lgu.url}" target="_blank" style="color: #667eea;">${lgu.url.substring(0, 30)}...</a></td>
                        <td>${lgu.contact_info || 'N/A'}</td>
                        <td class="text-muted">${created}</td>
                    </tr>
                `;
            });
            html += '</tbody></table>';
            return html;
        }
        
        function buildProjectsTable(projects) {
            let html = '<table><thead><tr><th>ID</th><th>Name</th><th>LGU ID</th><th>Budget</th><th>Status</th><th>Start Date</th></tr></thead><tbody>';
            projects.forEach(project => {
                const status = `<span class="status-badge status-${project.status}">${project.status}</span>`;
                const startDate = project.start_date ? new Date(project.start_date).toLocaleDateString() : 'N/A';
                html += `
                    <tr>
                        <td>${project.id}</td>
                        <td><strong>${project.name}</strong></td>
                        <td>${project.lgu_id}</td>
                        <td>₱${project.budget.toLocaleString()}</td>
                        <td>${status}</td>
                        <td class="text-muted">${startDate}</td>
                    </tr>
                `;
            });
            html += '</tbody></table>';
            return html;
        }
        
        function buildReportsTable(reports) {
            let html = '<table><thead><tr><th>ID</th><th>Promise</th><th>Status</th><th>Severity</th><th>Anomaly Score</th><th>Created</th></tr></thead><tbody>';
            reports.forEach(report => {
                const status = `<span class="status-badge status-${report.status}">${report.status}</span>`;
                const severity = `<span class="severity-${report.severity}">${report.severity}</span>`;
                const score = `<span class="score-badge">${report.anomaly_score.toFixed(3)}</span>`;
                const created = new Date(report.created_at).toLocaleDateString();
                const promise = report.promise.substring(0, 50);
                html += `
                    <tr>
                        <td>${report.id}</td>
                        <td><strong>${promise}...</strong></td>
                        <td>${status}</td>
                        <td>${severity}</td>
                        <td>${score}</td>
                        <td class="text-muted">${created}</td>
                    </tr>
                `;
            });
            html += '</tbody></table>';
            return html;
        }
        
        function buildCrawlLogsTable(logs) {
            let html = '<table><thead><tr><th>ID</th><th>Source</th><th>Status</th><th>URLs Processed</th><th>Items Found</th><th>Started</th></tr></thead><tbody>';
            logs.forEach(log => {
                const status = `<span class="status-badge status-${log.status}">${log.status}</span>`;
                const started = new Date(log.started_at).toLocaleDateString();
                html += `
                    <tr>
                        <td>${log.id}</td>
                        <td><strong>${log.source}</strong></td>
                        <td>${status}</td>
                        <td>${log.urls_processed}</td>
                        <td>${log.items_found}</td>
                        <td class="text-muted">${started}</td>
                    </tr>
                `;
            });
            html += '</tbody></table>';
            return html;
        }
        
        // Load data on page load
        window.addEventListener('load', () => {
            loadData();
            // Refresh every 30 seconds
            setInterval(loadData, 30000);
        });
    </script>
</body>
</html>
"""

@router.get("/", response_class=HTMLResponse)
async def dashboard():
    """Serve the database dashboard UI"""
    return DASHBOARD_HTML

@router.get("/db-stats", response_class=JSONResponse)
async def get_db_stats(db: Session = Depends(get_db)):
    """Get database statistics"""
    try:
        lgus_count = db.query(func.count(LGU.id)).scalar() or 0
        projects_count = db.query(func.count(Project.id)).scalar() or 0
        reports_count = db.query(func.count(BrokenPromiseReport.id)).scalar() or 0
        crawl_logs_count = db.query(func.count(CrawlLog.id)).scalar() or 0
        
        total_records = lgus_count + projects_count + reports_count + crawl_logs_count
        
        stats = {
            "lgus": lgus_count,
            "projects": projects_count,
            "reports": reports_count,
            "crawl_logs": crawl_logs_count,
        }
        
        return {
            "stats": stats,
            "total_records": total_records,
            "table_count": 5
        }
    except Exception as e:
        return {
            "error": str(e),
            "stats": {},
            "total_records": 0,
            "table_count": 0
        }

@router.get("/lgus")
async def get_lgus_data(db: Session = Depends(get_db)):
    """Get all LGUs"""
    try:
        lgus = db.query(LGU).all()
        records = [
            {
                "id": lgu.id,
                "name": lgu.name,
                "url": lgu.url,
                "contact_info": lgu.contact_info,
                "created_at": lgu.created_at
            }
            for lgu in lgus
        ]
        return {"records": records}
    except Exception as e:
        return {"records": [], "error": str(e)}

@router.get("/projects")
async def get_projects_data(db: Session = Depends(get_db)):
    """Get all projects"""
    try:
        projects = db.query(Project).all()
        records = [
            {
                "id": project.id,
                "name": project.name,
                "lgu_id": project.lgu_id,
                "budget": project.budget,
                "status": project.status,
                "start_date": project.start_date,
                "description": project.description[:100] if project.description else ""
            }
            for project in projects
        ]
        return {"records": records}
    except Exception as e:
        return {"records": [], "error": str(e)}

@router.get("/reports")
async def get_reports_data(db: Session = Depends(get_db)):
    """Get all broken promise reports"""
    try:
        reports = db.query(BrokenPromiseReport).all()
        records = [
            {
                "id": report.id,
                "promise": report.promise,
                "status": report.status,
                "severity": report.severity,
                "anomaly_score": report.anomaly_score,
                "created_at": report.created_at
            }
            for report in reports
        ]
        return {"records": records}
    except Exception as e:
        return {"records": [], "error": str(e)}

@router.get("/crawl_logs")
async def get_crawl_logs_data(db: Session = Depends(get_db)):
    """Get all crawl logs"""
    try:
        logs = db.query(CrawlLog).all()
        records = [
            {
                "id": log.id,
                "source": log.source,
                "status": log.status,
                "urls_processed": log.urls_processed,
                "items_found": log.items_found,
                "started_at": log.started_at,
                "error_message": log.error_message
            }
            for log in logs
        ]
        return {"records": records}
    except Exception as e:
        return {"records": [], "error": str(e)}
