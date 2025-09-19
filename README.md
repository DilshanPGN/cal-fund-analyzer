# CAL Fund Data Extractor

A comprehensive Python tool for extracting and analyzing unit trust fund data from Capital Alliance (CAL) API. This interactive script automatically discovers available funds, fetches historical fund prices, and creates detailed visualizations for investment analysis.

## 🚀 Features

- **Interactive Fund Selection**: Automatically discovers and allows selection from all available CAL funds
- **Smart Data Caching**: Loads existing data to avoid redundant API calls and speeds up analysis
- **Extended Historical Data**: Default date range from 2013-01-01 to current date - 1
- **Flexible Date Ranges**: Customizable start and end dates with intelligent date generation
- **Strategic Sampling**: Collects data on 1st and 15th of each month for comprehensive trend analysis
- **Dynamic File Naming**: Automatically generates fund-specific CSV and graph filenames
- **Interactive Visualizations**: Creates expandable, zoomable graphs with filtering options for large datasets
- **Data Export**: Saves raw data in CSV format for further analysis and external tools
- **Robust Error Handling**: Comprehensive error handling for network issues and data parsing
- **API-Friendly**: Implements respectful delays between API calls to protect server resources
- **Progress Tracking**: Real-time progress updates and data coverage summaries
- **Smart Data Handling**: Automatically skips dates with no data instead of showing errors
- **Large Dataset Management**: Automatic filtering suggestions for datasets with 100+ data points

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

### Interactive Usage
Run the script with a simple command:
```bash
python cal_fund_extractor.py
```

### Interactive Workflow
The script will guide you through the following steps:

1. **Fund Discovery**: Automatically discovers all available CAL funds from the API
2. **Fund Selection**: Presents a numbered list of available funds for you to choose from
3. **Date Range Configuration**: Allows you to specify custom start and end dates (defaults provided)
4. **Data Collection**: Intelligently collects data, using cached data when available
5. **Progress Tracking**: Shows real-time progress and data coverage summaries
6. **Data Storage**: Saves collected data to a fund-specific CSV file
7. **Visualization**: Creates and displays a professional graph with fund-specific naming
8. **Summary Statistics**: Provides detailed statistics about the collected data

### Example Interactive Session
```
CAL Fund Data Extractor
==================================================

Discovering available funds using sample date: 2024-06-01
Found 3 available funds

Available Funds:
--------------------------------------------------
 1. Capital Alliance Quantitative Equity Fund
 2. CAL Fixed Income Opportunites Fund
 3. Capital Alliance Investment Grade Fund

Select a fund (1-3) or press Enter for default: 1

Enter start date (YYYY-MM-DD) (default: 2013-01-01): 
Enter end date (YYYY-MM-DD) (default: 2024-12-19): 

==================================================
Target Fund: Capital Alliance Quantitative Equity Fund
Date Range: 2013-01-01 - 2024-12-19 (1st & 15th of each month)
Data will be saved to: cal_fund_data_Capital_Alliance_Quantitative_Equity_Fund.csv
==================================================

Data Coverage Summary:
  Total dates in range: 32
  Existing data points: 15
  Missing data points: 17
  Existing data range: 2024-06-01 to 2024-12-15
  ✓ Using cached data for 15 dates
  Missing data range: 2025-01-01 to 2025-09-01
  🔄 Fetching from API for 17 dates...
```

## 📊 Output Files

The script generates fund-specific files based on your selection:

| File Pattern | Description |
|--------------|-------------|
| `cal_fund_data_[Fund_Name].csv` | Raw fund price data in CSV format with Date and OLD_PRICE columns |
| `cal_fund_price_trend_[Fund_Name].png` | High-resolution graph visualization showing price trends over time |

### Example Output Files
For "Capital Alliance Quantitative Equity Fund":
- `cal_fund_data_Capital_Alliance_Quantitative_Equity_Fund.csv`
- `cal_fund_price_trend_Capital_Alliance_Quantitative_Equity_Fund.png`

For "CAL Fixed Income Opportunites Fund":
- `cal_fund_data_CAL_Fixed_Income_Opportunites_Fund.csv`
- `cal_fund_price_trend_CAL_Fixed_Income_Opportunites_Fund.png`

## 🔍 Advanced Features

### Fund Discovery
The script automatically discovers all available funds from the CAL API by making a sample request. This ensures you always have access to the most current fund offerings without manual updates.

### Smart Data Caching
- **Automatic Loading**: Existing CSV files are automatically detected and loaded
- **Incremental Updates**: Only missing data points are fetched from the API
- **Efficiency**: Dramatically reduces API calls and processing time for repeated runs
- **Data Integrity**: Validates existing data before using cached values

### Interactive Configuration
- **Fund Selection**: Choose from a dynamically generated list of available funds
- **Custom Date Ranges**: Specify any start and end date within the API's data range
- **Default Values**: Sensible defaults are provided for quick execution (2013-01-01 to current date - 1)
- **Input Validation**: Comprehensive validation for all user inputs

### Interactive Graph Features
- **Zoom and Pan**: Use mouse wheel to zoom in/out and drag to pan around the graph
- **Large Dataset Handling**: Automatic filtering suggestions when datasets exceed 100 data points
- **Date Range Filtering**: Interactive filtering to focus on specific time periods
- **High-Resolution Export**: 300 DPI PNG export for presentations and reports
- **Real-time Display**: Graphs display immediately with interactive controls

## 🔗 API Information

**Endpoint**: `https://cal.lk/wp-admin/admin-ajax.php?action=getUTFundRates&valuedate=YYYY-M-D`

**Parameters**:
- `action`: `getUTFundRates` (fixed)
- `valuedate`: Date in YYYY-M-D format (e.g., 2024-06-01)

**Rate Limiting**: 0.5-second delay between API calls to respect server resources

## 📈 Sample Output

The script provides:
- Real-time progress updates during data collection
- Summary statistics including total data points, date range, price range, and average price
- Professional graph with markers, grid, and proper formatting
- Raw data display for verification

## ⚙️ Technical Details

### Architecture
- **Object-Oriented Design**: Clean class-based architecture with `CALFundExtractor` class
- **Modular Functions**: Separate functions for fund discovery, data collection, and visualization
- **Type Hints**: Full type annotations for better code maintainability and IDE support

### Data Management
- **Smart Caching**: Automatic detection and loading of existing CSV files
- **Incremental Updates**: Only fetches missing data points to minimize API usage
- **Data Validation**: Comprehensive validation for fund names, dates, and price data
- **Error Recovery**: Graceful handling of network issues and malformed data

### Performance Features
- **Rate Limiting**: 0.5-second delay between API calls to respect server resources
- **Progress Tracking**: Real-time updates on data collection progress
- **Efficient Processing**: Uses pandas for fast data manipulation and analysis
- **Memory Optimization**: Processes data in chunks to handle large datasets

### Visualization
- **Professional Styling**: High-quality matplotlib graphs with proper formatting
- **Dynamic Titles**: Fund-specific graph titles and filenames
- **Export Options**: High-resolution PNG export (300 DPI) for presentations
- **Interactive Display**: Shows graphs in real-time during execution

### File Management
- **Dynamic Naming**: Automatic generation of fund-specific filenames
- **Safe Overwriting**: Preserves existing data while updating with new information
- **Standardized Format**: Consistent CSV structure for easy integration with other tools

## 🐛 Troubleshooting

### Common Issues
- **API Timeout**: Check internet connection and try again
- **Missing Data**: Some dates may not have data available - this is normal
- **Graph Display**: Ensure matplotlib backend is properly configured
- **Fund Not Found**: If a fund doesn't appear in the list, check if it's available in the API
- **Cached Data Issues**: Delete the CSV file if you suspect corrupted cached data

### Data Collection Issues
- **Partial Data**: The script will show which dates have data and which are missing
- **Missing Data Handling**: Dates with no data are automatically skipped (no errors shown)
- **API Rate Limiting**: If you get blocked, wait a few minutes before retrying
- **Date Range Errors**: Ensure dates are in YYYY-MM-DD format and within API range
- **Large Datasets**: For datasets with 100+ points, consider using the filtering option

### Getting Help
If you encounter issues:
1. Check the console output for detailed error messages and progress updates
2. Verify your internet connection and API endpoint availability
3. Ensure all dependencies are installed correctly (`pip install -r requirements.txt`)
4. Check if the fund you selected is available in the discovered fund list
5. Try deleting existing CSV files if you suspect data corruption
6. Verify date format (YYYY-MM-DD) and ensure dates are within reasonable range

## 📝 License

This project is for educational and personal use. Please respect CAL's API terms of service.

## 🤝 Contributing

Feel free to submit issues or pull requests to improve this tool.
