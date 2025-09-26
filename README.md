# CAL Fund Analyzer

A comprehensive Python tool for extracting and analyzing unit trust fund data from Capital Alliance (CAL) API. This modern GUI application automatically discovers available funds, fetches historical fund prices, and creates detailed visualizations for investment analysis.

## 🚀 Features

### 🖥️ **Modern GUI Interface**
- **Complete GUI Configuration**: All settings (fund selection, date ranges, API delay) handled through intuitive GUI
- **No Terminal Input Required**: Fully graphical interface eliminates command-line complexity
- **Multi-Window Support**: Configuration window, main analysis window, and dialog windows
- **Smart Window Positioning**: Automatic positioning on primary monitor with proper centering
- **Scrollable Interface**: Scrollable panels for better content organization
- **Professional Layout**: Clean, modern interface with organized sections

### 📊 **Enhanced Data Management**
- **Refresh Data Button**: Update fund data without restarting the application
- **Change Fund Button**: Switch between different funds seamlessly
- **Real-time Status Updates**: Live status messages during data operations
- **Smart Data Caching**: Loads existing data to avoid redundant API calls
- **Auto Start Date Detection**: Automatically detects earliest available date for each fund
- **Fund-Specific Defaults**: Each fund uses its own earliest date as default start date
- **Extended Historical Data**: Default date range from fund-specific earliest date to current date
- **Strategic Sampling**: Collects data on 1st and 15th of each month plus current date

### 🎯 **Two Operation Modes**
- **Normal Mode**: Single fund analysis with full GUI interface
- **Init Mode**: Bulk data collection for ALL available funds
- **GUI Configuration**: Both modes use graphical interface for setup
- **Seamless Workflow**: Easy switching between modes

### 🔍 **Advanced Analysis Features**
- **Financial Context Analysis**: AI-powered analysis with Sri Lankan economic context
- **Interactive Analysis Buttons**: One-click analysis for crisis periods, recovery periods, and custom ranges
- **Real-time Graph Updates**: Dynamic date range filtering with instant graph refresh
- **Popup Analysis Results**: Detailed analysis in dedicated popup windows
- **Current View Analysis**: Analyze the currently visible graph area
- **Custom Date Range Analysis**: User-defined period analysis with dialog inputs

### 🖼️ **Professional Visualization**
- **Embedded Matplotlib Graphs**: Full-featured interactive graphs within GUI
- **Complete Navigation Controls**: Zoom, pan, home, back/forward controls
- **High-Resolution Export**: 300 DPI PNG export for presentations
- **Dynamic Graph Updates**: Real-time updates when changing date ranges
- **Professional Styling**: High-quality graphs with proper formatting

### 🔧 **User Experience Improvements**
- **Easy Application Closing**: Multiple ways to close (button, keyboard shortcuts, window controls)
- **Keyboard Shortcuts**: Ctrl+Q and Escape keys for quick closing
- **Proper Window Management**: Automatic maximization and primary monitor positioning
- **Scrollable Content**: Mouse wheel support for scrolling through interface elements
- **Responsive Design**: Adapts to different screen sizes with minimum size constraints
- **Error Handling**: Comprehensive error handling with user-friendly messages

### 📁 **Smart File Management**
- **Dynamic File Naming**: Automatic generation of fund-specific filenames
- **Data Export**: Saves raw data in CSV format for external analysis
- **Safe Data Handling**: Preserves existing data while updating with new information
- **Bulk File Creation**: Init mode creates individual CSV files for all funds

### 🌐 **API Integration**
- **Automatic Fund Discovery**: Discovers all available CAL funds from API
- **API-Friendly**: Implements respectful delays between API calls
- **Progress Tracking**: Real-time progress updates during data collection
- **Smart Error Handling**: Gracefully handles network issues and missing data

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

### 🚀 **Quick Start**
Simply run the application:
```bash
python cal_fund_extractor.py
```

The application will open with a modern GUI interface - no command-line input required!

### 🖥️ **GUI Workflow**

#### **1. Configuration Window**
When you start the application, you'll see a configuration window with:

- **Fund Selection Dropdown**: Choose from all available CAL funds
- **Date Range Inputs**: Set start and end dates (defaults provided automatically)
- **API Delay Setting**: Configure delay between API calls (default: 0.5 seconds)
- **Start Analysis Button**: Begin data collection and analysis

#### **2. Main Analysis Window**
After configuration, the main analysis window opens with:

**Left Control Panel:**
- **Fund Information**: Current fund name and data summary
- **Analysis Options**: Five analysis buttons for different time periods
- **Data Management**: Refresh data and change fund buttons
- **Date Range Controls**: Update graph with new date ranges
- **Help Section**: Built-in instructions and tips
- **Close Application**: Easy application closing options

**Right Graph Panel:**
- **Interactive Graph**: Full-featured matplotlib graph with navigation controls
- **Zoom & Pan**: Mouse wheel zoom, click-and-drag pan
- **Navigation Toolbar**: Home, back/forward, zoom, pan, save controls

### 🎯 **Two Operation Modes**

#### **Normal Mode - Single Fund Analysis**
```bash
python cal_fund_extractor.py
```
- Opens GUI configuration window
- Select fund, dates, and settings
- Launches main analysis interface
- Full interactive analysis capabilities

#### **Init Mode - Bulk Data Collection**
```bash
python cal_fund_extractor.py init
```
- Opens GUI configuration window
- Collects data for ALL available funds
- Creates individual CSV files for each fund
- Efficient bulk data collection

### 🔄 **Data Management Features**

#### **Refresh Data**
- Click "Refresh Data" button to update current fund data
- Automatically fetches latest data points
- Updates graph and data summary
- No need to restart application

#### **Change Fund**
- Click "Change Fund" button to switch funds
- Opens fund selection dialog
- Automatically loads new fund data
- Updates interface with new fund information

#### **Real-time Status**
- Live status messages during operations
- Progress indicators for data collection
- Error messages with helpful suggestions
- Success confirmations for completed operations

### 🎮 **Interactive Analysis Features**

#### **Analysis Buttons**
- **🔍 Analyze Current View**: Analyzes the currently visible graph area
- **🚨 Crisis Period (2022)**: Pre-configured analysis for economic crisis
- **📈 Recovery Period (2023)**: Pre-configured analysis for post-crisis recovery
- **📊 Recent 6 Months**: Automatic analysis of the most recent performance
- **📅 Custom Date Range**: User-defined period analysis with dialog inputs

#### **Graph Controls**
- **Mouse Wheel**: Scroll up to zoom in, scroll down to zoom out
- **Click & Drag**: Pan around when zoomed in
- **Navigation Toolbar**: Complete set of zoom, pan, and navigation controls
- **Home Button**: Reset to original full view
- **Save Button**: Export current view as high-resolution image

#### **Date Range Controls**
- **Start Date Input**: Modify the start date for analysis
- **End Date Input**: Modify the end date for analysis
- **Update Graph Button**: Refresh graph with new date range
- **Real-time Validation**: Error messages for invalid date formats

### 🚪 **Application Closing Options**

#### **Multiple Ways to Close**
- **Close Button**: Click the "🚪 Close Application" button in the interface
- **Keyboard Shortcuts**: Press `Ctrl+Q` or `Escape` key
- **Window Controls**: Use the standard window close button (X)
- **Proper Cleanup**: All methods ensure proper resource cleanup

#### **Window Management**
- **Automatic Positioning**: Windows open on primary monitor
- **Smart Centering**: Automatic centering and sizing
- **Maximization**: Main window opens maximized for better viewing
- **Multi-Monitor Support**: Proper handling of multiple monitor setups

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

## 🖥️ **Modern GUI Interface**

### **Configuration Window**
The application starts with a clean configuration interface:

- **Fund Selection Dropdown**: Choose from all available CAL funds with earliest dates displayed
- **Date Range Inputs**: Start and end date fields with automatic defaults
- **API Delay Setting**: Configurable delay between API calls (default: 0.5 seconds)
- **Start Analysis Button**: Begin data collection and launch main interface
- **Scrollable Content**: Mouse wheel support for easy navigation
- **Smart Positioning**: Automatic centering on primary monitor

### **Main Analysis Window**
Professional analysis interface with organized layout:

**Left Control Panel (350px width):**
- **Fund Information**: Current fund name and comprehensive data summary
- **Analysis Options**: Five analysis buttons for different time periods
- **Data Management**: Refresh data and change fund buttons
- **Date Range Controls**: Start/end date inputs with update button
- **Help & Instructions**: Comprehensive usage guide
- **Close Application**: Multiple closing options with keyboard shortcuts
- **Scrollable Content**: Mouse wheel support for all sections

**Right Graph Panel (1250px width):**
- **Embedded Matplotlib Graph**: Full-featured interactive graph
- **Navigation Toolbar**: Complete zoom, pan, and navigation controls
- **Real-time Updates**: Graph refreshes when date range changes
- **High-Resolution Display**: Professional-quality graph rendering

### **Window Management Features**
- **Automatic Maximization**: Main window opens maximized for optimal viewing
- **Primary Monitor Positioning**: Ensures windows open on correct monitor
- **Smart Centering**: Automatic centering and proper sizing
- **Multi-Monitor Support**: Proper handling of multiple monitor setups
- **Responsive Design**: Adapts to different screen sizes with minimum constraints

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

### **GUI Issues**
- **Window Positioning**: If windows open on wrong monitor, check your display settings
- **Scrolling Problems**: Use mouse wheel to scroll through interface elements
- **Button Not Working**: Ensure you're clicking within the button area
- **Graph Not Displaying**: Check if matplotlib backend is properly configured
- **Popup Windows**: Analysis results open in dedicated windows - check if they're behind main window
- **Application Won't Close**: Try Ctrl+Q, Escape key, or the close button

### **Data Collection Issues**
- **API Timeout**: Check internet connection and try again
- **Missing Data**: Some dates may not have data available - this is normal
- **Fund Not Found**: If a fund doesn't appear in dropdown, check if it's available in API
- **Cached Data Issues**: Delete the CSV file if you suspect corrupted cached data
- **Partial Data**: The application will show which dates have data and which are missing
- **API Rate Limiting**: If you get blocked, wait a few minutes before retrying

### **Window Management Issues**
- **Multi-Monitor Problems**: Application automatically positions on primary monitor
- **Window Too Small**: Application has minimum size constraints to prevent issues
- **Maximization Issues**: Main window should open maximized automatically
- **Dialog Positioning**: All dialogs are centered on primary monitor

### **Getting Help**
If you encounter issues:
1. Check the console output for detailed error messages and progress updates
2. Verify your internet connection and API endpoint availability
3. Ensure all dependencies are installed correctly (`pip install -r requirements.txt`)
4. Try refreshing data or changing funds using the GUI buttons
5. Restart the application if GUI becomes unresponsive
6. Check if the fund you selected is available in the dropdown list

## 📝 License

This project is for educational and personal use. Please respect CAL's API terms of service.

## 🤝 Contributing

Feel free to submit issues or pull requests to improve this tool.
