# 🚀 Quick Deployment Steps

## TL;DR - Get Your App Online in 15 Minutes

### Part 1: Deploy Backend (5 minutes)

1. **Go to Render.com** → Sign up with GitHub
2. **New Web Service** → Select this repo
3. **Configure**:
   - Root Directory: `backend`
   - Build: `pip install -r requirements.txt`
   - Start: `python server.py`
4. **Copy your URL**: `https://your-app-name.onrender.com`

### Part 2: Deploy Frontend (10 minutes)

1. **Update config**:
   ```javascript
   // In frontend/assets/js/config.js
   API_BASE_URL: 'https://your-app-name.onrender.com/api/funds'
   ```

2. **Run deployment script**:
   ```bash
   prepare-github-pages.bat
   ```

3. **Commit and push**:
   ```bash
   git add .
   git commit -m "Deploy to GitHub Pages"
   git push origin gh-pages
   ```

4. **Enable GitHub Pages**:
   - Repo → Settings → Pages
   - Branch: gh-pages → /root
   - Save

5. **Done!** Visit: `https://yourusername.github.io/cal-fund-analyzer/`

---

## ⚠️ First Request Takes 30s

Render free tier "sleeps" after 15 min inactivity. First request wakes it up (30-60s).

---

## 💰 Cost: $0/month Forever!

Both services are 100% free for this use case.

---

**Full guide:** See `DEPLOYMENT_GUIDE.md` for detailed instructions.

