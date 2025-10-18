# 📊 CAL Fund Analyzer

A professional full-stack web application for tracking and analyzing Capital Alliance fund performance with clean architecture and modern design patterns.

---

## 🚀 Quick Start

### Windows
```bash
scripts\start.bat
```

### Mac/Linux
```bash
chmod +x scripts/start.sh
./scripts/start.sh
```

Then open your browser to: **http://localhost:5000**

---

## ✨ Features

- 📈 **Interactive Charts** - Visualize fund price trends with Chart.js
- 💾 **Smart Caching** - Data saved locally in browser for offline access
- 🔍 **Advanced Analysis** - Financial context with Sri Lankan economic events
- 📊 **Statistical Insights** - Returns, volatility, trend analysis
- 💾 **CSV Export** - Export data for external analysis
- 🎨 **Modern UI** - Responsive, mobile-friendly design
- 🏗️ **Clean Architecture** - Production-ready codebase with design patterns

---

## 🏗️ Architecture

### Project Structure

```
cal-fund-analyzer/
├── backend/                    # Python Flask Backend
│   ├── config.py              # Configuration settings
│   ├── server.py              # Flask app factory
│   ├── requirements.txt       # Python dependencies
│   ├── services/              # Business logic layer
│   │   ├── __init__.py
│   │   └── cal_api_service.py # External API service
│   └── routes/                # API endpoints
│       ├── __init__.py
│       └── api.py             # Fund data routes
│
├── frontend/                   # Web Frontend
│   ├── index.html             # Main HTML
│   ├── assets/
│   │   ├── css/
│   │   │   └── styles.css     # Styling
│   │   └── js/
│   │       ├── config.js      # Configuration
│   │       ├── app.js         # Main application
│   │       ├── services/      # Service layer
│   │       │   ├── api-service.js
│   │       │   └── storage-service.js
│   │       ├── components/    # UI components
│   │       │   ├── chart-component.js
│   │       │   ├── modal-component.js
│   │       │   └── ui-components.js
│   │       └── utils/         # Utilities
│   │           ├── date-utils.js
│   │           ├── analysis-utils.js
│   │           └── helpers.js
│
├── scripts/                    # Launcher scripts
│   ├── start.bat              # Windows launcher
│   ├── start.sh               # Unix/Mac launcher
│   ├── migrate.bat            # Windows migration
│   └── migrate.sh             # Unix/Mac migration
│
├── desktop/                    # Original Python desktop app
│   ├── cal_fund_extractor.py
│   ├── png_updater.py
│   └── requirements.txt
│
├── docs/                       # Documentation
│   ├── README_WEB.md
│   ├── DEPLOYMENT.md
│   └── QUICKSTART_WEB.md
│
├── data/                       # Data files (gitignored)
│   ├── *.csv
│   └── *.png
│
├── README.md                   # This file
├── .gitignore                  # Git ignore rules
└── LICENSE                     # MIT License
```

---

## 🎯 Design Patterns Implemented

### Backend (Python/Flask)
- ✅ **Factory Pattern** - Application creation (`create_app()`)
- ✅ **Service Pattern** - Business logic separation (`CALAPIService`)
- ✅ **Controller Pattern** - Request handling (API routes)
- ✅ **Configuration Pattern** - Centralized settings (`Config`)
- ✅ **Dependency Injection** - Loose coupling between layers

### Frontend (JavaScript)
- ✅ **Service Pattern** - API and Storage services
- ✅ **Component Pattern** - Reusable UI components
- ✅ **Module Pattern** - Encapsulated functionality
- ✅ **Singleton Pattern** - Global configuration
- ✅ **Strategy Pattern** - Multiple analysis strategies

---

## 🔧 Installation

### Prerequisites
- Python 3.8+ 
- Modern web browser (Chrome, Firefox, Edge, Safari)
- Internet connection (for fetching fund data)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/cal-fund-analyzer.git
   cd cal-fund-analyzer
   ```

2. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   # From project root:
   scripts/start.bat    # Windows
   ./scripts/start.sh   # Mac/Linux
   ```

4. **Open in browser**
   ```
   http://localhost:5000
   ```

---

## 📖 Usage Guide

### Fetching Fund Data

1. **Select a Fund** from the dropdown menu
2. **Choose Date Range** (or use defaults)
3. Click **"Fetch New Data"**
4. Wait for data to load (progress shown)
5. View the interactive chart

### Analyzing Data

The application provides multiple analysis presets:

- **Current View** - Analyze the visible chart range
- **Crisis Period** - 2022 economic crisis analysis
- **Recovery Period** - 2023 recovery analysis  
- **Recent 6 Months** - Latest performance

Each analysis includes:
- Price statistics (min, max, average)
- Total return percentage
- Volatility metrics
- Trend analysis
- Contextual economic events
- AI-generated insights

### Exporting Data

Click **"Export to CSV"** to download the current fund's data for use in Excel, Google Sheets, or other analysis tools.

### Managing Cache

- **View Storage** - See how much browser storage is used
- **Clear Cache** - Remove all cached data to free up space or force refresh

---

## 🌐 Deployment

### GitHub Pages (Frontend Only)

> **Note:** GitHub Pages is static hosting, so the Python backend won't work. You'll need to deploy the backend separately (e.g., Heroku, Render, PythonAnywhere).

1. Build static assets
2. Push to GitHub
3. Enable GitHub Pages in settings
4. Update `config.js` to point to your deployed backend

See `docs/DEPLOYMENT.md` for detailed instructions.

### Full-Stack Deployment

**Backend Options:**
- Heroku (Free tier available)
- Render (Free tier available)
- PythonAnywhere
- AWS EC2/EB
- Google Cloud Run

**Frontend Options:**
- Serve from Flask backend (simplest)
- Separate deployment to Netlify/Vercel
- GitHub Pages (requires separate backend)

---

## 🧪 Development

### Running in Development Mode

```bash
# Backend only
cd backend
python server.py

# Access at http://localhost:5000
```

### Code Quality

The codebase follows industry best practices:

- ✅ **Clean Code** - Self-documenting, meaningful names
- ✅ **SOLID Principles** - Single responsibility, open/closed, etc.
- ✅ **DRY** - Don't repeat yourself
- ✅ **Separation of Concerns** - Clear layer boundaries
- ✅ **Error Handling** - Comprehensive try-catch blocks
- ✅ **Documentation** - JSDoc and Python docstrings
- ✅ **Type Hints** - Python type annotations

### Project Structure Philosophy

```
┌─────────────── PRESENTATION LAYER ───────────────┐
│  HTML + CSS + UI Components                      │
│  (What the user sees and interacts with)         │
└────────────────────┬──────────────────────────────┘
                     │
┌────────────────────▼──────────────────────────────┐
│  APPLICATION LAYER (Frontend Services)            │
│  API Service, Storage Service, Utils              │
│  (Handles business logic and state)               │
└────────────────────┬──────────────────────────────┘
                     │ HTTP/JSON
┌────────────────────▼──────────────────────────────┐
│  API LAYER (Backend Routes)                       │
│  Flask endpoints, request validation              │
│  (Accepts requests, returns responses)            │
└────────────────────┬──────────────────────────────┘
                     │
┌────────────────────▼──────────────────────────────┐
│  SERVICE LAYER (Backend Services)                 │
│  CALAPIService, business logic                    │
│  (Interacts with external APIs)                   │
└────────────────────┬──────────────────────────────┘
                     │ HTTP
┌────────────────────▼──────────────────────────────┐
│  EXTERNAL API (CAL Website)                       │
│  https://cal.lk/wp-admin/admin-ajax.php           │
└───────────────────────────────────────────────────┘
```

---

## 🔐 Security

- ✅ CORS properly configured
- ✅ Input validation on all endpoints
- ✅ No sensitive data stored
- ✅ Local storage only for cached fund data
- ✅ No authentication required (public data)

---

## 📊 Technology Stack

### Backend
- **Flask** 2.3.2 - Python web framework
- **Flask-CORS** 4.0.0 - Cross-origin resource sharing
- **Requests** 2.31.0 - HTTP library

### Frontend
- **Chart.js** 4.4.0 - Interactive charts
- **Chart.js Date Adapter** 3.0.0 - Time series support
- **Vanilla JavaScript** - No heavy frameworks
- **CSS3** - Modern responsive design
- **HTML5** - Semantic markup

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- **Python:** Follow PEP 8
- **JavaScript:** Use ES6+, camelCase naming
- **Comments:** Document complex logic
- **Tests:** Add tests for new features

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Capital Alliance for providing the public API
- Chart.js team for the excellent charting library
- The open-source community

---

## 📞 Support

**Issues:** https://github.com/yourusername/cal-fund-analyzer/issues

**Documentation:** See `docs/` folder for detailed guides

**Contact:** [Your contact information]

---

## 🗺️ Roadmap

- [ ] Add more advanced technical indicators (RSI, MACD)
- [ ] Implement fund comparison feature
- [ ] Add predictive analytics with ML
- [ ] Create mobile app version
- [ ] Add real-time price alerts
- [ ] Implement portfolio tracking
- [ ] Add multi-language support
- [ ] Create API for third-party integrations

---

## 📈 Version History

### v2.0.0 (Current) - Clean Architecture
- Complete refactoring with design patterns
- Modular frontend and backend
- Comprehensive documentation
- Production-ready code

### v1.0.0 - Initial Web Version
- Basic web application
- Chart visualization
- Data caching
- CSV export

### v0.1.0 - Desktop Version
- Python desktop app with Tkinter
- Matplotlib charts
- CSV data extraction

---

**Built with ❤️ for the Sri Lankan investment community**
