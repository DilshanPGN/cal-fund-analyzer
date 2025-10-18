# 🔧 Setup Troubleshooting Guide

## ❗ You Got an Error - Let's Fix It!

You saw this error:
```
The system cannot find the path specified.
'pip' is not recognized as an internal or external command
```

This happens because either:
1. **Migration hasn't been run yet** (backend folder doesn't exist)
2. **Python isn't installed** or not in PATH

---

## ✅ SOLUTION: Use the All-In-One Setup Script

I've created a script that does EVERYTHING for you:

### Just run this:
```bash
SETUP_AND_RUN.bat
```

This script will:
1. ✅ Check if Python is installed
2. ✅ Create the new folder structure
3. ✅ Move files to correct locations
4. ✅ Install dependencies
5. ✅ Start the application
6. ✅ Open your browser

**That's it! One script does it all!** 🎉

---

## 🐍 If Python Isn't Installed

### Step 1: Download Python
Go to: https://www.python.org/downloads/

### Step 2: Install Python
**IMPORTANT:** During installation, check the box:
```
☑️ Add Python to PATH
```

This is critical! Without this, Windows won't find Python.

### Step 3: Verify Installation
Open a new Command Prompt and type:
```bash
python --version
```

You should see something like:
```
Python 3.11.x
```

### Step 4: Run Setup
Now run:
```bash
SETUP_AND_RUN.bat
```

---

## 📁 Alternative: Manual Step-by-Step

If the automated script doesn't work, here's the manual process:

### Step 1: Check Python
```bash
python --version
```

If this fails, install Python (see above).

### Step 2: Create Backend Folders
```bash
mkdir backend\services
mkdir backend\routes
mkdir frontend\assets\css
mkdir frontend\assets\js\services
mkdir frontend\assets\js\components
mkdir frontend\assets\js\utils
```

### Step 3: Install Dependencies
```bash
cd backend
python -m pip install Flask==2.3.2 Flask-Cors==4.0.0 requests==2.31.0
cd ..
```

### Step 4: Start Server
```bash
cd backend
python server.py
```

### Step 5: Open Browser
Go to: http://localhost:5000

---

## 🚀 Quick Command Reference

| Problem | Solution |
|---------|----------|
| Backend folder missing | Run `SETUP_AND_RUN.bat` |
| Python not found | Install from python.org |
| pip not found | Use `python -m pip` instead |
| Port already in use | Change port in `backend/config.py` |

---

## 📞 Still Having Issues?

### Check Python Installation:
```bash
python --version
python -m pip --version
```

Both should work. If not, reinstall Python with "Add to PATH" checked.

### Check Current Directory:
Make sure you're in the project root folder (where README.md is):
```bash
dir
```

You should see:
- backend/
- frontend/
- scripts/
- README.md

### Check Backend Files:
```bash
dir backend
```

You should see:
- server.py
- config.py
- requirements.txt
- services/
- routes/

---

## 💡 Pro Tip

The **SETUP_AND_RUN.bat** script is the easiest way!

It checks everything, fixes what it can, and gives clear error messages for what it can't fix.

Just double-click it or run:
```bash
SETUP_AND_RUN.bat
```

---

## ✅ Success Checklist

After running setup, you should see:
- ✅ "Found Python: 3.x.x"
- ✅ "Dependencies installed!"
- ✅ "Starting Flask server..."
- ✅ Browser opens to localhost:5000
- ✅ Fund analyzer loads

---

**Having trouble? The most common issue is Python not being installed or not in PATH. Install Python with "Add to PATH" checked, then run SETUP_AND_RUN.bat!**

