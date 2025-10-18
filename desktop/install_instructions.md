# Installation Instructions for CAL Fund Data Extractor

This guide will help you set up Python and install all required dependencies to run the CAL Fund Data Extractor.

## 📋 System Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **Python Version**: 3.8 or higher (3.11+ recommended)
- **Internet Connection**: Required for downloading packages and accessing CAL API
- **Disk Space**: At least 100MB free space

## 🐍 Step 1: Install Python

### Windows Installation

#### Option A: Official Python Website (Recommended)
1. **Download Python**:
   - Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
   - Click "Download Python 3.x.x" (latest stable version)
   - Choose the appropriate installer for your system (64-bit recommended)

2. **Run the Installer**:
   - Double-click the downloaded `.exe` file
   - **CRITICAL**: Check the box "Add Python to PATH" at the bottom of the installer
   - Click "Install Now" (this installs Python with pip)
   - Wait for installation to complete

3. **Verify Installation**:
   - Open PowerShell or Command Prompt
   - Type: `python --version`
   - You should see: `Python 3.11.x` or similar

#### Option B: Microsoft Store (Alternative)
1. Open Microsoft Store
2. Search for "Python"
3. Install "Python 3.x" (latest version)
4. This automatically adds Python to PATH

### macOS Installation

#### Option A: Official Python Website
1. Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Download the macOS installer (.pkg file)
3. Run the installer and follow the prompts
4. Python will be installed in `/usr/local/bin/`

#### Option B: Homebrew (Recommended for developers)
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python
```

### Linux Installation

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

#### CentOS/RHEL/Fedora:
```bash
sudo yum install python3 python3-pip
# or for newer versions:
sudo dnf install python3 python3-pip
```

## 🔧 Step 2: Verify Python Installation

Open your terminal/command prompt and run:

```bash
python --version
# or on some systems:
python3 --version
```

**Expected Output**: `Python 3.8.x` or higher

### Alternative Commands
If `python` doesn't work, try:
- `py --version` (Windows)
- `python3 --version` (Linux/macOS)

## 📦 Step 3: Install Required Packages

### Navigate to Project Directory
```bash
# Windows
cd "C:\Development\Personal\CAL fund extractor"

# macOS/Linux
cd "/path/to/CAL fund extractor"
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

**Expected Output**: Installation of `requests`, `pandas`, and `matplotlib` packages

### Alternative Installation Methods

#### Using Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv cal_fund_env

# Activate virtual environment
# Windows:
cal_fund_env\Scripts\activate
# macOS/Linux:
source cal_fund_env/bin/activate

# Install packages
pip install -r requirements.txt
```

#### Manual Package Installation
```bash
pip install requests>=2.31.0 pandas>=2.0.0 matplotlib>=3.7.0
```

## 🚀 Step 4: Run the Script

```bash
python cal_fund_extractor.py
```

The script will:
1. Display progress as it fetches data
2. Save results to `cal_fund_data.csv`
3. Create and display a graph (`cal_fund_price_trend.png`)
4. Show summary statistics

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### 1. "python" command not found
**Windows**:
- Restart PowerShell/Command Prompt
- Try `py` instead of `python`
- Reinstall Python with "Add to PATH" checked

**macOS/Linux**:
- Try `python3` instead of `python`
- Check if Python is in your PATH: `echo $PATH`

#### 2. "pip" command not found
```bash
# Try these alternatives:
python -m pip --version
python3 -m pip --version

# If pip is missing, install it:
python -m ensurepip --upgrade
```

#### 3. Permission Errors (macOS/Linux)
```bash
# Use --user flag to install in user directory
pip install --user -r requirements.txt
```

#### 4. Network/Proxy Issues
```bash
# If behind corporate firewall:
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
```

#### 5. Package Installation Failures
```bash
# Update pip first
python -m pip install --upgrade pip

# Then install packages
pip install -r requirements.txt
```

#### 6. Matplotlib Display Issues
**Windows**: Usually works out of the box
**macOS**: May need additional backend
```bash
pip install --upgrade matplotlib
```

**Linux**: May need GUI libraries
```bash
sudo apt-get install python3-tk
```

### Getting Additional Help

1. **Check Python Installation**:
   ```bash
   python -c "import sys; print(sys.version)"
   ```

2. **Check Package Installation**:
   ```bash
   python -c "import requests, pandas, matplotlib; print('All packages installed successfully')"
   ```

3. **Verify Internet Connection**:
   ```bash
   python -c "import requests; print(requests.get('https://cal.lk').status_code)"
   ```

## 🔄 Updating the Tool

To update to the latest version:
```bash
# Update pip
python -m pip install --upgrade pip

# Reinstall packages
pip install --upgrade -r requirements.txt
```

## 📞 Support

If you continue to have issues:
1. Check the console output for specific error messages
2. Verify your Python version meets requirements (3.8+)
3. Ensure all packages installed successfully
4. Test your internet connection
5. Try running the script in a virtual environment

## 🎯 Next Steps

Once installation is complete:
1. Run `python cal_fund_extractor.py`
2. Check the generated `cal_fund_data.csv` file
3. View the `cal_fund_price_trend.png` graph
4. Review the console output for any warnings or errors
