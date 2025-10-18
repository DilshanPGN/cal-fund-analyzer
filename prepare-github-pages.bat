@echo off
echo ========================================
echo   Prepare Frontend for GitHub Pages
echo ========================================
echo.
echo This script will:
echo 1. Create gh-pages branch
echo 2. Copy frontend files to root
echo 3. Clean up unnecessary files
echo.
echo Before running, make sure:
echo - All changes are committed
echo - You have your Render backend URL
echo.
pause

echo.
echo [Step 1] Creating gh-pages branch...
git checkout -b gh-pages

if %ERRORLEVEL% NEQ 0 (
    echo Branch might already exist, checking it out...
    git checkout gh-pages
)

echo.
echo [Step 2] Copying frontend files to root...
xcopy /E /I /Y frontend\* .

echo.
echo [Step 3] Cleaning up...
rmdir /S /Q backend 2>nul
rmdir /S /Q desktop 2>nul
rmdir /S /Q scripts 2>nul
rmdir /S /Q data 2>nul
del /Q *.md 2>nul
del /Q *.bat 2>nul

echo.
echo ========================================
echo   IMPORTANT: Update Configuration!
echo ========================================
echo.
echo Open: assets\js\config.js
echo.
echo Change API_BASE_URL to your Render URL:
echo   API_BASE_URL: 'https://YOUR-APP-NAME.onrender.com/api/funds'
echo.
echo Then run:
echo   git add .
echo   git commit -m "Deploy to GitHub Pages"
echo   git push origin gh-pages
echo.
pause

