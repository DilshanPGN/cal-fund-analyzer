# 📐 Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         USER BROWSER                         │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                     index.html                          │ │
│  │                    (Presentation)                       │ │
│  └─────────────┬──────────────────────────────────────────┘ │
│                │                                             │
│  ┌─────────────▼──────────────────────────────────────────┐ │
│  │               UI Components Layer                       │ │
│  │  - ChartComponent (Visualization)                       │ │
│  │  - ModalComponent (Dialogs)                             │ │
│  │  - UIComponents (Updates)                               │ │
│  └─────────────┬──────────────────────────────────────────┘ │
│                │                                             │
│  ┌─────────────▼──────────────────────────────────────────┐ │
│  │               Main Application (app.js)                 │ │
│  │         Coordinates all frontend logic                  │ │
│  └─────────────┬──────────────────────────────────────────┘ │
│                │                                             │
│  ┌─────────────▼──────────────────────────────────────────┐ │
│  │               Services Layer                            │ │
│  │  - APIService (HTTP requests)                           │ │
│  │  - StorageService (LocalStorage)                        │ │
│  └─────────────┬──────────────────────────────────────────┘ │
│                │                                             │
│  ┌─────────────▼──────────────────────────────────────────┐ │
│  │               Utilities Layer                           │ │
│  │  - DateUtils, AnalysisUtils, Helpers                    │ │
│  └─────────────┬──────────────────────────────────────────┘ │
│                │                                             │
└────────────────┼─────────────────────────────────────────────┘
                 │ HTTP/JSON
                 │ (localhost:5000)
┌────────────────▼─────────────────────────────────────────────┐
│                       FLASK SERVER                            │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Static File Server                       │   │
│  │        (Serves frontend files)                        │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              API Routes (/api/*)                      │   │
│  │  - GET /api/funds?date=YYYY-MM-DD                     │   │
│  │  - GET /api/health                                    │   │
│  └─────────────┬────────────────────────────────────────┘   │
│                │                                              │
│  ┌─────────────▼────────────────────────────────────────┐   │
│  │              Service Layer                            │   │
│  │     CALAPIService (Business Logic)                    │   │
│  └─────────────┬────────────────────────────────────────┘   │
│                │                                              │
└────────────────┼──────────────────────────────────────────────┘
                 │ HTTP
                 │
┌────────────────▼──────────────────────────────────────────────┐
│                   EXTERNAL CAL API                             │
│         https://cal.lk/wp-admin/admin-ajax.php                 │
│           (Capital Alliance Website)                           │
└────────────────────────────────────────────────────────────────┘
```

---

## Data Flow: Fetching Fund Prices

```
┌─────────┐
│  USER   │ Clicks "Fetch Data"
└────┬────┘
     │
     ▼
┌─────────────────────────────────┐
│  1. UI Component                │
│     Captures click event        │
└────┬────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│  2. Main App (app.js)           │
│     Validates inputs            │
│     Prepares date range         │
└────┬────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│  3. Storage Service             │
│     Checks if data cached       │
│     Returns cached or null      │
└────┬────────────────────────────┘
     │
     ▼ (if not cached)
┌─────────────────────────────────┐
│  4. API Service                 │
│     Makes HTTP request          │
│     http://localhost:5000/api/  │
└────┬────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│  5. Flask Route                 │
│     Validates request           │
│     Extracts date parameter     │
└────┬────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│  6. CALAPIService               │
│     Makes external API call     │
│     Handles errors/retries      │
└────┬────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│  7. External CAL API            │
│     Returns JSON data           │
└────┬────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│  8. CALAPIService               │
│     Processes response          │
│     Returns to Flask            │
└────┬────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│  9. Flask Route                 │
│     Formats JSON response       │
│     Adds CORS headers           │
└────┬────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│  10. API Service                │
│      Receives JSON              │
│      Parses data                │
└────┬────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│  11. Storage Service            │
│      Saves to localStorage      │
└────┬────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│  12. Main App                   │
│      Updates state              │
└────┬────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│  13. Chart Component            │
│      Renders new data           │
└────┬────────────────────────────┘
     │
     ▼
┌─────────┐
│  USER   │ Sees updated chart
└─────────┘
```

---

## File Organization Map

```
PROJECT ROOT
│
├── backend/                    🖥️ SERVER SIDE
│   ├── config.py              📝 Settings (port, API URL, delays)
│   ├── server.py              🚀 Flask app factory
│   ├── requirements.txt       📦 Python packages
│   │
│   ├── services/              💼 Business Logic
│   │   └── cal_api_service.py   - Calls external API
│   │                            - Handles errors
│   │                            - Implements retry logic
│   │
│   └── routes/                🛣️ API Endpoints
│       └── api.py               - /api/funds endpoint
│                                - /api/health endpoint
│                                - Request validation
│
├── frontend/                   🌐 CLIENT SIDE
│   ├── index.html             📄 Main page
│   │
│   └── assets/
│       ├── css/
│       │   └── styles.css     🎨 Styling
│       │
│       └── js/
│           ├── config.js      ⚙️ Frontend config
│           ├── app.js         🎯 Main application
│           │
│           ├── services/      💼 Data Layer
│           │   ├── api-service.js    - HTTP requests
│           │   └── storage-service.js - LocalStorage
│           │
│           ├── components/    🎨 UI Layer
│           │   ├── chart-component.js   - Chart.js wrapper
│           │   ├── modal-component.js   - Dialog boxes
│           │   └── ui-components.js     - UI updates
│           │
│           └── utils/         🔧 Helpers
│               ├── date-utils.js        - Date functions
│               ├── analysis-utils.js    - Calculations
│               └── helpers.js           - General utils
│
├── scripts/                    🚀 Automation
│   ├── start.bat              ▶️ Windows launcher
│   ├── start.sh               ▶️ Unix launcher
│   ├── migrate.bat            📦 Windows migration
│   └── migrate.sh             📦 Unix migration
│
├── desktop/                    🖥️ Original Python App
├── docs/                       📚 Documentation
├── data/                       💾 CSV/PNG files
│
├── README.md                   📖 Main docs
├── START.md                    🚀 Quick start
├── COMPLETE.md                 ✅ Completion guide
├── PROJECT_COMPLETE.md         🎉 Full summary
├── .gitignore                  🔒 Git exclusions
└── LICENSE                     📜 MIT License
```

---

## Component Interaction Diagram

```
                    ┌─────────────┐
                    │   CONFIG    │
                    │  (Settings) │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐      ┌──────▼──────┐    ┌─────▼─────┐
   │   API   │      │   STORAGE   │    │  UTILS    │
   │ SERVICE │      │   SERVICE   │    │ (helpers) │
   └────┬────┘      └──────┬──────┘    └─────┬─────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                    ┌──────▼──────┐
                    │   MAIN APP  │
                    │   (app.js)  │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐      ┌──────▼──────┐    ┌─────▼─────┐
   │  CHART  │      │    MODAL    │    │    UI     │
   │COMPONENT│      │  COMPONENT  │    │COMPONENTS │
   └────┬────┘      └──────┬──────┘    └─────┬─────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                    ┌──────▼──────┐
                    │  index.html │
                    │    (DOM)    │
                    └─────────────┘
```

---

## Technology Stack Layers

```
┌──────────────────────────────────────────────────────┐
│                   PRESENTATION                        │
│  HTML5 │ CSS3 │ Responsive Design │ Modern UI        │
└─────────────────────┬────────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────────┐
│                  FRONTEND LOGIC                       │
│  Vanilla JavaScript │ ES6+ │ Chart.js │ LocalStorage │
└─────────────────────┬────────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────────┐
│                COMMUNICATION LAYER                    │
│  REST API │ JSON │ HTTP │ CORS │ Fetch API           │
└─────────────────────┬────────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────────┐
│                  BACKEND LOGIC                        │
│  Python 3.8+ │ Flask │ Flask-CORS │ Requests          │
└─────────────────────┬────────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────────┐
│                  EXTERNAL API                         │
│  Capital Alliance Fund Data API                       │
└───────────────────────────────────────────────────────┘
```

---

## Error Handling Flow

```
┌─────────────────────────┐
│  User Action            │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Try-Catch Block        │
└────┬────────────────┬───┘
     │                │
     │ SUCCESS        │ ERROR
     │                │
     ▼                ▼
┌─────────┐      ┌─────────────────┐
│ Process │      │ Catch Error     │
│ Data    │      └────┬────────────┘
└────┬────┘           │
     │                ▼
     │           ┌─────────────────┐
     │           │ Log to Console  │
     │           └────┬────────────┘
     │                │
     │                ▼
     │           ┌─────────────────┐
     │           │ Retry Logic?    │
     │           └────┬───────┬────┘
     │                │ YES   │ NO
     │                ▼       ▼
     │           ┌────────┐  ┌──────────────┐
     │           │ Retry  │  │ Show Error   │
     │           │ Request│  │ to User      │
     │           └────┬───┘  └──────────────┘
     │                │
     │                ▼
     │           ┌─────────────────┐
     │           │ Exponential     │
     │           │ Backoff         │
     │           └────┬────────────┘
     │                │
     └────────────────┴──────────────►
                      │
                      ▼
                ┌──────────┐
                │ Update   │
                │ UI       │
                └──────────┘
```

---

## Deployment Architecture

```
DEVELOPMENT                STAGING               PRODUCTION
    │                         │                      │
    ▼                         ▼                      ▼
localhost:5000          test.domain.com        domain.com
    │                         │                      │
    ▼                         ▼                      ▼
┌─────────┐            ┌─────────┐           ┌─────────┐
│  Flask  │            │  Flask  │           │ Gunicorn│
│  Debug  │            │ Staging │           │+ Flask  │
└─────────┘            └─────────┘           └─────────┘
    │                         │                      │
    ▼                         ▼                      ▼
 Local DB               Test Data             Production
                                                  Data
```

---

**This architecture provides:**
- ✅ Clear separation of concerns
- ✅ Easy to test each layer
- ✅ Scalable design
- ✅ Maintainable code
- ✅ Professional structure

