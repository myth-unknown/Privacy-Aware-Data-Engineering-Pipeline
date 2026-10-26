# 🚀 Deployment Guide

## Quick Deploy to Streamlit Cloud (5 Minutes)

### Step 1: Push to GitHub

```powershell
# Add all files
git add .

# Commit
git commit -m "feat: Ready for deployment with auto spaCy download"

# Push to GitHub
git push origin main
```

### Step 2: Deploy

**Option A: Use Deploy Button in App**
1. Run: `.\start.ps1`
2. Look at top-right corner of the app
3. Click "Deploy" button
4. Browser opens to Streamlit Cloud

**Option B: Go Directly to Streamlit Cloud**
1. Visit: https://share.streamlit.io/
2. Click "New app"
3. Sign in with GitHub

### Step 3: Configure

```
Repository: YOUR-USERNAME/Privacy-Aware-Data-Engineering-Pipeline
Branch: main
Main file path: app.py
App URL: privacy-data-pipeline (or your choice)
```

### Step 4: Click "Deploy!"

Wait 5-10 minutes for first deployment. Watch the build logs.

### Step 5: Done! 🎉

Your app is live at:
```
https://privacy-data-pipeline.streamlit.app
```

Share this URL with anyone!

---

## What Happens During Deployment

1. **Build Stage:**
   - Installs Python 3.12
   - Installs all packages from requirements.txt
   - Downloads spaCy model automatically (handled by app.py)

2. **Run Stage:**
   - Starts Streamlit server
   - App becomes accessible online

3. **Auto-Updates:**
   - Every GitHub push triggers automatic redeployment
   - Changes go live in 2-5 minutes

---

## Updating Your Deployed App

```powershell
# Make changes locally
# Test: .\start.ps1

# Commit and push
git add .
git commit -m "Update feature X"
git push origin main

# Streamlit Cloud auto-redeploys!
# Wait 2-5 minutes
```

---

## Important Notes

### 1. First Deployment
- Takes 8-12 minutes (downloads 500MB spaCy model)
- Subsequent deployments: 2-5 minutes
- spaCy model downloads automatically via app.py

### 2. Resource Limits (Free Tier)
- 1 GB RAM
- 1 CPU core
- 1 GB storage
- App sleeps after 7 days of inactivity
- Wakes up in ~30 seconds on first visit

### 3. Data Privacy
- Your app is PUBLIC by default
- Anyone with URL can access
- Don't use for sensitive/production data
- For private apps, upgrade to paid plan

### 4. Database
- DuckDB file is NOT persistent on free tier
- Data resets on each deployment
- Use cloud database for persistent data

---

## Sharing Your Deployed App

### Share URL:
```
https://your-app.streamlit.app
```

### On Portfolio:
```markdown
🔗 [Live Demo](https://your-app.streamlit.app)
```

### On LinkedIn:
```
Check out my Privacy-Aware Data Pipeline!
🔗 https://your-app.streamlit.app
Built with Python, Streamlit, and AI
```

### On Resume:
```
Privacy-Aware Data Engineering Pipeline
• Live Demo: your-app.streamlit.app
• GitHub: github.com/YOUR-USERNAME/Privacy-Aware-Data-Engineering-Pipeline
• Tech: Python, Streamlit, Presidio, spaCy, DuckDB
```

---

## Troubleshooting

### Build Fails with "Unable to locate package"
- **Cause:** `packages.txt` with comments or invalid content
- **Fix:** Delete `packages.txt` if you don't need system packages
- **Note:** We deleted this file - not needed for this project

### Build Fails
- Check build logs in Streamlit Cloud dashboard
- Verify requirements.txt has all dependencies
- Ensure Python version compatibility

### App Doesn't Start
- Check logs for errors
- Verify app.py is in root directory
- Check that all imports work

### spaCy Model Issue
- App handles download automatically
- First run shows: "Downloading NLP model..."
- Wait for download to complete (~2 minutes)

### Out of Memory
- Free tier has 1GB RAM limit
- Reduce data/sample sizes
- Upgrade to paid tier for more resources

---

## Alternative: Render Deployment

If Streamlit Cloud doesn't work:

1. Go to https://render.com
2. New → Web Service
3. Connect GitHub repo
4. Select: Privacy-Aware-Data-Engineering-Pipeline
5. Settings:
   - Runtime: Python 3
   - Build: `pip install -r requirements.txt && python -m spacy download en_core_web_lg`
   - Start: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
6. Click "Create Web Service"

Your app will be at: `https://your-app.onrender.com`

---

## Cost Comparison

### Streamlit Cloud:
- **Free**: Unlimited public apps, 1 private app
- **Starter ($20/month)**: 3 private apps
- **Team ($250/month)**: Unlimited private apps, custom domain

### Render:
- **Free**: Public app, sleeps after inactivity
- **Starter ($7/month)**: Always on, 512MB RAM
- **Standard ($25/month)**: 2GB RAM, better performance

### Recommendation:
**Use Streamlit Cloud Free Tier** for portfolio/demo projects!

---

## Need Help?

- Streamlit Docs: https://docs.streamlit.io/streamlit-cloud
- Community: https://discuss.streamlit.io/
- GitHub Issues: (create issue in your repo)

---

**Ready to deploy? Push to GitHub and click Deploy!** 🚀
