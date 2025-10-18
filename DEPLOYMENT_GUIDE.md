# 🚀 Deployment Guide - GitHub Pages + Render.com

Complete guide to deploy your CAL Fund Analyzer with split hosting.

---

## 📋 Overview

- **Frontend**: GitHub Pages (Free, Static hosting)
- **Backend**: Render.com (Free tier, Python hosting)

---

## Part 1: Deploy Backend to Render.com

### Step 1: Sign Up for Render

1. Go to https://render.com
2. Sign up with GitHub account (easiest)
3. Authorize Render to access your repositories

### Step 2: Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `cal-fund-analyzer`
3. Configure:
   ```
   Name: cal-fund-analyzer-backend
   Region: Choose closest to you
   Branch: Development
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python server.py
   ```
4. Select **"Free"** plan
5. Click **"Create Web Service"**

### Step 3: Wait for Deployment

- Render will build and deploy (takes 2-5 minutes)
- You'll get a URL like: `https://cal-fund-analyzer-backend.onrender.com`
- **Copy this URL** - you'll need it!

### Step 4: Test Backend

Visit in browser:
```
https://your-app-name.onrender.com/api/health
```

Should return:
```json
{
  "status": "healthy",
  "api_accessible": true,
  "timestamp": "2025-10-18T..."
}
```

✅ **Backend is deployed!**

---

## Part 2: Deploy Frontend to GitHub Pages

### Step 1: Create gh-pages Branch

```bash
# Create and checkout gh-pages branch
git checkout -b gh-pages

# Copy frontend files to root
xcopy /E /I frontend\* .

# Or on Mac/Linux:
# cp -r frontend/* .

# Delete backend and other folders
rmdir /S /Q backend
rmdir /S /Q desktop
rmdir /S /Q scripts

# Or on Mac/Linux:
# rm -rf backend desktop scripts data docs
```

### Step 2: Update Configuration

Edit `assets/js/config.js` and replace `API_BASE_URL` with your Render URL:

```javascript
const CONFIG = {
    API_BASE_URL: 'https://cal-fund-analyzer-backend.onrender.com/api/funds',
    // ... rest stays the same
};
```

### Step 3: Commit and Push

```bash
git add .
git commit -m "Deploy frontend to GitHub Pages"
git push origin gh-pages
```

### Step 4: Enable GitHub Pages

1. Go to your GitHub repository
2. Settings → Pages
3. Source: **Deploy from branch**
4. Branch: **gh-pages** → **/root**
5. Click **Save**

### Step 5: Wait and Access

- GitHub will build (takes 1-2 minutes)
- Your site will be at: `https://yourusername.github.io/cal-fund-analyzer/`

✅ **Frontend is deployed!**

---

## 🧪 Testing Your Deployment

1. **Open your GitHub Pages URL**
2. **Select a fund** from dropdown
3. **Click "Fetch New Data"**
4. **Watch data load** - it's calling your Render backend!
5. **Try analysis features**
6. **Export CSV/PNG**

---

## ⚠️ Important Notes

### Render Free Tier Limitations

- **Spins down after 15 minutes** of inactivity
- **First request after sleep** takes 30-60 seconds to wake up
- **750 hours/month** of runtime (plenty for personal use)

### Solution for Cold Starts

Add this to your frontend to show a warming message:

```javascript
// In app.js, before first API call
if (firstRequest) {
    this.showLoading('⏳ Waking up backend server... (first request takes 30s)');
}
```

---

## 🔧 Environment Variables (Optional)

If you want to make the backend URL configurable:

### On Render:
1. Dashboard → Your Service → Environment
2. Add: `FRONTEND_URL` = `https://yourusername.github.io`
3. Update config.py to use this

---

## 🔄 Updating Your App

### Update Backend:
```bash
git checkout Development
# Make changes to backend/
git add .
git commit -m "Update backend"
git push origin Development
```
Render auto-deploys on push!

### Update Frontend:
```bash
git checkout gh-pages
# Make changes
git add .
git commit -m "Update frontend"
git push origin gh-pages
```
GitHub Pages auto-deploys!

---

## 💰 Cost Summary

| Service | Cost | Limits |
|---------|------|--------|
| GitHub Pages | **FREE** | 100GB bandwidth/month |
| Render.com | **FREE** | 750 hours/month, 512MB RAM |
| **TOTAL** | **$0/month** | ✅ Free forever! |

---

## 🐛 Troubleshooting

### Backend won't start on Render:
```
Check Logs → Look for errors
Common: Missing dependencies in requirements.txt
```

### CORS errors:
```
Check backend/config.py → CORS_ORIGINS includes your GitHub Pages URL
```

### Backend sleeping:
```
This is normal on free tier
First request takes 30-60s to wake up
Consider paid tier ($7/month) for always-on
```

### GitHub Pages 404:
```
Make sure index.html is in root of gh-pages branch
Check Settings → Pages → Source is correct
```

---

## 🎉 Success Checklist

- [ ] Render account created
- [ ] Backend deployed to Render
- [ ] Backend health check returns "healthy"
- [ ] GitHub Pages enabled
- [ ] Frontend config updated with Render URL
- [ ] Frontend pushed to gh-pages branch
- [ ] GitHub Pages site accessible
- [ ] Can select fund and fetch data
- [ ] Analysis features work
- [ ] Export features work

---

## 📚 Additional Resources

- **Render Docs**: https://render.com/docs
- **GitHub Pages Docs**: https://docs.github.com/en/pages
- **Flask Deployment**: https://flask.palletsprojects.com/en/latest/deploying/

---

**Your app is now live and accessible from anywhere in the world! 🌍**

