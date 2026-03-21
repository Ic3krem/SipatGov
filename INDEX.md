# Documentation Index

Your complete guide to SipatGov Backend API. Start here!

## 🚀 Getting Started (Choose Your Level)

### ⚡ Fastest: 30 Seconds
1. Open Command Prompt
2. Navigate to project folder
3. Double-click: `run_server.bat`
4. Open browser: http://localhost:8000/docs

### ⏱️ Quick: 5 Minutes
- Read: [QUICKSTART.md](QUICKSTART.md)
- Follow the 4 simple steps
- Server will be running

### 📚 Thorough: 30 Minutes  
- Read: [WINDOWS_SETUP.md](WINDOWS_SETUP.md)
- Detailed step-by-step for all requirements
- Includes database setup

## 📖 Documentation Guide

### New Users
| Document | Purpose | Read Time |
|----------|---------|-----------|
| [QUICKSTART.md](QUICKSTART.md) | 5-minute setup | 5 min |
| [CHECKLIST.md](CHECKLIST.md) | Setup verification | 10 min |
| [README.md](README.md) | Full features overview | 15 min |

### Windows Users
| Document | Purpose | Read Time |
|----------|---------|-----------|
| [WINDOWS_SETUP.md](WINDOWS_SETUP.md) | Detailed Windows guide | 20 min |
| [run_server.bat](run_server.bat) | Automatic launcher | 0 min (auto) |
| [run_server.ps1](run_server.ps1) | PowerShell alternative | 0 min (auto) |

### Developers
| Document | Purpose | Read Time |
|----------|---------|-----------|
| [API_EXAMPLES.md](API_EXAMPLES.md) | Response formats + React code | 15 min |
| [README.md](README.md) | Architecture + API reference | 20 min |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Structure + tech stack | 10 min |

### DevOps/Production
| Document | Purpose | Read Time |
|----------|---------|-----------|
| [DEPLOYMENT.md](DEPLOYMENT.md) | Production, Docker, Cloud | 30 min |
| [README.md](README.md) | Scaling & monitoring | 15 min |
| [config.py](config.py) | All configuration options | 10 min |

### Troubleshooting
| Document | Purpose | Read Time |
|----------|---------|-----------|
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | 25+ solutions | 5 min per issue |
| [WINDOWS_SETUP.md](WINDOWS_SETUP.md#verification-checklist) | Verification steps | 5 min |
| [logs/server.log](logs/server.log) | Application logs | As needed |

## 🔗 Quick Links by Task

### "I want to launch the server"
1. [QUICKSTART.md](QUICKSTART.md)
2. Double-click `run_server.bat`
3. Visit http://localhost:8000/docs

### "I need detailed Windows setup"
1. [WINDOWS_SETUP.md](WINDOWS_SETUP.md) - Step 1-10
2. [CHECKLIST.md](CHECKLIST.md) - Verify each step
3. Double-click `run_server.bat`

### "I want to connect React frontend"
1. [API_EXAMPLES.md](API_EXAMPLES.md) - Example responses
2. [README.md](README.md#running-with-react-frontend) - CORS config
3. Follow code examples in [API_EXAMPLES.md](API_EXAMPLES.md)

### "I need to deploy to production"
1. [DEPLOYMENT.md](DEPLOYMENT.md) - Choose platform
2. Follow step-by-step for your platform
3. [README.md](README.md#production-deployment) - Best practices

### "Something isn't working"
1. [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Search issue
2. [WINDOWS_SETUP.md](WINDOWS_SETUP.md#verification-checklist) - Verify setup
3. Check `logs/server.log` - View error details

## 📋 File Organization

```
Documentation/
├── QUICKSTART.md          ← Start here (5 min)
├── CHECKLIST.md           ← Verify setup
├── WINDOWS_SETUP.md       ← Detailed guide
├── README.md              ← Full reference
├── API_EXAMPLES.md        ← React integration
├── DEPLOYMENT.md          ← Production
├── TROUBLESHOOTING.md     ← Solutions
├── PROJECT_SUMMARY.md     ← Overview
└── INDEX.md               ← This file

Code/
├── main.py                ← Server entry point
├── config.py              ← Configuration
├── database.py            ← Database models
├── init_data.py           ← Demo data loader
├── api/routes.py          ← API endpoints
├── crawlers/              ← Web crawlers
├── processors/            ← OCR/NLP/Cross-check
└── models/                ← AI models

Launchers/
├── run_server.bat         ← Windows batch (fastest)
└── run_server.ps1         ← PowerShell alternative

Config/
├── .env.example          ← Configuration template
├── requirements.txt      ← Dependencies
└── .gitignore            ← Git ignore rules
```

## 🎯 Common Tasks

### Task: Get server running
**Docs**: [QUICKSTART.md](QUICKSTART.md) → [CHECKLIST.md](CHECKLIST.md)
**Time**: 5 minutes
**Steps**: 4

### Task: Setup PostgreSQL database
**Docs**: [WINDOWS_SETUP.md](WINDOWS_SETUP.md#step-2-install-postgresql)
**Time**: 10 minutes
**Steps**: 5

### Task: Load demo data
**Docs**: [README.md](README.md#crawling-demo-data) → `python init_data.py`
**Time**: 2 minutes
**Steps**: 2

### Task: Integrate with React
**Docs**: [API_EXAMPLES.md](API_EXAMPLES.md) → [README.md](README.md#running-with-react-frontend)
**Time**: 15 minutes
**Steps**: 3

### Task: Setup GPU acceleration
**Docs**: [README.md](README.md#gpu-acceleration-setup)
**Time**: 20 minutes
**Steps**: 4

### Task: Deploy to production
**Docs**: [DEPLOYMENT.md](DEPLOYMENT.md)
**Time**: 30-60 minutes
**Steps**: 6-10

## 📊 Documentation Road Map

### Start
```
[QUICKSTART.md] 
    ↓
[CHECKLIST.md]
    ↓
```

### Choose Path

**Path 1: Local Development**
```
[README.md]
    ↓
[API_EXAMPLES.md]
    ↓
[React Integration]
```

**Path 2: Production**
```
[DEPLOYMENT.md]
    ↓
[Choose: Linux/Docker/Cloud]
    ↓
[Deploy & Monitor]
```

**Path 3: Troubleshooting**
```
[TROUBLESHOOTING.md]
    ↓
[Find Issue]
    ↓
[Follow Solution]
```

## 🔑 Key Files Reference

| File | Purpose | For Whom |
|------|---------|----------|
| `main.py` | Server entry point | Developers |
| `config.py` | All settings | DevOps |
| `database.py` | Database models | Developers |
| `api/routes.py` | API endpoints | Frontend devs |
| `processors/*` | AI/ML logic | Data scientists |
| `.env.example` | Configuration template | Everyone |
| `requirements.txt` | Dependencies | DevOps |
| `run_server.bat` | Windows launcher | End users |

## 🆘 Getting Help

### Quick Issues (< 1 minute)
→ Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) section headings

### Setup Issues (< 5 minutes)
→ Follow [CHECKLIST.md](CHECKLIST.md) step by step

### Detailed Troubleshooting (< 10 minutes)
→ Full guide: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### Complex Issues (> 10 minutes)
1. Check `logs/server.log`
2. Try solutions in [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
3. Consult [README.md](README.md) architecture section

## 📱 Mobile/Quick Reference

**Commands to Remember**:
```bash
# Activate environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start server
python main.py

# Load demo data
python init_data.py

# Check if running
curl http://localhost:8000/health
```

**URLs to Remember**:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health
- LGUs: http://localhost:8000/lgus
- Dashboard: http://localhost:8000/dashboard-summary

## 🎓 Learning Resources

### Understand the Architecture
1. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - 10 min overview
2. [README.md](README.md#project-structure) - File layout
3. Code comments in `main.py`, `api/routes.py`

### Learn the API
1. [API_EXAMPLES.md](API_EXAMPLES.md) - Example calls
2. http://localhost:8000/docs - Interactive docs
3. [README.md](README.md#api-endpoints) - Endpoint reference

### Understand the Database
1. [README.md](README.md#database-schema) - Schema overview
2. [database.py](database.py) - Model definitions
3. `init_data.py` - Sample data structure

### Master Deployment
1. [DEPLOYMENT.md](DEPLOYMENT.md) - All platforms
2. Choose your platform section
3. Follow step-by-step

## 📝 Notes

- **First Run**: May take 10-15 min due to AI model downloads
- **Subsequent Runs**: 30 seconds (models cached)
- **GPU**: Optional, speeds up OCR/NLP by ~10x
- **Database**: Required (PostgreSQL or MongoDB)
- **Internet**: Needed for model downloads only (first time)

## ✅ Before You Start

Check you have:
- [ ] Python 3.10+ installed
- [ ] PostgreSQL or MongoDB running
- [ ] 32 GB RAM minimum
- [ ] Internet connection (for first run)
- [ ] This project folder accessible

---

## Quick Navigation

| I want to... | File | Time |
|---|---|---|
| Start in 5 minutes | [QUICKSTART.md](QUICKSTART.md) | 5 min |
| Setup on Windows | [WINDOWS_SETUP.md](WINDOWS_SETUP.md) | 30 min |
| Use the API | [API_EXAMPLES.md](API_EXAMPLES.md) | 15 min |
| Deploy to production | [DEPLOYMENT.md](DEPLOYMENT.md) | 60 min |
| Troubleshoot errors | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | varies |
| Understand the code | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | 10 min |
| Double-check setup | [CHECKLIST.md](CHECKLIST.md) | 10 min |

---

**📖 Start with [QUICKSTART.md](QUICKSTART.md) - takes only 5 minutes!**

For questions, consult the appropriate document above. Most issues have solutions in [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

Happy coding! 🚀
