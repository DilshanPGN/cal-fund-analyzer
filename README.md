# CAL Fund Data Extractor

A comprehensive Python tool for extracting and analyzing unit trust fund data from Capital Alliance (CAL) API. This interactive script automatically discovers available funds, fetches historical fund prices, and creates detailed visualizations for investment analysis.

## 🚀 Features

- **Two Operation Modes**: Normal mode for single fund analysis and Init mode for bulk data collection
- **Bulk Data Collection**: Init command efficiently collects data for ALL available funds in one operation
- **Interactive Fund Selection**: Automatically discovers and allows selection from all available CAL funds
- **Smart Data Caching**: Loads existing data to avoid redundant API calls and speeds up analysis
- **Auto Start Date Detection**: Automatically detects the earliest available date for each fund from existing CSV files
- **Fund-Specific Defaults**: Each fund uses its own earliest date as the default start date (no more invalid date ranges)
- **Extended Historical Data**: Default date range from fund-specific earliest date to current date - 1
- **Flexible Date Ranges**: Customizable start and end dates with intelligent date generation
- **Strategic Sampling**: Collects data on 1st and 15th of each month for comprehensive trend analysis
- **Dynamic File Naming**: Automatically generates fund-specific CSV and graph filenames
- **Professional Manual UI**: Dedicated tkinter interface with embedded matplotlib graphs and intuitive controls
- **Financial Context Analysis**: AI-powered analysis of fund performance with Sri Lankan economic context
- **Interactive Analysis Buttons**: One-click analysis for crisis periods, recovery periods, and custom date ranges
- **Real-time Graph Updates**: Dynamic date range filtering with instant graph refresh
- **Popup Analysis Results**: Detailed financial context analysis in dedicated popup windows
- **Data Export**: Saves raw data in CSV format for further analysis and external tools
- **Robust Error Handling**: Comprehensive error handling for network issues and data parsing
- **API-Friendly**: Implements respectful delays between API calls to protect server resources
- **Progress Tracking**: Real-time progress updates and data coverage summaries
- **Smart Data Handling**: Automatically skips dates with no data instead of showing errors
- **Large Dataset Management**: Automatic filtering suggestions for datasets with 100+ data points
- **Smart Data Filtering**: Only loads cached data within the current date range to avoid showing old data

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

### Two Operation Modes

#### 1. Normal Mode - Single Fund Analysis
Run the script with a simple command:
```bash
python cal_fund_extractor.py
```

#### 2. Init Mode - Bulk Data Collection
Collect data for ALL available funds efficiently:
```bash
python cal_fund_extractor.py init
```

### Normal Mode Workflow
The script will guide you through the following steps:

1. **Fund Discovery**: Automatically discovers all available CAL funds from the API
2. **Fund Selection**: Presents a numbered list of available funds for you to choose from
3. **Date Range Configuration**: Allows you to specify custom start and end dates (defaults provided)
4. **Data Collection**: Intelligently collects data, using cached data when available
5. **Progress Tracking**: Shows real-time progress and data coverage summaries
6. **Data Storage**: Saves collected data to a fund-specific CSV file
7. **Manual UI Launch**: Opens the professional tkinter interface with embedded graph
8. **Interactive Analysis**: Use analysis buttons and date controls for comprehensive analysis
9. **Financial Context**: View detailed analysis results in popup windows

### Init Mode Workflow
The init command efficiently collects data for all funds:

1. **Fund Discovery**: Automatically discovers all available CAL funds from the API
2. **Date Range Configuration**: Allows you to specify custom start and end dates (defaults provided)
3. **Smart Data Collection**: Collects data for ALL funds using single API call per date
4. **Progress Tracking**: Shows real-time progress across all funds
5. **Bulk Data Storage**: Creates individual CSV files for each fund
6. **Efficiency Summary**: Reports total files created and data points collected

### Example Normal Mode Session
```
CAL Fund Data Extractor
==================================================
Running in NORMAL mode - analyzing a specific fund
==================================================

Discovering available funds using sample date: 2024-06-01
Found 13 available funds

Detecting earliest dates for 13 funds:
--------------------------------------------------
Found earliest date for Capital Alliance Corporate Treasury Fund: 2013-04-01
Found earliest date for Capital Alliance Medium Risk Debt Fund: 2013-12-15
Found earliest date for CAL Fixed Income Opportunities Fund: 2013-12-15
Found earliest date for CAL Money Market Fund: 2015-01-01
Found earliest date for Capital Alliance Gilt Fund: 2013-08-15
Found earliest date for Capital Alliance Income Fund: 2014-03-15
Found earliest date for Capital Alliance Gilt Trading Fund: 2015-01-15
Found earliest date for Capital Alliance Investment Grade Fund: 2013-09-01
Found earliest date for Capital Alliance High Yield Fund: 2013-01-01
Found earliest date for Capital Alliance Quantitative Equity Fund: 2013-01-15
Found earliest date for Capital Alliance Balanced Fund: 2015-02-01
Found earliest date for CAL Five year Optimum Fund: 2023-07-01
Found earliest date for FYCF: 2024-09-15

Available Funds:
--------------------------------------------------------------------------------
 1. Capital Alliance Corporate Treasury Fund
    📅 Data available from: 2013-04-01
 2. Capital Alliance Medium Risk Debt Fund
    📅 Data available from: 2013-12-15
 3. CAL Fixed Income Opportunities Fund
    📅 Data available from: 2013-12-15
 4. CAL Money Market Fund
    📅 Data available from: 2015-01-01
 5. Capital Alliance Gilt Fund
    📅 Data available from: 2013-08-15
 6. Capital Alliance Income Fund
    📅 Data available from: 2014-03-15
 7. Capital Alliance Gilt Trading Fund
    📅 Data available from: 2015-01-15
 8. Capital Alliance Investment Grade Fund
    📅 Data available from: 2013-09-01
 9. Capital Alliance High Yield Fund
    📅 Data available from: 2013-01-01
10. Capital Alliance Quantitative Equity Fund
    📅 Data available from: 2013-01-15
11. Capital Alliance Balanced Fund
    📅 Data available from: 2015-02-01
12. CAL Five year Optimum Fund
    📅 Data available from: 2023-07-01
13. FYCF
    📅 Data available from: 2024-09-15

Select a fund (1-13) or press Enter for default: 12

Enter start date (YYYY-MM-DD) (default: 2023-07-01): 
Enter end date (YYYY-MM-DD) (default: 2024-12-19): 

==================================================
Target Fund: CAL Five year Optimum Fund
Date Range: 2023-07-01 - 2024-12-19 (1st & 15th of each month)
Data will be saved to: cal_fund_data_CAL_Five_year_Optimum_Fund.csv
==================================================

Data Coverage Summary:
  Total dates in range: 12
  Existing data points: 12
  Missing data points: 0
  ✅ All 12 dates already have data - no API calls needed!
```

### Example Init Mode Session
```
CAL Fund Data Extractor
==================================================
Running INIT command - collecting data for all available funds
==================================================

Discovering available funds using sample date: 2024-12-09
Found 13 available funds

Detecting earliest dates for 13 funds:
--------------------------------------------------
Found earliest date for Capital Alliance Corporate Treasury Fund: 2013-04-01
Found earliest date for Capital Alliance Medium Risk Debt Fund: 2013-12-15
Found earliest date for CAL Fixed Income Opportunities Fund: 2013-12-15
Found earliest date for CAL Money Market Fund: 2015-01-01
Found earliest date for Capital Alliance Gilt Fund: 2013-08-15
Found earliest date for Capital Alliance Income Fund: 2014-03-15
Found earliest date for Capital Alliance Gilt Trading Fund: 2015-01-15
Found earliest date for Capital Alliance Investment Grade Fund: 2013-09-01
Found earliest date for Capital Alliance High Yield Fund: 2013-01-01
Found earliest date for Capital Alliance Quantitative Equity Fund: 2013-01-15
Found earliest date for Capital Alliance Balanced Fund: 2015-02-01
Found earliest date for CAL Five year Optimum Fund: 2023-07-01
Found earliest date for FYCF: 2024-09-15

Earliest data available across all funds: 2013-01-01
Enter start date (YYYY-MM-DD) (default: 2013-01-01): 
Enter end date (YYYY-MM-DD) (default: 2024-12-19): 

==================================================
INIT Mode: Collecting data for ALL available funds
Date Range: 2013-01-01 - 2024-12-19 (1st & 15th of each month)
API Delay: 0.5 seconds between requests
==================================================

Initializing data collection for all funds using sample date: 2024-12-09
Found 13 available funds:
   1. Capital Alliance Corporate Treasury Fund
   2. Capital Alliance Medium Risk Debt Fund
   3. CAL Fixed Income Opportunities Fund
   4. CAL Money Market Fund
   5. Capital Alliance Gilt Fund
   6. Capital Alliance Income Fund
   7. Capital Alliance Gilt Trading Fund
   8. Capital Alliance Investment Grade Fund
   9. Capital Alliance High Yield Fund
  10. Capital Alliance Quantitative Equity Fund
  11. Capital Alliance Balanced Fund
  12. CAL Five year Optimum Fund
  13. FYCF

Data Coverage Summary:
  Total dates in range: 32
  Unique dates needing API calls: 0
  Existing data points: 384/416
  ✅ All 32 dates already have data for all funds - no API calls needed!

File Summary:
  📁 New files created: 0
  🔄 Existing files updated: 13

✅ INIT completed successfully!
📊 Collected data for 13 funds
📁 Created CSV files for each fund

You can now run the normal mode to analyze specific funds:
  python cal_fund_extractor.py
```

## 🎯 When to Use Each Mode

### Use Init Mode When:
- **First-time setup**: You want to collect data for all available funds
- **Bulk data collection**: You need historical data for multiple funds
- **Data refresh**: You want to update all fund data with latest information
- **Research purposes**: You're analyzing multiple funds and need comprehensive datasets

### Use Normal Mode When:
- **Single fund analysis**: You want to focus on one specific fund
- **Interactive visualization**: You want to create graphs and visualizations
- **Detailed analysis**: You need to examine trends and patterns for a specific fund
- **Regular monitoring**: You're tracking a particular fund over time

### Recommended Workflow:
1. **Start with Init**: Run `python cal_fund_extractor.py init` to collect all fund data
2. **Analyze individually**: Use `python cal_fund_extractor.py` to analyze specific funds
3. **Periodic updates**: Re-run init command to refresh data with new dates

## 📅 Fund-Specific Start Dates

The system automatically detects the earliest available date for each fund:

| Fund Name | Earliest Date | Data Points |
|-----------|---------------|-------------|
| Capital Alliance High Yield Fund | 2013-01-01 | 308 |
| Capital Alliance Quantitative Equity Fund | 2013-01-15 | 307 |
| Capital Alliance Corporate Treasury Fund | 2013-04-01 | 302 |
| Capital Alliance Gilt Fund | 2013-08-15 | 293 |
| Capital Alliance Investment Grade Fund | 2013-09-01 | 292 |
| Capital Alliance Medium Risk Debt Fund | 2013-12-15 | 285 |
| CAL Fixed Income Opportunities Fund | 2013-12-15 | 285 |
| Capital Alliance Income Fund | 2014-03-15 | 279 |
| CAL Money Market Fund | 2015-01-01 | 260 |
| Capital Alliance Gilt Trading Fund | 2015-01-15 | 259 |
| Capital Alliance Balanced Fund | 2015-02-01 | 258 |
| CAL Five year Optimum Fund | 2023-07-01 | 56 |
| FYCF | 2024-09-15 | 27 |

**Key Benefits:**
- **No Invalid Dates**: Each fund uses its actual earliest date as default
- **Optimal Data Collection**: Avoids API calls for non-existent data
- **User-Friendly**: Clear display of data availability for each fund
- **Efficient Analysis**: Focuses on actual data ranges for each fund

## 📊 Output Files

### Normal Mode Output
The script generates fund-specific files based on your selection:

| File Pattern | Description |
|--------------|-------------|
| `cal_fund_data_[Fund_Name].csv` | Raw fund price data in CSV format with Date and OLD_PRICE columns |
| `cal_fund_price_trend_[Fund_Name].png` | High-resolution graph visualization showing price trends over time |

### Init Mode Output
The init command creates individual CSV files for ALL available funds:

| File Pattern | Description |
|--------------|-------------|
| `cal_fund_data_[Fund_Name].csv` | Raw fund price data for each fund (one file per fund) |

### Example Output Files
For "Capital Alliance Quantitative Equity Fund":
- `cal_fund_data_Capital_Alliance_Quantitative_Equity_Fund.csv`
- `cal_fund_price_trend_Capital_Alliance_Quantitative_Equity_Fund.png` (Normal mode only)

For "CAL Fixed Income Opportunites Fund":
- `cal_fund_data_CAL_Fixed_Income_Opportunites_Fund.csv`
- `cal_fund_price_trend_CAL_Fixed_Income_Opportunites_Fund.png` (Normal mode only)

### Init Mode Creates Files For All Funds:
- `cal_fund_data_Capital_Alliance_Corporate_Treasury_Fund.csv`
- `cal_fund_data_Capital_Alliance_Medium_Risk_Debt_Fund.csv`
- `cal_fund_data_CAL_Fixed_Income_Opportunities_Fund.csv`
- `cal_fund_data_CAL_Money_Market_Fund.csv`
- `cal_fund_data_Capital_Alliance_Gilt_Fund.csv`
- `cal_fund_data_Capital_Alliance_Income_Fund.csv`
- `cal_fund_data_Capital_Alliance_Gilt_Trading_Fund.csv`
- `cal_fund_data_Capital_Alliance_Investment_Grade_Fund.csv`
- `cal_fund_data_Capital_Alliance_High_Yield_Fund.csv`
- `cal_fund_data_Capital_Alliance_Quantitative_Equity_Fund.csv`
- `cal_fund_data_Capital_Alliance_Balanced_Fund.csv`
- `cal_fund_data_CAL_Five_year_Optimum_Fund.csv`
- `cal_fund_data_FYCF.csv`

## 🔍 Advanced Features

### Fund Discovery
The script automatically discovers all available funds from the CAL API by making a sample request. This ensures you always have access to the most current fund offerings without manual updates.

### Smart Data Caching
- **Automatic Loading**: Existing CSV files are automatically detected and loaded
- **Incremental Updates**: Only missing data points are fetched from the API
- **Efficiency**: Dramatically reduces API calls and processing time for repeated runs
- **Data Integrity**: Validates existing data before using cached values
- **Init Mode Caching**: Init command uses smart caching - subsequent runs only fetch missing data
- **Cross-Fund Efficiency**: Single API call per date collects data for all funds simultaneously

### Auto Start Date Detection
- **Fund-Specific Defaults**: Each fund automatically uses its earliest available date as the default start date
- **CSV File Analysis**: Reads existing CSV files to determine the earliest date for each fund
- **Smart Date Ranges**: Prevents invalid date ranges by using fund-specific start dates
- **Visual Indicators**: Shows each fund's earliest available date in the selection menu
- **Init Mode Intelligence**: Uses the earliest date across all funds for comprehensive data collection
- **No More Invalid Dates**: Eliminates API calls for dates before a fund existed

### Init Command Features
- **Bulk Data Collection**: Efficiently collects data for ALL available funds in one operation
- **Single API Call Per Date**: One request per date fetches data for all funds simultaneously
- **Smart Caching**: Subsequent runs only fetch missing data, dramatically reducing API usage
- **Individual File Creation**: Creates separate CSV files for each fund for easy analysis
- **Progress Tracking**: Shows real-time progress across all funds and dates
- **Efficiency Reporting**: Reports total files created, updated, and data points collected

### Interactive Configuration
- **Fund Selection**: Choose from a dynamically generated list of available funds with earliest dates displayed (Normal mode)
- **Auto Start Dates**: Each fund automatically uses its earliest available date as the default start date
- **Custom Date Ranges**: Specify any start and end date within the API's data range
- **Smart Defaults**: Fund-specific defaults prevent invalid date ranges and optimize data collection
- **Input Validation**: Comprehensive validation for all user inputs

### Manual UI Features
- **Professional Interface**: Dedicated tkinter GUI with embedded matplotlib graphs
- **Left Control Panel**: Analysis buttons, date controls, and help section
- **Right Graph Panel**: Full-featured matplotlib graph with navigation toolbar
- **Real-time Updates**: Dynamic graph updates when changing date ranges
- **Intuitive Controls**: Clear buttons with icons and descriptive labels
- **Responsive Layout**: 1400x900 window with organized panels
- **Error Handling**: Proper error messages and validation in GUI

### Financial Context Analysis
- **AI-Powered Insights**: Intelligent analysis of fund performance patterns
- **Sri Lankan Economic Context**: Integration of significant financial events
- **Performance Metrics**: Return calculations, volatility analysis, and trend detection
- **Crisis Period Analysis**: Pre-configured analysis for 2022 economic crisis
- **Recovery Period Analysis**: Pre-configured analysis for 2023 post-crisis recovery
- **Custom Date Range Analysis**: User-defined period analysis with dialog inputs
- **Current View Analysis**: Analyzes the currently visible graph area
- **Recent Performance**: Automatic analysis of the last 6 months
- **Popup Results**: Detailed analysis displayed in dedicated windows
- **Scrollable Output**: Large text areas for comprehensive analysis results

### Interactive Graph Features
- **Full Zoom Control**: Mouse wheel scroll up to zoom in, scroll down to zoom out
- **Navigation Toolbar**: Complete set of controls including Home, Back/Forward, Pan, and Zoom tools
- **Pan Functionality**: Click and drag to move around when zoomed in
- **Large Dataset Handling**: Automatic filtering suggestions when datasets exceed 100 data points
- **Date Range Filtering**: Interactive filtering to focus on specific time periods
- **High-Resolution Export**: 300 DPI PNG export for presentations and reports
- **Real-time Display**: Graphs display immediately with full interactive controls
- **Embedded Integration**: Seamless integration with tkinter interface

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
- Professional interactive graph with full zoom/pan controls
- Raw data display for verification

## 🖥️ Manual UI Interface

### Interface Layout
The new manual UI provides a professional, user-friendly interface with:

**Left Control Panel (300px width):**
- **Fund Information**: Displays selected fund name and data summary
- **Analysis Options**: Five analysis buttons for different time periods
- **Date Range Controls**: Start/end date inputs with update button
- **Help & Instructions**: Comprehensive usage guide

**Right Graph Panel (1100px width):**
- **Embedded Matplotlib Graph**: Full-featured interactive graph
- **Navigation Toolbar**: Complete zoom, pan, and navigation controls
- **Real-time Updates**: Graph refreshes when date range changes

### Analysis Buttons
- **🔍 Analyze Current View**: Analyzes the currently visible graph area
- **🚨 Crisis Period (2022)**: Pre-configured analysis for economic crisis
- **📈 Recovery Period (2023)**: Pre-configured analysis for post-crisis recovery
- **📊 Recent 6 Months**: Automatic analysis of the most recent performance
- **📅 Custom Date Range**: User-defined period analysis with dialog inputs

### Date Range Controls
- **Start Date Entry**: Text field showing current data start date
- **End Date Entry**: Text field showing current data end date
- **Update Graph Button**: Refreshes graph with new date range
- **Real-time Validation**: Error messages for invalid date formats

### Analysis Results
- **Popup Windows**: Dedicated windows for each analysis result
- **Scrollable Text**: Large text areas for detailed analysis
- **Formatted Output**: Clean, readable analysis presentation
- **Dynamic Titles**: Each window shows the specific analysis period

## 🎮 Interactive Graph Controls

### Mouse Controls
- **Scroll Up**: Zoom in to see more detail
- **Scroll Down**: Zoom out to see broader view
- **Click & Drag**: Pan around when zoomed in

### Toolbar Controls
- **🏠 Home**: Reset to original full view (instant zoom out)
- **⬅️ Back**: Go to previous zoom level
- **➡️ Forward**: Go to next zoom level
- **✋ Pan**: Enable pan mode for moving around
- **🔍 Zoom**: Enable zoom mode for selecting areas to zoom into
- **⚙️ Configure**: Adjust plot settings and appearance
- **💾 Save**: Save the current view as an image

### Manual UI Controls
- **Analysis Buttons**: Click any button for instant financial context analysis
- **Date Range Inputs**: Type new dates and click "Update Graph" to refresh
- **Popup Windows**: View detailed analysis results in dedicated windows
- **Help Section**: Built-in instructions and usage tips

## 🧠 Financial Context Analysis

### AI-Powered Insights
The financial context analysis feature provides intelligent analysis of fund performance with:

**Performance Metrics:**
- **Total Return**: Percentage change from start to end of period
- **Volatility**: Standard deviation of price changes
- **Price Range**: Minimum and maximum prices during the period
- **Significant Moves**: Identification of major price movements (>5% changes)

**Trend Analysis:**
- **Linear Regression**: Statistical trend direction and strength
- **Trend Classification**: Uptrend, Downtrend, or Sideways movement
- **Trend Strength**: Correlation coefficient indicating trend reliability

**Sri Lankan Economic Context:**
- **2022 Crisis Events**: Economic crisis, political instability, inflation
- **2023 Recovery Events**: Economic stabilization, policy changes, market recovery
- **2024 Recent Events**: Current economic conditions and policy updates
- **Event Correlation**: Links between economic events and fund performance

**AI-Generated Insights:**
- **Performance Interpretation**: Human-readable analysis of fund behavior
- **Risk Assessment**: Volatility and risk level evaluation
- **Market Context**: Explanation of performance in economic context
- **Investment Guidance**: Actionable insights for investors

### Analysis Types

**1. Crisis Period Analysis (2022)**
- Analyzes the economic crisis period
- Identifies impact of political and economic instability
- Shows fund resilience during difficult times

**2. Recovery Period Analysis (2023)**
- Examines post-crisis recovery
- Identifies recovery patterns and growth trends
- Shows fund performance during stabilization

**3. Recent Performance Analysis**
- Analyzes the last 6 months
- Provides current market assessment
- Shows recent trends and patterns

**4. Custom Date Range Analysis**
- User-defined period analysis
- Flexible date range selection
- Custom economic context evaluation

**5. Current View Analysis**
- Analyzes the currently visible graph area
- Perfect for zoomed-in analysis
- Real-time context for specific periods

### Benefits for Investors
- **Contextual Understanding**: Understand why fund prices moved
- **Risk Assessment**: Evaluate fund volatility and risk levels
- **Trend Identification**: Spot patterns and trends early
- **Economic Correlation**: See how economic events affect fund performance
- **Investment Decisions**: Make informed decisions based on comprehensive analysis

## ⚙️ Technical Details

### Architecture
- **Object-Oriented Design**: Clean class-based architecture with `CALFundExtractor` class
- **Modular Functions**: Separate functions for fund discovery, data collection, and visualization
- **Type Hints**: Full type annotations for better code maintainability and IDE support
- **GUI Integration**: Seamless integration between tkinter and matplotlib

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
- **Full Navigation**: Complete zoom in/out, pan, and navigation controls
- **Smart Filtering**: Automatic filtering suggestions for large datasets
- **Manual UI Integration**: Embedded matplotlib graphs in tkinter interface
- **Real-time Updates**: Dynamic graph updates when changing date ranges
- **Professional Layout**: Organized control panels with intuitive design

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
- **Manual UI Issues**: Ensure tkinter is properly installed (usually included with Python)
- **Button Clicks**: All analysis buttons should work without errors - check console for debug messages
- **Popup Windows**: Analysis results open in dedicated windows - check if they're behind the main window

### Data Collection Issues
- **Partial Data**: The script will show which dates have data and which are missing
- **Missing Data Handling**: Dates with no data are automatically skipped (no errors shown)
- **API Rate Limiting**: If you get blocked, wait a few minutes before retrying
- **Date Range Errors**: Ensure dates are in YYYY-MM-DD format and within API range
- **Large Datasets**: For datasets with 100+ points, consider using the filtering option
- **Old Data Display**: Cached data is automatically filtered to only show data within your current date range

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
