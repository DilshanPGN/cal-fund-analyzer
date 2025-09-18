# CAL Fund Data Extractor

A comprehensive Python tool for extracting and analyzing unit trust fund data from Capital Alliance (CAL) API. This script automatically fetches historical fund prices and creates detailed visualizations for investment analysis.

## 🚀 Features

- **Automated Data Collection**: Fetches fund data from CAL API for specific date ranges
- **Targeted Analysis**: Focuses on "Capital Alliance Quantitative Equity Fund" OLD_PRICE data
- **Comprehensive Date Coverage**: Analyzes data from June 2024 to September 2025
- **Strategic Sampling**: Collects data on 1st and 15th of each month for trend analysis
- **Interactive Visualizations**: Creates professional graphs showing price trends over time
- **Data Export**: Saves raw data in CSV format for further analysis
- **Robust Error Handling**: Includes comprehensive error handling and data validation
- **API-Friendly**: Implements respectful delays between API calls

## 📋 Prerequisites

- Python 3.8 or higher
- Internet connection for API access
- Required Python packages (see Installation section)

## 🛠️ Installation

### Quick Start
1. Clone or download this repository
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Detailed Installation
For detailed installation instructions, including Python setup, see [install_instructions.md](install_instructions.md).

## 🎯 Usage

### Basic Usage
Run the script with a simple command:
```bash
python cal_fund_extractor.py
```

### What the Script Does
1. **Date Generation**: Creates a comprehensive list of dates (1st and 15th of each month from June 2024 to September 2025)
2. **API Data Fetching**: Retrieves fund data from CAL API for each specified date
3. **Data Extraction**: Extracts OLD_PRICE values for "Capital Alliance Quantitative Equity Fund"
4. **Data Storage**: Saves collected data to `cal_fund_data.csv`
5. **Visualization**: Creates and displays a professional graph saved as `cal_fund_price_trend.png`
6. **Summary Statistics**: Provides detailed statistics about the collected data

## 📊 Output Files

| File | Description |
|------|-------------|
| `cal_fund_data.csv` | Raw fund price data in CSV format with Date and OLD_PRICE columns |
| `cal_fund_price_trend.png` | High-resolution graph visualization showing price trends over time |

## 🔗 API Information

**Endpoint**: `https://cal.lk/wp-admin/admin-ajax.php?action=getUTFundRates&valuedate=YYYY-M-D`

**Parameters**:
- `action`: `getUTFundRates` (fixed)
- `valuedate`: Date in YYYY-M-D format (e.g., 2024-06-01)

## 📈 Sample Output

The script provides:
- Real-time progress updates during data collection
- Summary statistics including total data points, date range, price range, and average price
- Professional graph with markers, grid, and proper formatting
- Raw data display for verification

## ⚙️ Technical Details

- **Rate Limiting**: 0.5-second delay between API calls to respect server resources
- **Error Handling**: Comprehensive error handling for network issues and data parsing
- **Data Validation**: Validates fund names and price data before processing
- **Graph Features**: Interactive matplotlib graphs with professional styling
- **CSV Format**: Standardized CSV output for easy import into other tools

## 🐛 Troubleshooting

### Common Issues
- **API Timeout**: Check internet connection and try again
- **Missing Data**: Some dates may not have data available
- **Graph Display**: Ensure matplotlib backend is properly configured

### Getting Help
If you encounter issues:
1. Check the console output for error messages
2. Verify your internet connection
3. Ensure all dependencies are installed correctly
4. Check the API endpoint availability

## 📝 License

This project is for educational and personal use. Please respect CAL's API terms of service.

## 🤝 Contributing

Feel free to submit issues or pull requests to improve this tool.
