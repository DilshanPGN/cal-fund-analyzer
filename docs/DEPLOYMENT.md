# GitHub Pages Deployment Guide 🚀

This guide will help you deploy the CAL Fund Analyzer web application to GitHub Pages.

## 📋 Prerequisites

- A GitHub account
- Basic Git knowledge (or use GitHub Desktop/Web UI)
- The web app files: `index.html`, `app.js`, `styles.css`

## 🎯 Deployment Methods

### Method 1: Using Git Command Line (Recommended)

#### Step 1: Prepare Your Repository

```bash
# Navigate to your project directory
cd cal-fund-analyzer

# Initialize Git (if not already done)
git init

# Add your files
git add index.html app.js styles.css README_WEB.md

# Commit your changes
git commit -m "Initial commit: Web application"

# Create main branch (if needed)
git branch -M main
```

#### Step 2: Push to GitHub

```bash
# Add remote repository (replace with your username)
git remote add origin https://github.com/YOUR-USERNAME/cal-fund-analyzer.git

# Push to GitHub
git push -u origin main
```

#### Step 3: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under **Source**, select:
   - Branch: `main`
   - Folder: `/ (root)`
4. Click **Save**
5. Wait 1-2 minutes for deployment

#### Step 4: Access Your App

Your app will be available at:
```
https://YOUR-USERNAME.github.io/cal-fund-analyzer/
```

---

### Method 2: Using GitHub Desktop (Easy)

#### Step 1: Open GitHub Desktop

1. Download and install [GitHub Desktop](https://desktop.github.com/)
2. Sign in with your GitHub account

#### Step 2: Create Repository

1. Click **File** → **New Repository**
2. Name: `cal-fund-analyzer`
3. Local Path: Choose location
4. Click **Create Repository**

#### Step 3: Add Files

1. Copy `index.html`, `app.js`, `styles.css` to repository folder
2. GitHub Desktop will detect changes
3. Write commit message: "Initial web app"
4. Click **Commit to main**

#### Step 4: Publish Repository

1. Click **Publish repository**
2. Uncheck "Keep this code private" (for free GitHub Pages)
3. Click **Publish repository**

#### Step 5: Enable GitHub Pages

1. Go to repository on GitHub.com
2. **Settings** → **Pages**
3. Source: `main` branch, `/ (root)`
4. **Save**

Your app is now live! 🎉

---

### Method 3: Using GitHub Web Interface (No Git Needed)

#### Step 1: Create Repository

1. Go to [GitHub.com](https://github.com)
2. Click **+** → **New repository**
3. Repository name: `cal-fund-analyzer`
4. Make it **Public**
5. Click **Create repository**

#### Step 2: Upload Files

1. Click **Add file** → **Upload files**
2. Drag and drop:
   - `index.html`
   - `app.js`
   - `styles.css`
   - `README_WEB.md`
3. Commit message: "Initial web app upload"
4. Click **Commit changes**

#### Step 3: Enable GitHub Pages

1. Go to **Settings** → **Pages**
2. Source: `main` branch, `/ (root)`
3. Click **Save**
4. Wait 1-2 minutes

#### Step 4: Access Your App

Visit: `https://YOUR-USERNAME.github.io/cal-fund-analyzer/`

---

## 🔧 Custom Domain (Optional)

Want a custom domain like `cal-analyzer.com`?

### Step 1: Configure Domain

1. Buy a domain from any registrar (Namecheap, GoDaddy, etc.)
2. Add DNS records:
   ```
   Type: A
   Host: @
   Value: 185.199.108.153
   
   Type: A
   Host: @
   Value: 185.199.109.153
   
   Type: A
   Host: @
   Value: 185.199.110.153
   
   Type: A
   Host: @
   Value: 185.199.111.153
   
   Type: CNAME
   Host: www
   Value: YOUR-USERNAME.github.io
   ```

### Step 2: Configure GitHub

1. Go to **Settings** → **Pages**
2. Under **Custom domain**, enter your domain
3. Click **Save**
4. Wait for DNS propagation (up to 24 hours)

---

## 📱 Testing Your Deployment

### 1. Check Deployment Status

Go to repository → **Actions** tab to see deployment status.

### 2. Test in Different Browsers

- ✅ Chrome
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Mobile browsers

### 3. Test Core Features

- [ ] Fund selection dropdown works
- [ ] Date inputs accept values
- [ ] Fetch data button works
- [ ] Chart displays correctly
- [ ] Analysis buttons open modals
- [ ] Export CSV works
- [ ] LocalStorage saves data

### 4. Check Mobile Responsiveness

- Test on actual mobile devices
- Use browser DevTools → Device Mode
- Check portrait and landscape orientations

---

## 🐛 Troubleshooting Deployment

### Issue: 404 Page Not Found

**Solution:**
- Verify `index.html` is in root directory
- Check GitHub Pages settings
- Wait 2-3 minutes after enabling Pages
- Force refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

### Issue: Blank Page

**Solution:**
- Open browser console (F12)
- Check for JavaScript errors
- Verify all files uploaded correctly
- Check file names are exact (case-sensitive)

### Issue: Chart Not Loading

**Solution:**
- Check internet connection (CDN libraries)
- Verify Chart.js CDN link in `index.html`
- Check browser console for errors
- Try different browser

### Issue: API Requests Failing

**Solution:**
- Check CORS settings (should work from GitHub Pages)
- Verify CAL API is accessible
- Check browser console for CORS errors
- Test API directly: `https://cal.lk/wp-admin/admin-ajax.php`

### Issue: LocalStorage Not Working

**Solution:**
- Check browser privacy settings
- Disable browser extensions
- Try incognito/private mode
- Clear browser cache

---

## 🔄 Updating Your Deployed App

### Using Git Command Line

```bash
# Make changes to your files
# ...

# Stage changes
git add .

# Commit changes
git commit -m "Update: description of changes"

# Push to GitHub
git push origin main

# GitHub Pages will auto-deploy in 1-2 minutes
```

### Using GitHub Desktop

1. Make changes to files
2. GitHub Desktop will show changes
3. Write commit message
4. Click **Commit to main**
5. Click **Push origin**
6. Wait for automatic deployment

### Using GitHub Web Interface

1. Go to repository on GitHub
2. Click on file to edit
3. Click pencil icon (Edit)
4. Make changes
5. Commit changes
6. Wait for automatic deployment

---

## 📊 Monitoring Your App

### GitHub Pages Analytics

GitHub Pages doesn't include built-in analytics. To add analytics:

#### Option 1: Google Analytics

Add to `index.html` before `</head>`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

#### Option 2: Simple Analytics

Use privacy-friendly analytics like:
- [Plausible](https://plausible.io/)
- [Fathom](https://usefathom.com/)
- [Simple Analytics](https://simpleanalytics.com/)

---

## 🔒 Security Best Practices

### 1. Don't Commit Sensitive Data
- Never commit API keys
- Don't store personal information
- Keep `.env` files in `.gitignore`

### 2. Use HTTPS
- GitHub Pages automatically provides HTTPS
- Always use HTTPS URLs for CDN resources
- Enable "Enforce HTTPS" in repository settings

### 3. Content Security Policy

Add to `index.html`:

```html
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; 
               style-src 'self' 'unsafe-inline';">
```

---

## 🎨 Customization After Deployment

### Change Colors

Edit `styles.css`:
```css
:root {
    --primary-color: #your-color;
    --success-color: #your-color;
    /* ... */
}
```

### Add Custom Logo

Add to `index.html` header:
```html
<img src="logo.png" alt="Logo" class="header-logo">
```

### Modify App Name

Change in `index.html`:
```html
<title>Your Custom Name</title>
<h1>Your Custom Name</h1>
```

---

## 📦 Backup & Version Control

### Create Releases

1. Go to repository on GitHub
2. Click **Releases** → **Create a new release**
3. Tag version: `v1.0.0`
4. Title: "Initial Release"
5. Describe changes
6. Click **Publish release**

### Branches for Features

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "Add new feature"

# Push branch
git push origin feature/new-feature

# Create Pull Request on GitHub
# Merge when ready
```

---

## 🚀 Performance Optimization

### 1. Minimize Files

Use minifiers for production:
- CSS: [CSSMinifier](https://cssminifier.com/)
- JS: [JSCompress](https://jscompress.com/)

### 2. Optimize Images

If you add images:
- Use WebP format
- Compress images
- Use appropriate sizes

### 3. Enable Caching

Add `.nojekyll` file to repository root:
```bash
touch .nojekyll
git add .nojekyll
git commit -m "Add .nojekyll for better caching"
git push
```

---

## ✅ Deployment Checklist

Before going live:

- [ ] Test locally first
- [ ] All files committed to Git
- [ ] Repository is public
- [ ] GitHub Pages enabled
- [ ] Custom domain configured (if using)
- [ ] All features tested
- [ ] Mobile responsive checked
- [ ] Browser compatibility verified
- [ ] README documentation complete
- [ ] License file added
- [ ] Contact information added

---

## 📞 Need Help?

- **GitHub Pages Docs:** https://docs.github.com/en/pages
- **GitHub Community:** https://github.community/
- **Stack Overflow:** Search for "GitHub Pages" questions

---

## 🎉 Success!

Once deployed, share your app:

```markdown
🎉 CAL Fund Analyzer is now live!

Visit: https://YOUR-USERNAME.github.io/cal-fund-analyzer/

Features:
✅ Real-time fund data
✅ Interactive charts
✅ Performance analysis
✅ Mobile responsive

Star ⭐ the repo if you find it useful!
```

---

**Happy Deploying! 🚀**

