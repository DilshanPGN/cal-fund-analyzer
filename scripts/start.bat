@echo off
echo ========================================
echo   CAL Fund Analyzer - Clean Architecture
echo ========================================
echo.

REM Check if backend folder exists
if not exist "backend" (
    echo ERROR: Backend folder not found!
    echo.
    echo It looks like the migration hasn't been run yet.
    echo Please run the migration first:
    echo.
    echo   scripts\migrate.bat
    echo.
    echo This will organize files into the new structure.
    echo.
    pause
    exit /b 1
)

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Found Python: 
python --version
echo.

REM Check if pip is available
python -m pip --version >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: pip is not available
    echo.
    echo Trying to install pip...
    python -m ensurepip --default-pip
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to install pip. Please install Python properly.
        pause
        exit /b 1
    )
)

echo Installing dependencies...
echo.

REM Install backend dependencies
cd backend
python -m pip install -r requirements.txt --quiet
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to install dependencies
    echo.
    echo Trying without --quiet flag to see the error...
    python -m pip install -r requirements.txt
    cd ..
    pause
    exit /b 1
)
cd ..

echo.
echo Dependencies installed successfully!
echo.
echo ========================================
echo   Starting Flask Server
echo ========================================
echo.
echo Server will start on: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.
echo Opening browser in 3 seconds...
timeout /t 3 /nobreak >nul
start http://localhost:5000
echo.

REM Start the Flask server
cd backend
python server.py

REM If we get here, the server stopped
cd ..
echo.
echo Server stopped.
pause
