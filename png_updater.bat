@echo off
REM CAL Fund PNG Updater - Windows Batch Script
REM This script provides easy access to PNG updater functionality

echo CAL Fund PNG Updater
echo ====================

if "%1"=="help" goto :help
if "%1"=="status" goto :status
if "%1"=="monitor" goto :monitor
if "%1"=="update" goto :update
if "%1"=="" goto :update

:help
echo Usage: png_updater.bat [command]
echo.
echo Commands:
echo   help     - Show this help message
echo   status   - Show status of CSV and PNG files
echo   monitor  - Monitor CSV files and auto-update PNGs
echo   update   - Update PNG files for all CSV files (default)
echo.
echo Examples:
echo   png_updater.bat           # Update all files
echo   png_updater.bat status    # Show file status
echo   png_updater.bat monitor   # Start monitoring
goto :end

:status
python png_updater.py --status
goto :end

:monitor
python png_updater.py --monitor
goto :end

:update
python png_updater.py --all
goto :end

:end
pause
