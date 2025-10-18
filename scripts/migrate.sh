#!/bin/bash

echo "========================================"
echo "  File Migration to New Structure"
echo "========================================"
echo ""
echo "This script will reorganize files into clean architecture"
echo ""
read -p "Press Enter to continue..."

# Create necessary directories
echo "Creating directories..."
mkdir -p frontend/assets/css
mkdir -p desktop
mkdir -p docs
mkdir -p data

echo ""
echo "Moving files..."

# Move frontend files
if [ -f "styles.css" ]; then
    echo "Moving styles.css to frontend/assets/css/"
    mv styles.css frontend/assets/css/
fi

if [ -f "index.html" ]; then
    echo "Moving index.html to frontend/"
    mv index.html frontend/
fi

# Move desktop files
if [ -f "cal_fund_extractor.py" ]; then
    echo "Moving cal_fund_extractor.py to desktop/"
    mv cal_fund_extractor.py desktop/
fi

if [ -f "png_updater.py" ]; then
    echo "Moving png_updater.py to desktop/"
    mv png_updater.py desktop/
fi

if [ -f "requirements.txt" ]; then
    echo "Copying requirements.txt to desktop/"
    cp requirements.txt desktop/requirements.txt
fi

if [ -f "install_instructions.md" ]; then
    echo "Moving install_instructions.md to desktop/"
    mv install_instructions.md desktop/
fi

# Move documentation
[ -f "README_WEB.md" ] && mv README_WEB.md docs/
[ -f "DEPLOYMENT.md" ] && mv DEPLOYMENT.md docs/
[ -f "QUICKSTART_WEB.md" ] && mv QUICKSTART_WEB.md docs/
[ -f "WORKING_SOLUTION.md" ] && mv WORKING_SOLUTION.md docs/
[ -f "PROJECT_CLEANUP.md" ] && mv PROJECT_CLEANUP.md docs/

# Move data files
echo "Moving data files to data/..."
mv *.csv data/ 2>/dev/null
mv *.png data/ 2>/dev/null
mv *.zip data/ 2>/dev/null

# Clean up old files
echo ""
echo "Cleaning up old files..."
[ -f "server.py" ] && rm server.py
[ -f "requirements_server.txt" ] && rm requirements_server.txt
[ -f "start_fullstack.bat" ] && rm start_fullstack.bat
[ -f "start_fullstack.sh" ] && rm start_fullstack.sh

if [ -f "app.js" ]; then
    echo "Backing up old app.js to app.js.backup"
    mv app.js app.js.backup
fi

echo ""
echo "========================================"
echo "  Migration Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Check that files are in correct locations"
echo "2. Run: ./scripts/start.sh"
echo "3. Open browser to: http://localhost:5000"
echo ""
echo "Old app.js backed up to: app.js.backup"
echo ""

