# 🤖 GitHub Actions Workflows

This directory contains automated CI/CD workflows for the CAL Fund Analyzer.

---

## 📋 Available Workflows

### **`deploy.yml` - Production Deployment**

Automatically deploys the full stack when PRs are merged.

**Triggers:**
- Push to `main`, `production`, or `deployment` branch
- Manual trigger via Actions tab

**Jobs:**
1. **Deploy Backend** → Render.com
2. **Deploy Frontend** → GitHub Pages (after backend verification)
3. **Verify Full Stack** → Test all endpoints

**Duration:** ~8-15 minutes

---

## 🔧 Setup Required

Before workflows can run, you must configure:

### **GitHub Secrets** (Settings → Secrets and variables → Actions)

| Secret | Required | Description | Example |
|--------|----------|-------------|---------|
| `BACKEND_URL` | ✅ Yes | Your Render backend URL | `https://cal-fund-analyzer.onrender.com` |
| `RENDER_DEPLOY_HOOK_URL` | ✅ Yes | Render deploy hook URL | `https://api.render.com/deploy/srv-xxx?key=xxx` |
| `CUSTOM_DOMAIN` | ❌ No | Custom domain for GitHub Pages | `cal-fund.example.com` |

### **GitHub Pages** (Settings → Pages)

- Source: **GitHub Actions**

---

## 📊 Workflow Status

View workflow status:
- **Actions** tab → **Deploy to Production**
- Green ✅ = Success
- Red ❌ = Failed
- Yellow 🟡 = Running

---

## 🧪 Testing Workflows

### **Option 1: Create Test PR**
```bash
git checkout -b test-deployment
echo "# Test" >> README.md
git add . && git commit -m "test: deployment"
git push origin test-deployment
# Create and merge PR on GitHub
```

### **Option 2: Manual Trigger**
1. Go to **Actions** tab
2. Select **"Deploy to Production"**
3. Click **"Run workflow"**
4. Choose branch and click **"Run workflow"**

---

## 🔍 Debugging Failed Deployments

### **Backend Job Failed**

Check:
1. Render dashboard for deployment errors
2. `BACKEND_URL` secret is correct (no trailing slash)
3. `RENDER_DEPLOY_HOOK_URL` is valid
4. Backend responds at `/api/version`

### **Frontend Job Failed**

Check:
1. GitHub Pages is enabled and set to "GitHub Actions"
2. You have Pages write permissions
3. `backend/routes/api.py` has `/api/version` endpoint

### **Verification Job Failed**

Check:
1. Backend is actually running on Render
2. CORS is configured correctly
3. Test endpoints manually with `curl`

---

## 📚 Documentation

For complete setup instructions, see:
- **[GitHub Actions Setup Guide](../docs/GITHUB_ACTIONS_SETUP.md)**
- **[Deployment Guide](../docs/DEPLOYMENT_GUIDE.md)**

---

## 🎯 Quick Reference

### **View Logs**
```
Actions tab → Select workflow run → Click job → View logs
```

### **Test Backend Version Endpoint**
```bash
curl https://YOUR-BACKEND-URL.onrender.com/api/version
```

### **Test Frontend**
```
https://YOUR-USERNAME.github.io/cal-fund-analyzer/
```

---

## 🔐 Security

- **Never commit** secrets to repository
- **Use GitHub Secrets** for sensitive data
- **Enable branch protection** on main branch
- **Review** deployment logs regularly

---

## 🚀 Next Steps

1. ✅ Set up GitHub Secrets
2. ✅ Enable GitHub Pages
3. ✅ Run test deployment
4. ✅ Monitor first deployment
5. ✅ Configure branch protection

**Need help?** Check [GITHUB_ACTIONS_SETUP.md](../docs/GITHUB_ACTIONS_SETUP.md)

