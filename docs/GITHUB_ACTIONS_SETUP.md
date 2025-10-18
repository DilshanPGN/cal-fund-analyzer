# 🤖 GitHub Actions Automated Deployment Setup

This guide will help you set up automated deployment for the CAL Fund Analyzer using GitHub Actions.

---

## 📋 Overview

The automated deployment workflow:

1. **Triggers** when you merge a PR to `main`, `production`, or `deployment` branch
2. **Deploys Backend** to Render.com via deploy hook
3. **Verifies Backend** by calling the `/api/version` endpoint
4. **Deploys Frontend** to GitHub Pages (only after backend is verified)
5. **Verifies Full Stack** by testing all endpoints

---

## 🔧 Setup Steps

### **1. Deploy Backend to Render.com First**

Before setting up GitHub Actions, manually deploy your backend once:

1. Go to [render.com](https://render.com) and sign up
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `cal-fund-analyzer` (or your choice)
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python server.py`
   - **Plan**: Free

5. Click **"Create Web Service"**
6. Wait for deployment (5-10 minutes)
7. Copy your backend URL (e.g., `https://cal-fund-analyzer.onrender.com`)

---

### **2. Get Render Deploy Hook**

1. In your Render dashboard, go to your web service
2. Click **"Settings"** in the left sidebar
3. Scroll down to **"Deploy Hook"**
4. Click **"Create Deploy Hook"**
5. Copy the deploy hook URL (looks like: `https://api.render.com/deploy/srv-xxxxx?key=xxxxxx`)

---

### **3. Configure GitHub Secrets**

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"** and add these secrets:

| Secret Name | Value | Example |
|-------------|-------|---------|
| `BACKEND_URL` | Your Render backend URL | `https://cal-fund-analyzer.onrender.com` |
| `RENDER_DEPLOY_HOOK_URL` | Your Render deploy hook URL | `https://api.render.com/deploy/srv-xxxxx?key=xxxxxx` |
| `CUSTOM_DOMAIN` | (Optional) Your custom domain | `cal-fund.example.com` |

**Important**: Do NOT include trailing slashes in URLs!

---

### **4. Enable GitHub Pages**

1. Go to your GitHub repository
2. Click **Settings** → **Pages**
3. Under **"Source"**, select **"GitHub Actions"**
4. Click **"Save"**

---

### **5. Test the Workflow**

#### **Option A: Merge a PR (Recommended)**
```bash
# Create a feature branch
git checkout -b test-deployment

# Make a small change
echo "# Test deployment" >> README.md

# Commit and push
git add .
git commit -m "Test: trigger deployment workflow"
git push origin test-deployment

# Create PR on GitHub and merge to main/deployment branch
```

#### **Option B: Manual Trigger**
1. Go to **Actions** tab in GitHub
2. Click **"Deploy to Production"**
3. Click **"Run workflow"**
4. Select branch and click **"Run workflow"**

---

## 📊 Workflow Details

### **Job 1: Deploy Backend** (5-10 minutes)
- Triggers Render deployment via webhook
- Waits 30 seconds for deployment to start
- Polls `/api/version` endpoint every 10 seconds (max 5 minutes)
- Extracts and displays version info
- Fails if backend doesn't respond in 5 minutes

### **Job 2: Deploy Frontend** (2-3 minutes)
- Only runs after backend is verified
- Auto-generates `config.production.js` with correct backend URL
- Uploads frontend files to GitHub Pages
- Deploys to GitHub Pages

### **Job 3: Verify Deployment** (30 seconds)
- Tests `/api/version` endpoint
- Tests `/api/health` endpoint
- Tests `/api/funds` endpoint
- Creates deployment summary

---

## 🎯 Version Endpoint

The workflow uses the `/api/version` endpoint to verify deployment:

**Example Response:**
```json
{
  "version": "1.0.0",
  "commit": "a1b2c3d",
  "branch": "main",
  "environment": "production",
  "python_version": "3.9.6",
  "timestamp": "2025-10-18T10:30:00",
  "service": "CAL Fund Analyzer Backend",
  "status": "running"
}
```

**Test it locally:**
```bash
# Start your backend
cd backend
python server.py

# In another terminal
curl http://localhost:5000/api/version | jq
```

---

## 🔍 Monitoring Deployments

### **View Deployment Status**

1. Go to **Actions** tab in GitHub
2. Click on the running workflow
3. Watch real-time logs for each job

### **Deployment Summary**

After successful deployment, check the **Summary** tab to see:
- Backend URL and version
- Frontend URL
- All tested endpoints
- Deployment timestamp

---

## 🚨 Troubleshooting

### **Backend Verification Fails**

**Error**: "Backend deployment timeout - failed to respond after 5 minutes"

**Solutions**:
1. Check Render logs for errors
2. Verify `BACKEND_URL` secret is correct (no trailing slash)
3. Ensure backend deployed successfully on Render
4. Check if Render free tier is sleeping (first request takes longer)

### **Frontend Deployment Fails**

**Error**: "Error: No deployment found for the environment"

**Solutions**:
1. Ensure GitHub Pages is set to "GitHub Actions" source
2. Check repository has Pages enabled
3. Verify you have Pages write permissions

### **API Tests Fail**

**Error**: "Funds endpoint returned invalid JSON"

**Solutions**:
1. Test backend manually: `curl YOUR_BACKEND_URL/api/funds?valuedate=2024-01-01`
2. Check if CAL API is accessible from Render
3. Check backend logs for CORS errors

---

## ⚙️ Workflow Configuration

### **Trigger Branches**

Edit `.github/workflows/deploy.yml` to change trigger branches:

```yaml
on:
  push:
    branches:
      - main           # Production
      - production     # Production alternative
      - deployment     # Deployment branch
```

### **Backend Wait Time**

Adjust max wait time for backend (default: 5 minutes):

```yaml
# In deploy.yml
max_attempts=30  # 30 attempts * 10 seconds = 5 minutes
```

### **Custom Domain**

If using a custom domain for GitHub Pages:

1. Add `CUSTOM_DOMAIN` secret in GitHub
2. Workflow will auto-create `CNAME` file

---

## 📁 Files Created

### **`.github/workflows/deploy.yml`**
Main deployment workflow with 3 jobs

### **`backend/routes/api.py`**
Added `/api/version` endpoint

### **`frontend/assets/js/config.production.js`**
Auto-generated during deployment with correct backend URL

---

## 🎉 What Happens After Merge

```
PR merged to main
       ↓
┌──────────────────┐
│ Deploy Backend   │ (5-10 min)
│ → Render.com     │
└──────────────────┘
       ↓
┌──────────────────┐
│ Verify Backend   │ (30 sec)
│ → /api/version   │
└──────────────────┘
       ↓
┌──────────────────┐
│ Deploy Frontend  │ (2-3 min)
│ → GitHub Pages   │
└──────────────────┘
       ↓
┌──────────────────┐
│ Verify Full Stack│ (30 sec)
│ → Test All APIs  │
└──────────────────┘
       ↓
    ✅ DONE!
```

**Total Time**: ~8-15 minutes

---

## 🔐 Security Best Practices

1. **Never commit secrets** to your repository
2. **Use GitHub Secrets** for all sensitive data
3. **Rotate deploy hooks** periodically
4. **Review deployment logs** for suspicious activity
5. **Enable branch protection** on main/production branches

---

## 🚀 Advanced: Manual Deployment

If you prefer to deploy manually:

### **Backend Only**
```bash
curl -X POST "$RENDER_DEPLOY_HOOK_URL"
```

### **Frontend Only**
```bash
# Run the workflow with only frontend job
# (requires editing workflow or manual upload)
```

---

## 📞 Support

**Issues?**
1. Check workflow logs in GitHub Actions
2. Check Render logs in Render dashboard
3. Verify all secrets are set correctly
4. Test endpoints manually with `curl`

**Workflow failing?**
- Check backend deployment on Render first
- Verify `/api/version` returns valid JSON
- Ensure GitHub Pages is enabled

---

## 🎓 Next Steps

✅ Complete setup steps above  
✅ Test with a small PR  
✅ Monitor first deployment  
✅ Configure branch protection  
✅ Set up custom domain (optional)  
✅ Add deployment notifications (optional)  

**Congratulations! Your app now deploys automatically on every merge! 🎉**

