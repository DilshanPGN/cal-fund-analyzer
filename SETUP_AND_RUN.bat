@echo off
echo ==========================================
echo   CAL Fund Analyzer - Complete Setup
echo ==========================================
echo.
echo This will:
echo 1. Check Python installation
echo 2. Migrate files to new structure
echo 3. Install dependencies
echo 4. Start the application
echo.
pause

REM ========================================
REM STEP 1: Check Python
REM ========================================
echo.
echo [Step 1/4] Checking Python...
echo.

where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo.
    echo IMPORTANT: During installation, check the box that says
    echo "Add Python to PATH"
    echo.
    echo After installing Python, run this script again.
    echo.
    pause
    exit /b 1
)

echo Found: 
python --version
echo.

REM ========================================
REM STEP 2: Run Migration
REM ========================================
echo [Step 2/4] Migrating files...
echo.

if exist "backend\server.py" (
    echo Backend folder already exists. Skipping migration.
) else (
    echo Creating directory structure...
    
    REM Create directories
    if not exist "backend\services" mkdir backend\services
    if not exist "backend\routes" mkdir backend\routes
    if not exist "frontend\assets\css" mkdir frontend\assets\css
    if not exist "frontend\assets\js\services" mkdir frontend\assets\js\services
    if not exist "frontend\assets\js\components" mkdir frontend\assets\js\components
    if not exist "frontend\assets\js\utils" mkdir frontend\assets\js\utils
    if not exist "desktop" mkdir desktop
    if not exist "docs" mkdir docs
    if not exist "data" mkdir data
    
    echo Directories created!
    
    REM Move frontend files
    if exist "styles.css" (
        echo Moving styles.css...
        move styles.css frontend\assets\css\
    )
    
    if exist "index.html" (
        echo Moving index.html...
        move index.html frontend\
    )
    
    REM Move desktop files
    if exist "cal_fund_extractor.py" move cal_fund_extractor.py desktop\
    if exist "png_updater.py" move png_updater.py desktop\
    if exist "requirements.txt" copy requirements.txt desktop\requirements.txt >nul
    if exist "install_instructions.md" move install_instructions.md desktop\
    
    REM Move docs
    if exist "README_WEB.md" move README_WEB.md docs\
    if exist "DEPLOYMENT.md" move DEPLOYMENT.md docs\
    if exist "QUICKSTART_WEB.md" move QUICKSTART_WEB.md docs\
    if exist "WORKING_SOLUTION.md" move WORKING_SOLUTION.md docs\
    if exist "PROJECT_CLEANUP.md" move PROJECT_CLEANUP.md docs\
    if exist "RESTRUCTURE_GUIDE.md" move RESTRUCTURE_GUIDE.md docs\
    if exist "RESTRUCTURE_COMPLETE.md" move RESTRUCTURE_COMPLETE.md docs\
    
    REM Move data files
    for %%f in (*.csv *.png *.zip) do (
        if exist "%%f" move "%%f" data\ 2>nul
    )
    
    REM Clean up old files
    if exist "server.py" del server.py
    if exist "requirements_server.txt" del requirements_server.txt
    if exist "start_fullstack.bat" del start_fullstack.bat
    if exist "start_fullstack.sh" del start_fullstack.sh
    if exist "app.js" move app.js app.js.backup
    
    echo Migration complete!
)

echo.

REM ========================================
REM STEP 3: Install Dependencies
REM ========================================
echo [Step 3/4] Installing dependencies...
echo.

cd backend
echo Installing Python packages...
python -m pip install -r requirements.txt --quiet

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo WARNING: Installation had issues. Trying again with verbose output...
    python -m pip install -r requirements.txt
)

cd ..
echo Dependencies installed!
echo.

REM ========================================
REM STEP 4: Start Application
REM ========================================
echo [Step 4/4] Starting application...
echo.
echo ==========================================
echo   Application Ready!
echo ==========================================
echo.
echo Open your browser to: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.
echo Opening browser in 3 seconds...
timeout /t 3 /nobreak >nul
start http://localhost:5000
echo.

cd backend
python server.py

cd ..
echo.
echo Server stopped.
pause

