@echo off
echo ========================================
echo   File Migration to New Structure
echo ========================================
echo.
echo This script will reorganize files into clean architecture
echo.
pause

REM Create necessary directories
echo Creating directories...
if not exist "frontend\assets\css" mkdir frontend\assets\css
if not exist "desktop" mkdir desktop
if not exist "docs" mkdir docs
if not exist "data" mkdir data

echo.
echo Moving files...

REM Move frontend files
if exist "styles.css" (
    echo Moving styles.css to frontend/assets/css/
    move styles.css frontend\assets\css\
)

if exist "index.html" (
    echo Moving index.html to frontend/
    move index.html frontend\
)

REM Move desktop files
if exist "cal_fund_extractor.py" (
    echo Moving cal_fund_extractor.py to desktop/
    move cal_fund_extractor.py desktop\
)

if exist "png_updater.py" (
    echo Moving png_updater.py to desktop/
    move png_updater.py desktop\
)

if exist "requirements.txt" (
    echo Copying requirements.txt to desktop/
    copy requirements.txt desktop\requirements.txt
)

if exist "install_instructions.md" (
    echo Moving install_instructions.md to desktop/
    move install_instructions.md desktop\
)

REM Move documentation
if exist "README_WEB.md" move README_WEB.md docs\
if exist "DEPLOYMENT.md" move DEPLOYMENT.md docs\
if exist "QUICKSTART_WEB.md" move QUICKSTART_WEB.md docs\
if exist "WORKING_SOLUTION.md" move WORKING_SOLUTION.md docs\
if exist "PROJECT_CLEANUP.md" move PROJECT_CLEANUP.md docs\

REM Move data files
echo Moving data files to data/...
if exist "*.csv" move *.csv data\ 2>nul
if exist "*.png" move *.png data\ 2>nul
if exist "*.zip" move *.zip data\ 2>nul

REM Clean up old files
echo.
echo Cleaning up old files...
if exist "server.py" del server.py
if exist "requirements_server.txt" del requirements_server.txt
if exist "start_fullstack.bat" del start_fullstack.bat
if exist "start_fullstack.sh" del start_fullstack.sh
if exist "app.js" (
    echo Backing up old app.js to app.js.backup
    move app.js app.js.backup
)

echo.
echo ========================================
echo   Migration Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Check that files are in correct locations
echo 2. Run: scripts\start.bat
echo 3. Open browser to: http://localhost:5000
echo.
echo Old app.js backed up to: app.js.backup
echo.
pause

