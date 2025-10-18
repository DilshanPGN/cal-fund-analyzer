# CAL Fund Analyzer - Web Edition 🌐

A modern, browser-based application for analyzing Capital Alliance (CAL) unit trust fund performance. This web application runs entirely in your browser, stores data locally, and can be hosted on GitHub Pages.

![Web Application](https://img.shields.io/badge/Web-Application-blue)
![GitHub Pages](https://img.shields.io/badge/Hosted%20on-GitHub%20Pages-green)
![No Backend](https://img.shields.io/badge/Backend-Not%20Required-orange)

## 🚀 Live Demo

**Access the app here:** `https://YOUR-USERNAME.github.io/cal-fund-analyzer/`

*(Replace with your actual GitHub Pages URL after deployment)*

## ✨ Features

### 📊 **Interactive Data Visualization**
- Real-time chart updates with Chart.js
- Zoom and pan capabilities
- Responsive design for all devices
- Professional-quality graphs

### 💾 **Local Data Storage**
- All data stored in browser's localStorage
- Works offline after initial data fetch
- No backend server required
- Fast data access

### 🔄 **Smart Data Management**
- Fetch historical fund prices from CAL API
- Automatic data caching
- Refresh capability for latest prices
- Export data to CSV

### 📈 **Advanced Analysis**
- Current view analysis
- Crisis period analysis (2022)
- Recovery period analysis (2023)
- Recent 6 months performance
- AI-powered insights

### 🎨 **Modern UI/UX**
- Clean, intuitive interface
- Mobile-responsive design
- Dark mode support (coming soon)
- Accessibility features

## 🛠️ Technology Stack

- **Frontend:** Pure HTML5, CSS3, JavaScript (ES6+)
- **Charting:** Chart.js v4
- **Storage:** Browser localStorage
- **API:** Capital Alliance REST API
- **Hosting:** GitHub Pages (static hosting)

## 📋 How to Use

### 1️⃣ **Select a Fund**
- Open the application in your browser
- Choose a fund from the dropdown menu
- The app will show cached data if available

### 2️⃣ **Fetch Data**
- Set your desired date range (or use defaults)
- Click "Fetch New Data" to download prices
- Data is automatically saved to your browser

### 3️⃣ **Analyze Performance**
- Use the interactive chart to explore trends
- Click analysis buttons for detailed insights
- Export data to CSV for external analysis

### 4️⃣ **Manage Data**
- Refresh to get latest prices
- Clear cache to start fresh
- View storage usage

## 🌐 Deployment on GitHub Pages

### Option 1: Deploy Your Own Copy

1. **Fork or Clone the Repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/cal-fund-analyzer.git
   cd cal-fund-analyzer
   ```

2. **Enable GitHub Pages**
   - Go to your repository settings
   - Navigate to "Pages" section
   - Select source: `main` branch, `/` (root)
   - Click "Save"

3. **Access Your App**
   - Wait a few minutes for deployment
   - Visit: `https://YOUR-USERNAME.github.io/cal-fund-analyzer/`

### Option 2: Use GitHub Desktop

1. Create a new repository
2. Add the web files (index.html, app.js, styles.css)
3. Commit and push
4. Enable GitHub Pages in settings
5. Access your deployed app

### Option 3: Direct Upload

1. Go to GitHub.com
2. Create a new repository
3. Upload files: `index.html`, `app.js`, `styles.css`
4. Enable GitHub Pages
5. Done!

## 📱 Mobile Support

The web app is fully responsive and works great on:
- 📱 Smartphones (iOS, Android)
- 📟 Tablets (iPad, Android tablets)
- 💻 Desktops (Windows, Mac, Linux)
- 🖥️ Large displays (4K monitors)

## 🔒 Privacy & Security

### Your Data is Safe
- ✅ All data stored **locally** in your browser
- ✅ No server-side storage
- ✅ No user tracking
- ✅ No cookies
- ✅ Works offline after initial fetch

### API Usage
- The app fetches data from CAL's public API
- Implements rate limiting (500ms delay between requests)
- Respects server resources
- No API key required

## 💡 Tips & Tricks

### Faster Data Loading
- Start with recent date ranges (last 6 months)
- Gradually expand to historical data
- Use the cache effectively

### Better Analysis
- Zoom into specific periods for detailed view
- Use "Analyze Current View" after zooming
- Export data for Excel analysis

### Storage Management
- Each fund's data is stored separately
- Clear cache if you encounter issues
- Browser typically allows 5-10MB storage

## 🆚 Web vs Desktop Version

| Feature | Web App | Desktop App (Python) |
|---------|---------|---------------------|
| Installation | None required | Python + packages |
| Platform | Any browser | Windows/Mac/Linux |
| Data Storage | localStorage | CSV files |
| Offline Use | After initial fetch | Full offline |
| Updates | Auto (GitHub Pages) | Manual |
| Sharing | Share URL | Share files |

## 🐛 Troubleshooting

### Data Not Loading?
- Check your internet connection
- Verify the CAL API is accessible
- Clear browser cache and try again
- Check browser console for errors

### Chart Not Displaying?
- Ensure JavaScript is enabled
- Try a different browser
- Clear localStorage and refresh

### Slow Performance?
- Large date ranges take time to fetch
- Use smaller date ranges initially
- Clear old cached data

### Storage Full?
- Each browser has storage limits (~5-10MB)
- Clear cache for unused funds
- Use Export feature before clearing

## 🔧 Advanced Configuration

### Modify API Delay
Edit `app.js` line with delay setting:
```javascript
await this.delay(500); // Change 500 to desired milliseconds
```

### Change Date Sampling
Modify `generateDateRange()` function to sample different dates.

### Customize Appearance
Edit `styles.css` to change colors, fonts, and layout.

## 📊 Data Format

### LocalStorage Structure
```javascript
{
  "cal_fund_FundName": {
    "fundName": "Capital Alliance Fund",
    "prices": {
      "2024-01-01": 125.50,
      "2024-01-15": 126.75
    },
    "lastUpdated": "2024-10-18T12:00:00Z"
  }
}
```

### CSV Export Format
```csv
Date,OLD_PRICE
2024-01-01,125.50
2024-01-15,126.75
```

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational and personal use. Please respect CAL's API terms of service and don't abuse their servers.

## 🙏 Acknowledgments

- **Capital Alliance Limited** for providing the public API
- **Chart.js** for the excellent charting library
- The open-source community

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Open an issue on GitHub
3. Check browser console for error messages

## 🔄 Updates & Changelog

### Version 1.0.0 (Current)
- ✅ Initial web release
- ✅ Full localStorage integration
- ✅ Interactive charts
- ✅ Analysis features
- ✅ CSV export
- ✅ Mobile responsive

### Coming Soon
- 🔜 Dark mode
- 🔜 Multiple fund comparison
- 🔜 Portfolio tracking
- 🔜 Email alerts
- 🔜 PDF reports

## 🌟 Star This Project

If you find this useful, please ⭐ star the repository on GitHub!

---

**Built with ❤️ for the Sri Lankan investment community**

**Note:** This is an unofficial tool and is not affiliated with Capital Alliance Limited.

