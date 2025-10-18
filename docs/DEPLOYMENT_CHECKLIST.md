# ✅ GitHub Actions Deployment Checklist

Use this checklist to set up automated deployment for the CAL Fund Analyzer.

---

## 📋 Pre-Deployment Checklist

### **1. Backend Setup on Render.com** ⏱️ 10 minutes

- [ ] Go to [render.com](https://render.com) and sign up/login
- [ ] Click **"New +"** → **"Web Service"**
- [ ] Connect your GitHub repository
- [ ] Configure service:
  - [ ] **Name**: `cal-fund-analyzer`
  - [ ] **Root Directory**: `backend`
  - [ ] **Build Command**: `pip install -r requirements.txt`
  - [ ] **Start Command**: `python server.py`
  - [ ] **Plan**: Free
- [ ] Click **"Create Web Service"**
- [ ] Wait for first deployment (~5 minutes)
- [ ] Copy backend URL: `https://__________.onrender.com`
- [ ] Test backend: Open `https://YOUR-URL.onrender.com/api/health`

---

### **2. Get Render Deploy Hook** ⏱️ 2 minutes

- [ ] In Render dashboard, go to your web service
- [ ] Click **"Settings"** (left sidebar)
- [ ] Scroll to **"Deploy Hook"** section
- [ ] Click **"Create Deploy Hook"**
- [ ] Copy deploy hook URL (starts with `https://api.render.com/deploy/`)

---

### **3. Configure GitHub Secrets** ⏱️ 3 minutes

- [ ] Go to your GitHub repository
- [ ] Click **Settings** → **Secrets and variables** → **Actions**
- [ ] Add these secrets:

#### Secret 1: BACKEND_URL
- [ ] Click **"New repository secret"**
- [ ] Name: `BACKEND_URL`
- [ ] Value: Your Render URL (e.g., `https://cal-fund-analyzer.onrender.com`)
- [ ] **Important**: No trailing slash!
- [ ] Click **"Add secret"**

#### Secret 2: RENDER_DEPLOY_HOOK_URL
- [ ] Click **"New repository secret"**
- [ ] Name: `RENDER_DEPLOY_HOOK_URL`
- [ ] Value: Your deploy hook URL from Step 2
- [ ] Click **"Add secret"**

#### Secret 3: CUSTOM_DOMAIN (Optional)
- [ ] If using custom domain for GitHub Pages
- [ ] Click **"New repository secret"**
- [ ] Name: `CUSTOM_DOMAIN`
- [ ] Value: Your domain (e.g., `cal-fund.example.com`)
- [ ] Click **"Add secret"**

---

### **4. Enable GitHub Pages** ⏱️ 2 minutes

- [ ] Go to your GitHub repository
- [ ] Click **Settings** → **Pages** (left sidebar)
- [ ] Under **"Source"**:
  - [ ] Select **"GitHub Actions"** (NOT "Deploy from a branch")
- [ ] Click **"Save"**
- [ ] Note your GitHub Pages URL: `https://YOUR-USERNAME.github.io/cal-fund-analyzer/`

---

### **5. Verify Workflow Files** ⏱️ 1 minute

Check these files exist in your repository:

- [ ] `.github/workflows/deploy.yml` ✅
- [ ] `backend/routes/api.py` has `/api/version` endpoint ✅
- [ ] `docs/GITHUB_ACTIONS_SETUP.md` exists ✅

---

## 🚀 First Deployment

### **Option A: Test with Sample PR** (Recommended)

- [ ] Create a new branch:
  ```bash
  git checkout -b test-deployment
  ```
- [ ] Make a small change:
  ```bash
  echo "# Automated Deployment Test" >> README.md
  git add README.md
  git commit -m "test: GitHub Actions deployment"
  git push origin test-deployment
  ```
- [ ] Go to GitHub → Create Pull Request
- [ ] Merge PR to `main` branch
- [ ] Go to **Actions** tab
- [ ] Watch the **"Deploy to Production"** workflow run
- [ ] Wait for all jobs to complete (~8-15 minutes)

---

### **Option B: Manual Trigger**

- [ ] Go to **Actions** tab in GitHub
- [ ] Click **"Deploy to Production"** workflow
- [ ] Click **"Run workflow"** button
- [ ] Select branch (`main` or `deployment`)
- [ ] Click green **"Run workflow"** button
- [ ] Watch the workflow execute

---

## ✅ Post-Deployment Verification

### **1. Check Workflow Status**

- [ ] All 3 jobs completed successfully (green ✅)
- [ ] No failed steps (red ❌)
- [ ] Check Summary tab for deployment info

---

### **2. Test Backend**

- [ ] Open: `https://YOUR-BACKEND-URL.onrender.com/api/version`
- [ ] Should return JSON with version info
- [ ] Check for `"status": "running"`

Example test:
```bash
curl https://YOUR-BACKEND-URL.onrender.com/api/version | jq
```

Expected response:
```json
{
  "version": "1.0.0",
  "commit": "a1b2c3d",
  "branch": "main",
  "environment": "production",
  "python_version": "3.9.x",
  "timestamp": "2025-10-18T...",
  "service": "CAL Fund Analyzer Backend",
  "status": "running"
}
```

---

### **3. Test Frontend**

- [ ] Open: `https://YOUR-USERNAME.github.io/cal-fund-analyzer/`
- [ ] Page loads without errors
- [ ] Fund dropdown populates
- [ ] Can select a fund
- [ ] Can fetch data (test with "Fetch New Data" button)
- [ ] Chart displays correctly

---

### **4. Test Full Integration**

- [ ] Open browser DevTools (F12)
- [ ] Go to Network tab
- [ ] Fetch data for a fund
- [ ] Check requests go to your Render backend
- [ ] Verify no CORS errors
- [ ] Check localStorage has data

---

## 🔧 Troubleshooting

### **Workflow Fails at "Deploy Backend"**

**Symptoms**: "curl: Failed to connect" or timeout

**Solutions**:
- [ ] Verify `RENDER_DEPLOY_HOOK_URL` is correct
- [ ] Check Render dashboard for errors
- [ ] Ensure backend is not sleeping (free tier)

---

### **Workflow Fails at "Verify Backend"**

**Symptoms**: "Backend deployment timeout"

**Solutions**:
- [ ] Check `BACKEND_URL` secret (no trailing slash)
- [ ] Test manually: `curl YOUR-BACKEND-URL/api/version`
- [ ] Check Render logs for errors
- [ ] Verify `/api/version` endpoint exists in code

---

### **Workflow Fails at "Deploy Frontend"**

**Symptoms**: "No deployment found for environment"

**Solutions**:
- [ ] Verify GitHub Pages source is set to "GitHub Actions"
- [ ] Check repository has Pages enabled
- [ ] Verify workflow has Pages write permissions
- [ ] Try disabling and re-enabling Pages

---

### **Frontend Can't Connect to Backend**

**Symptoms**: CORS errors in browser console

**Solutions**:
- [ ] Verify `backend/config.py` has correct CORS origins
- [ ] Check `BACKEND_URL` secret is correct
- [ ] Test backend directly: `curl YOUR-BACKEND-URL/api/health`
- [ ] Check browser DevTools Network tab for actual URL called

---

## 🎉 Success Criteria

Your deployment is successful when:

- [ ] ✅ Workflow completes without errors
- [ ] ✅ Backend responds at `/api/version`
- [ ] ✅ Backend responds at `/api/health`
- [ ] ✅ Frontend loads on GitHub Pages
- [ ] ✅ Fund dropdown populates
- [ ] ✅ Can fetch and display data
- [ ] ✅ Chart renders correctly
- [ ] ✅ No CORS errors in console
- [ ] ✅ Data saves to localStorage

---

## 📊 Next Steps

After successful first deployment:

- [ ] Configure branch protection on `main`
- [ ] Set up PR templates
- [ ] Add status badges to README
- [ ] Configure custom domain (optional)
- [ ] Set up monitoring/alerting (optional)
- [ ] Test deployment with actual feature PR

---

## 🔗 Helpful Links

- **Render Dashboard**: https://dashboard.render.com
- **GitHub Actions**: `https://github.com/YOUR-USERNAME/cal-fund-analyzer/actions`
- **GitHub Pages**: `https://YOUR-USERNAME.github.io/cal-fund-analyzer/`
- **Backend URL**: `https://YOUR-BACKEND-URL.onrender.com`

---

## 📞 Need Help?

If you get stuck:

1. **Check workflow logs** in Actions tab (detailed error messages)
2. **Check Render logs** in Render dashboard
3. **Test endpoints manually** with `curl`
4. **Review** [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) for detailed guide
5. **Verify secrets** are set correctly (no typos, no trailing slashes)

---

## 🎓 Congratulations!

Once all items are checked, you have:

✅ Automated CI/CD pipeline  
✅ Backend on Render.com  
✅ Frontend on GitHub Pages  
✅ Full-stack web app live and accessible  
✅ Zero-cost hosting  
✅ Auto-deploy on every PR merge  

**Your app is production-ready! 🎉**

