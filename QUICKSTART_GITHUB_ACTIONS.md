# 🚀 QUICK START - Automated Deployment

## 🎯 Goal
Set up automated deployment for CAL Fund Analyzer in **~15 minutes**.

---

## ⚡ Super Quick Setup

### **Step 1: Deploy Backend** (5 min)

1. Go to [render.com](https://render.com) → Sign up
2. **New +** → **Web Service** → Connect GitHub
3. Settings:
   - Root: `backend`
   - Build: `pip install -r requirements.txt`
   - Start: `python server.py`
   - Plan: **Free**
4. **Create** → Wait 5 min → Copy URL

### **Step 2: Get Deploy Hook** (1 min)

1. Render → Your Service → **Settings**
2. Scroll to "Deploy Hook" → **Create**
3. Copy hook URL

### **Step 3: GitHub Secrets** (2 min)

GitHub Repo → **Settings** → **Secrets and variables** → **Actions**

Add 2 secrets:

| Name | Value |
|------|-------|
| `BACKEND_URL` | `https://YOUR-APP.onrender.com` |
| `RENDER_DEPLOY_HOOK_URL` | `https://api.render.com/deploy/...` |

### **Step 4: Enable Pages** (1 min)

GitHub Repo → **Settings** → **Pages** → Source: **GitHub Actions**

### **Step 5: Test!** (2 min)

```bash
git checkout -b test-deploy
echo "test" >> README.md
git add . && git commit -m "test"
git push origin test-deploy
```

Create PR → Merge → Watch **Actions** tab → Done! ✅

---

## ⏱️ What Happens Next

After merge:
1. 🚀 Backend deploys (5-10 min)
2. ✅ Verifies backend health
3. 📄 Frontend deploys to Pages (2 min)
4. 🧪 Tests all endpoints
5. 🎉 **LIVE!**

---

## 🔗 URLs After Deployment

- **Backend**: `https://YOUR-APP.onrender.com`
- **Frontend**: `https://YOUR-USERNAME.github.io/cal-fund-analyzer/`
- **API Version**: `https://YOUR-APP.onrender.com/api/version`

---

## ❌ Troubleshooting

**Workflow fails?**
1. Check secrets (no typos, no trailing slashes)
2. Test backend: `curl YOUR-BACKEND-URL/api/health`
3. Check workflow logs in Actions tab

**Need detailed help?**
- 📚 [Complete Guide](GITHUB_ACTIONS_SETUP.md)
- ✅ [Checklist](DEPLOYMENT_CHECKLIST.md)
- 📖 [Summary](GITHUB_ACTIONS_SUMMARY.md)

---

## 🎉 That's It!

Now every PR merge auto-deploys! 🚀

No more manual deployments. Just code → merge → live!

