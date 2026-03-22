# SipatGov

**Civic-tech transparency platform for tracking Philippine LGU budgets, promises, and project implementations.**

> *"Taon-taon tayong nabibigo sa mga pangakong nabibitawan tuwing eleksyon.*
> *Di natin alam kung may nangyari nga ba, o kung naka-post man, hindi naman naiintindihan."*
>
> SipatGov exists to change that.

---

## Project Description

### What is SipatGov?

**SipatGov** (from the Filipino word *sipat* — to observe, to check, to scrutinize) is a civic-technology platform that empowers Filipino citizens to hold their Local Government Units (LGUs) accountable. It is a complete system that autonomously collects, processes, and presents government data in a way that ordinary citizens can understand and act upon.

The platform addresses a fundamental problem in Philippine governance: **the gap between what officials promise and what they deliver**. Every election cycle, candidates make commitments — infrastructure projects, budget allocations, social programs. But once elected, there is no accessible, centralized system for citizens to track whether those promises were kept, how public funds were spent, or whether projects were actually completed.

### The Problem

1. **Inaccessible Data** — Government procurement records (PhilGEPS), budget documents (DBM), audit reports (COA), and FOI disclosures are scattered across multiple portals, buried in PDFs, and written in bureaucratic language.

2. **No Accountability Tracking** — There is no system that cross-references campaign promises against actual budget allocations, awarded contracts, and completed projects.

3. **Citizen Disengagement** — Without understandable data, citizens cannot meaningfully participate in governance oversight, leading to a cycle of broken promises and voter frustration.

4. **Manual Monitoring is Impossible** — A single LGU might publish hundreds of procurement notices, budget documents, and project updates per year. No citizen or watchdog group can manually track all of this.

### The Solution

SipatGov solves this through two integrated systems:

#### GovernanceGhost (The AI Auditing Engine)

An autonomous backend service that operates 24/7 to:

- **Crawl** four major government portals (PhilGEPS, DBM, COA, e-FOI) on configurable schedules
- **Extract** text from scanned PDFs using AWS Textract OCR
- **Understand** unstructured government documents using Claude AI, converting them into structured data (budget amounts, contractor names, project timelines, audit findings)
- **Validate** extracted data using a 21-rule validation pipeline with Jaccard similarity deduplication and AI verification for ambiguous cases
- **Store** everything in a normalized PostgreSQL database with Row-Level Security

The system requires zero human intervention once configured. It discovers new documents, downloads PDFs, extracts structured data, validates quality, and stores results — all autonomously.

#### SipatGov App (The Citizen Interface)

A mobile application (Android) that presents government data in an accessible, visual format:

- **Interactive Map** — OpenStreetMap-based visualization of LGU projects and budget allocations by region, with color-coded transparency scores
- **Promise Tracker** — Every official's campaign commitments tracked against actual delivery, with evidence links to source documents (Kept / Broken / In Progress / Pending)
- **Project Monitor** — Real-time status of infrastructure and government projects with budget utilization, contractor info, and timeline tracking
- **Community Reports** — Citizens can submit concerns, corruption tips, progress updates, and delay reports with upvoting to surface the most important issues
- **Accountability Dashboard** — Per-LGU and per-official scorecards with historical trends

The app supports **English and Tagalog**, works **offline** with cached data, and gracefully degrades when the backend is unreachable by falling back to locally stored mock/cached data.

### Who is it for?

| User | Use Case |
|------|----------|
| **Citizens** | Check if their LGU is keeping promises, report concerns, view how taxes are spent |
| **Journalists** | Access structured government data for investigative reporting |
| **Civil Society / NGOs** | Monitor LGU compliance, track budget utilization across regions |
| **Researchers** | Analyze governance patterns, procurement trends, audit findings |
| **Government Watchdogs** | Cross-reference promises vs. actual spending vs. audit results |

### Key Features

| Feature | Description |
|---------|-------------|
| **Autonomous Data Collection** | 4 spiders crawl PhilGEPS, DBM, COA, e-FOI on scheduled intervals |
| **AI-Powered Extraction** | Claude API converts messy government PDFs into structured, searchable data |
| **ML Validation Pipeline** | 21 rule-based checks + AI verification ensure data quality (auto-approve > 0.8, flag 0.3-0.8, reject < 0.3) |
| **Promise Accountability** | Campaign commitments tracked with evidence linking to source documents |
| **Transparency Scoring** | Each LGU gets a computed transparency score based on data availability, promise fulfillment, and audit results |
| **Community Reporting** | Citizens can file reports with upvoting to surface critical issues |
| **Bilingual Support** | Full English and Tagalog translations (100+ keys) |
| **Offline-First Design** | React Query persistence + AsyncStorage ensures the app works without connectivity |
| **Open Data** | All government data is public record — the platform just makes it accessible |

### Data Pipeline

```
Government Portals          AI Processing           Citizen App
─────────────────          ──────────────           ───────────
PhilGEPS (bids) ─┐                                 ┌─ Dashboard
DBM (budgets) ───┤  Scrapy    Textract   Claude    ├─ Promise Tracker
COA (audits) ────┼──────►──────►────────►──────►───├─ Project Monitor
e-FOI (FOI) ─────┘  Crawl     OCR       NLP       ├─ Community Reports
                     │         │         │         └─ Accountability
                     ▼         ▼         ▼
              Validation Pipeline (21 rules)
                     │
                     ▼
              PostgreSQL (Supabase)
              14 tables, RLS, materialized views
```

### Design Philosophy

The app's visual identity draws from the **Philippine flag colors** — navy blue, red, and gold — embodied in the SipatGov shield emblem (an eye within a shield, symbolizing vigilant civic observation). The design transitions from a **dark, bold onboarding flow** (establishing the app's serious civic purpose) to a **clean, light dashboard** (prioritizing data readability and accessibility).

The taglines reflect the app's mission:
- *"Buksan ang mga mata"* — Open your eyes
- *"Maging Mapagmasid"* — Be observant
- *"Ipaglaban ang Tama"* — Fight for what's right
- *"Sipatin ang Gobyerno"* — Scrutinize the government

### Project Status

This is an actively developed civic-tech project. Current implementation includes:

- ✅ Full mobile app with 5 screens (Dashboard, Sipat, Projects, Reports, Profile)
- ✅ Multi-step onboarding flow with bilingual support
- ✅ 4 autonomous web spiders targeting major PH government portals
- ✅ PDF processing pipeline (OCR + NLP) with mock mode for development
- ✅ Data validation pipeline with AI verification
- ✅ Auto-scheduling system for crawl jobs
- ✅ 14-table PostgreSQL schema with RLS and materialized views
- ✅ 12 REST API endpoints with input validation and error handling
- ✅ React Query integration with offline-first data persistence
- ✅ Design system (typography, spacing, colors) aligned with Philippine flag identity

---

## Architecture Overview

```
SipatGov/
├── Frontend (React Native + Expo)     ← Citizen-facing mobile app
├── Backend (FastAPI + Python)         ← GovernanceGhost AI auditing engine
├── Database (Supabase/PostgreSQL)     ← Structured government data
└── Crawler (Scrapy)                   ← Autonomous web scraping pipeline
```

### System Flow

```
┌─────────────────────────────────────────────────────────────┐
│  GovernanceGhost (Backend)                                  │
│                                                             │
│  PhilGEPS ─┐                                                │
│  DBM ──────┤    Scrapy      AWS         Claude AI           │
│  COA ──────┼──► Spiders ──► Textract ──► Extractor ──► DB   │
│  e-FOI ────┘    (4)         (OCR)       (NLP)               │
│                                                             │
│  Auto-Scheduler ──► Validation Pipeline ──► PostgreSQL      │
└──────────────────────────┬──────────────────────────────────┘
                           │ FastAPI (REST)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  SipatGov App (Frontend)                                    │
│                                                             │
│  Onboarding ──► Dashboard ──► Accountability ──► Projects   │
│                     │              │                  │      │
│                  Map View    Promise Tracker    Project List │
│                     │              │                  │      │
│                 LGU Scores   Kept/Broken       Status/Budget│
│                                                             │
│  Reports ──► Community Tips ──► Upvotes                     │
│  Profile ──► Settings ──► Region Selector                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Mobile App** | React Native + Expo SDK 54 | Cross-platform Android/iOS |
| **Navigation** | Expo Router (file-based) | Tab + stack navigation |
| **State** | Zustand + React Query | Client state + server cache |
| **API Client** | Axios + React Query hooks | Type-safe API integration |
| **Backend API** | FastAPI + Pydantic | REST API with validation |
| **Database** | PostgreSQL (Supabase) | Structured data + RLS |
| **ORM** | SQLAlchemy 2.0 (async) | Database models |
| **Crawler** | Scrapy | Government portal scraping |
| **OCR** | AWS Textract | PDF text extraction |
| **NLP** | Claude API (Anthropic) | Structured data extraction |
| **Auth** | JWT + Supabase Auth | User authentication |
| **i18n** | Custom hooks | English + Tagalog |

---

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.11+
- Android Studio (for emulator)
- Supabase project (or local PostgreSQL)

### 1. Install Dependencies

```bash
# Frontend
cd C:\JC\SipatGov
npm install

# Backend
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Backend: Copy and edit .env
cd backend
cp .env.example .env
# Fill in: DATABASE_URL, SUPABASE_URL, SUPABASE_ANON_KEY
```

```bash
# Frontend: Create .env.local at project root
EXPO_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

### 3. Apply Database Migrations

Run these SQL files in order against your Supabase project:

```bash
backend/supabase/migrations/001_initial_schema.sql
backend/supabase/migrations/002_rls_and_views.sql
backend/supabase/migrations/003_scraping_schedules.sql
backend/supabase/seed.sql                              # Optional: seed data
```

### 4. Run Everything

```bash
# Both frontend + backend together
npm run dev

# Or individually:
npm run dev:app     # Expo dev server
npm run dev:api     # FastAPI backend
```

### 5. Native Build (for maps + WebView)

```bash
npx expo run:android    # First build ~20min, subsequent ~2min
```

---

## Project Structure

### Frontend (React Native)

```
app/
├── _layout.tsx                          # Root layout + QueryClient provider
├── index.tsx                            # Splash screen → onboarding/dashboard
├── language-select.tsx                  # Language picker (EN/TL)
├── (onboarding)/
│   ├── _layout.tsx                      # Onboarding stack layout
│   └── index.tsx                        # Swipeable onboarding flow
└── (tabs)/
    ├── _layout.tsx                      # Tab navigator (5 tabs)
    ├── index.tsx                        # Dashboard: map + LGU scores + stats
    ├── accountability.tsx               # Promise tracker: kept/broken/pending
    ├── projects.tsx                     # Project list: search + filter + cards
    ├── reports.tsx                      # Community reports: submit + upvote
    └── profile.tsx                      # Settings: region, language, logout

components/
├── ShieldLogo.tsx                       # SVG shield emblem
├── haptic-tab.tsx                       # Tab with haptic feedback
├── accountability/
│   ├── PromiseListItem.tsx              # Promise card with status badge
│   ├── PromiseSummaryCard.tsx           # Stats summary (kept/broken/etc)
│   └── StatusBadge.tsx                  # Color-coded status indicator
├── dashboard/
│   ├── CTAButton.tsx                    # Gold "OBSERVE THE GOVERNMENT" button
│   ├── DashboardHeader.tsx              # Date/time header (auto-updates)
│   └── QuickStats.tsx                   # Circular progress indicators
├── map/
│   └── SafeMapView.tsx                  # OpenLayers map or fallback grid
├── onboarding/
│   ├── DotIndicator.tsx                 # Page indicator dots
│   └── OnboardingCard.tsx               # Onboarding slide with SVG arches
├── projects/
│   ├── ProjectCard.tsx                  # Project card: budget, progress, status
│   └── ProjectFilters.tsx               # Horizontal filter chips
└── reports/
    ├── ReportCard.tsx                   # Report card with upvote button
    ├── ReportForm.tsx                   # Modal form (React Hook Form + Zod)
    └── ReportTypeChip.tsx               # Color-coded report type badge

constants/
├── api.ts                               # API base URL + endpoint paths
├── regions.ts                           # 17 Philippine regions (PSGC codes)
├── status.ts                            # Status labels, colors, icons
└── theme.ts                             # SipatColors, Typography, Spacing, Radius

hooks/
├── use-color-scheme.ts                  # System dark/light mode
├── use-language.ts                      # Language toggle (EN ↔ TL)
├── use-onboarding.ts                    # Onboarding completion state
├── use-theme-color.ts                   # Themed color values
└── api/
    ├── index.ts                         # Barrel export
    ├── query-keys.ts                    # React Query key factory
    ├── use-dashboard.ts                 # Dashboard data (mock fallback)
    ├── use-lgus.ts                      # LGU list + map markers
    ├── use-projects.ts                  # Projects with server-side filter
    ├── use-promises.ts                  # Promises + stats
    └── use-reports.ts                   # Reports + create/upvote mutations

services/
├── api-client.ts                        # Axios instance + JWT interceptors
├── api.ts                               # 16 API functions (typed)
├── dashboard-service.ts                 # Dashboard aggregation
├── lgu-service.ts                       # LGU data service
├── promise-service.ts                   # Promise tracking service
└── supabase.ts                          # Supabase client init

store/
├── index.ts                             # Barrel export
├── auth-store.ts                        # Auth state (JWT, user, error)
├── dashboard-store.ts                   # Dashboard preferences
├── language-store.ts                    # Language persistence
├── map-store.ts                         # Map zoom/center/selection
└── report-store.ts                      # Report drafts

types/
├── api.ts                               # AuthResponse, CreateReportInput, etc.
└── models.ts                            # LGU, Project, Promise, Report, etc.

utils/
├── format.ts                            # formatPeso, formatDate, timeAgo
├── i18n.ts                              # i18n setup
├── mock-data.ts                         # 15 projects, 12 promises, 12 reports
├── storage.ts                           # AsyncStorage helpers (NaN-safe)
└── translations/
    ├── en.ts                            # English (6 sections, 100+ keys)
    └── tl.ts                            # Tagalog (matching keys)
```

### Backend (Python/FastAPI)

```
backend/
├── .env                                 # Environment variables
├── requirements.txt                     # 16 Python packages
├── pyproject.toml                       # Project metadata + tool config
├── scrapy.cfg                           # Scrapy project config

├── app/
│   ├── main.py                          # FastAPI app + CORS + size limit
│   ├── config.py                        # Pydantic Settings (env-based)
│   ├── database.py                      # Async SQLAlchemy engine + pool
│   │
│   ├── api/v1/
│   │   ├── router.py                    # All endpoint routers mounted
│   │   ├── deps.py                      # Dependency injection (get_db, auth)
│   │   └── endpoints/
│   │       ├── auth.py                  # POST /login, /register, /refresh
│   │       ├── budgets.py               # GET /budgets, /budgets/summary
│   │       ├── crawler.py               # POST /trigger, GET /jobs/{id}
│   │       ├── dashboard.py             # GET /dashboard, /dashboard/{lgu}
│   │       ├── documents.py             # GET /documents, /documents/{id}
│   │       ├── lgus.py                  # GET /lgus, /lgus/{id}, /lgus/map
│   │       ├── projects.py              # GET /projects, /projects/{id}
│   │       ├── promises.py              # GET /promises, /promises/stats
│   │       ├── regions.py               # GET /regions
│   │       ├── reports.py               # GET/POST /reports, upvote
│   │       ├── scheduler.py             # GET/PUT schedules, POST run, health
│   │       └── search.py                # GET /search?q=
│   │
│   ├── models/                          # SQLAlchemy ORM (14 tables)
│   │   ├── base.py                      # DeclarativeBase + mixins
│   │   ├── user.py                      # Users (citizen/admin/moderator)
│   │   ├── region.py                    # 17 Philippine regions
│   │   ├── province.py                  # Provinces (FK → regions)
│   │   ├── lgu.py                       # LGUs (coordinates, scores)
│   │   ├── official.py                  # Elected officials
│   │   ├── project.py                   # Infrastructure projects
│   │   ├── promise.py                   # Campaign promises
│   │   ├── budget.py                    # Budget allocations (GAA/NEP)
│   │   ├── document.py                  # Crawled PDFs/documents
│   │   ├── community_report.py          # Citizen reports
│   │   ├── crawl_job.py                 # Spider run tracking
│   │   └── scraping_schedule.py         # Auto-schedule config
│   │
│   ├── schemas/                         # Pydantic response models
│   │   ├── common.py                    # HealthResponse, PaginatedParams
│   │   ├── lgu.py                       # LGUListItem, LGUMapMarker
│   │   ├── promise.py                   # PromiseListItem, PromiseStats
│   │   └── report.py                    # CreateReportRequest (validated)
│   │
│   └── utils/
│       └── security.py                  # JWT encode/decode, password hash

├── crawler/governance_ghost/
│   ├── items.py                         # 5 item types (Bid, Award, Budget, Audit, FOI)
│   ├── middlewares.py                   # RateLimit + ProxyRotation + RetryMiddleware
│   ├── settings.py                      # AutoThrottle, pipelines, user-agents
│   ├── pipelines.py                     # 4 pipelines: Dedup → Validate → PDF → DB
│   │
│   ├── spiders/
│   │   ├── philgeps_spider.py           # PhilGEPS: bids, awards, contracts
│   │   ├── dbm_spider.py               # DBM: GAA, NEP, LGU budgets
│   │   ├── coa_spider.py               # COA: annual audit reports
│   │   └── efoi_spider.py              # e-FOI: FOI requests, compliance
│   │
│   ├── pdf_pipeline/
│   │   ├── textract_processor.py        # AWS Textract OCR (mock-able)
│   │   ├── claude_extractor.py          # Claude AI NLP (mock-able)
│   │   ├── fallback_processor.py        # PyMuPDF/pdfplumber fallback
│   │   └── mock_data.py                 # Realistic mock OCR/NLP outputs
│   │
│   ├── validation/
│   │   ├── models.py                    # ValidationResult, ScrapingSchedule
│   │   └── data_validator.py            # 21 rule checks + Jaccard dedup + Claude verify
│   │
│   └── scheduler/
│       └── auto_scheduler.py            # Cron engine + health reporting

├── supabase/
│   ├── migrations/
│   │   ├── 001_initial_schema.sql       # 14 tables, indexes, triggers (368 lines)
│   │   ├── 002_rls_and_views.sql        # RLS policies, materialized views (271 lines)
│   │   └── 003_scraping_schedules.sql   # Schedule table + seed data
│   └── seed.sql                         # 30 LGUs, 22 promises, 15 projects (584 lines)

├── tests/
│   ├── conftest.py                      # Pytest fixtures
│   ├── test_api/                        # API endpoint tests
│   ├── test_crawler/                    # Spider tests
│   └── test_services/                   # Service layer tests

└── alembic/                             # SQLAlchemy migrations
    └── versions/
```

---

## Database Schema

```
regions (17)
  └── provinces
       └── lgus (30+)
            ├── officials
            ├── documents (crawled PDFs)
            ├── budget_allocations
            ├── projects (PhilGEPS-linked)
            ├── promises
            │    └── promise_evidence
            └── community_reports
                 ├── report_attachments
                 └── report_upvotes

users (citizen/admin/moderator)
crawl_jobs (spider run tracking)
scraping_schedules (auto-scheduler config)

Views:
  mv_promise_stats    ← materialized (per-LGU fulfillment rates)
  vw_budget_summary   ← budget utilization per LGU/year
  vw_official_scorecard ← per-official promise stats
```

---

## Data Sources

| Source | Spider | Schedule | Data |
|--------|--------|----------|------|
| **PhilGEPS** | `philgeps` | Daily 2 AM | Public bids, awarded contracts |
| **DBM** | `dbm` | Weekly Mon 3 AM | GAA, NEP, LGU budget allocations |
| **COA** | `coa` | Monthly 1st 4 AM | Annual Audit Reports, disallowances |
| **e-FOI** | `efoi` | Weekly Wed 5 AM | FOI requests, compliance rates |

### Crawl Pipeline

```
Spider Output → DuplicateFilter → ValidationPipeline → PDFDownload → DatabasePipeline
                  (SHA-256)        (21 rules + AI)      (S3/local)     (PostgreSQL)
```

**Validation Pipeline:**
- Score 0.0-1.0 per item
- Auto-approve > 0.8 | Flag 0.3-0.8 | Reject < 0.3
- Claude AI verification for ambiguous items (0.4-0.7)
- Jaccard similarity dedup (500-item window)

---

## API Endpoints

```
Base: /api/v1

Auth
  POST   /auth/login              # JWT login
  POST   /auth/register           # User registration
  POST   /auth/refresh            # Token refresh

LGUs
  GET    /lgus                    # List with search/filter
  GET    /lgus/{id}               # Detail + projects + promises
  GET    /lgus/map-markers        # Coordinates + scores for map

Promises
  GET    /promises                # List with status/LGU filter
  GET    /promises/{id}           # Detail + evidence
  GET    /promises/stats          # Kept/broken/pending counts

Projects
  GET    /projects                # List with status/LGU filter
  GET    /projects/{id}           # Detail + budget + timeline

Budgets
  GET    /budgets                 # Allocations with filters
  GET    /budgets/summary         # Utilization by LGU/year

Reports
  GET    /reports                 # Community reports list
  POST   /reports                 # Submit new report
  POST   /reports/{id}/upvote     # Upvote a report

Dashboard
  GET    /dashboard               # Aggregate stats
  GET    /dashboard/{lgu_id}      # Per-LGU dashboard

Crawler
  POST   /crawler/trigger         # Trigger spider run
  GET    /crawler/jobs/{id}       # Check crawl status

Scheduler
  GET    /scheduler/schedules     # List all schedules
  PUT    /scheduler/schedules/{s} # Update schedule
  POST   /scheduler/schedules/{s}/run  # Manual trigger
  GET    /scheduler/health        # Overall health report
  GET    /scheduler/validation-stats   # Quality metrics

Documents
  GET    /documents               # Crawled documents list
  GET    /documents/{id}          # Document detail + extracted data

Regions
  GET    /regions                 # 17 Philippine regions

Search
  GET    /search?q=               # Full-text search
```

---

## Design System

### Brand Colors
| Token | Hex | Usage |
|-------|-----|-------|
| `navy` | `#0A0E1A` | Primary backgrounds, headings |
| `red` | `#CE1126` | Philippine flag red, alerts |
| `blue` | `#0038A8` | Philippine flag blue, accents |
| `gold` | `#D4A843` | CTAs, active states, badges |

### Typography Scale
| Token | Size | Weight | Usage |
|-------|------|--------|-------|
| `h1` | 28px | Bold | Page titles |
| `h2` | 22px | Bold | Section headers |
| `h3` | 18px | SemiBold | Card titles |
| `body` | 15px | Regular | Content text |
| `bodySmall` | 13px | Regular | Secondary text |
| `caption` | 11px | Regular | Labels, metadata |
| `button` | 16px | Bold | Button text |
| `tabLabel` | 11px | Medium | Tab bar labels |

### Spacing Scale
| Token | Value | Usage |
|-------|-------|-------|
| `xs` | 4px | Tight gaps |
| `sm` | 8px | Component padding |
| `md` | 12px | Card padding |
| `lg` | 16px | Section gaps |
| `xl` | 20px | Page padding |
| `xxl` | 24px | Large gaps |
| `section` | 32px | Section separation |

---

## i18n Support

The app supports **English** and **Tagalog** with 100+ translation keys across 6 sections:

| Section | Keys | Example (EN → TL) |
|---------|------|--------------------|
| `tabs` | 5 | "Home" → "Mapa" |
| `onboarding` | 10 | "Welcome to" → "Buksan ang mga mata" |
| `accountability` | 15 | "Promises Kept" → "Mga Pangakong Natupad" |
| `projects` | 13 | "Budget" → "Badyet" |
| `reports` | 24 | "New Report" → "Bagong Ulat" |
| `profile` | 21 | "Logout" → "Mag-log Out" |

---

## Running Spiders

```bash
cd backend

# Individual spiders
scrapy crawl philgeps
scrapy crawl dbm
scrapy crawl coa
scrapy crawl efoi

# Via API (requires backend running)
curl -X POST http://localhost:8000/api/v1/crawler/trigger \
  -H "Content-Type: application/json" \
  -d '{"spider": "philgeps"}'

# Check scheduler health
curl http://localhost:8000/api/v1/scheduler/health
```

---

## File Counts

| Area | Files | Lines (approx) |
|------|-------|-----------------|
| App screens | 8 | ~2,500 |
| Components | 14 | ~2,800 |
| Hooks | 11 | ~500 |
| Services | 6 | ~400 |
| Stores | 6 | ~300 |
| Utils + i18n | 6 | ~1,200 |
| Backend API | 14 | ~1,500 |
| Models | 14 | ~700 |
| Spiders | 4 | ~1,200 |
| Pipelines | 5 | ~800 |
| Validation | 2 | ~400 |
| SQL migrations | 4 | ~1,200 |
| **Total** | **~94** | **~13,500** |

---

## License

This project is for civic transparency purposes. Built for the Filipino people.

**Sipatin ang Gobyerno.**
