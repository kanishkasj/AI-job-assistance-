# 🚀 Render Deployment Guide (SQLite)

## Prerequisites
- [ ] GitHub account
- [ ] Render account (free): https://render.com
- [ ] Mistral AI API key

---

## 📋 Step-by-Step Deployment

### **Step 1: Prepare Your Code**

**1.1 Initialize Git Repository (if not already done)**
```powershell
git init
git add .
git commit -m "Initial commit - FastAPI Assessment App"
```

**1.2 Create GitHub Repository**
1. Go to https://github.com/new
2. Create a new repository (e.g., `assessment-app`)
3. **DO NOT** initialize with README (you already have files)

**1.3 Push to GitHub**
```powershell
git remote add origin https://github.com/YOUR_USERNAME/assessment-app.git
git branch -M main
git push -u origin main
```
Replace `YOUR_USERNAME` with your actual GitHub username.

---

### **Step 2: Deploy on Render**

**2.1 Sign Up/Login to Render**
- Go to https://render.com
- Click **"Get Started for Free"**
- Sign up with GitHub (recommended for easier deployment)

**2.2 Create New Web Service**
1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Click **"Connect a repository"** or **"Build and deploy from a Git repository"**
4. Authorize Render to access your GitHub repositories
5. Select your `assessment-app` repository

**2.3 Configure Web Service**

Fill in the following settings:

| Field | Value |
|-------|-------|
| **Name** | `assessment-app` (or your preferred name) |
| **Region** | Choose closest to you |
| **Branch** | `main` |
| **Root Directory** | Leave blank |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | **Free** |

**2.4 Add Environment Variables**
1. Scroll down to **"Environment Variables"** section
2. Click **"Add Environment Variable"**
3. Add:
   - **Key**: `MISTRAL_API_KEY`
   - **Value**: Your actual Mistral API key (from your `.env` file)
4. Click **"Add"**

**2.5 Advanced Settings (Optional)**
- **Auto-Deploy**: Keep enabled (deploys automatically on git push)
- **Health Check Path**: `/health`

**2.6 Deploy!**
1. Click **"Create Web Service"** button at the bottom
2. Wait 5-10 minutes for deployment (watch the logs)
3. ✅ Once you see **"Your service is live"**, it's ready!

---

### **Step 3: Get Your App URL**

After deployment completes:
1. Copy the URL shown at the top (e.g., `https://assessment-app-xxxx.onrender.com`)
2. Click on it to open your app
3. Your frontend will be at: `https://assessment-app-xxxx.onrender.com`
4. API docs at: `https://assessment-app-xxxx.onrender.com/docs`

---

## ⚠️ Important Notes

### **SQLite Data Persistence**
- ✅ Data persists during normal usage
- ❌ Data is **lost** when:
  - You redeploy (git push)
  - Render restarts your service
  - You manually restart the service
- 💡 **Solution**: Don't redeploy unless necessary!

### **Free Tier Limitations**
- ⏱️ Service spins down after **15 minutes** of inactivity
- 🐌 First request after spin-down takes **30-60 seconds** (cold start)
- 💾 **750 hours/month** free (enough for continuous running)
- 💿 Ephemeral filesystem (files don't persist across restarts)

### **Keep Your Service Alive**
To prevent spin-down, use a monitoring service:
- UptimeRobot (https://uptimerobot.com) - free, pings every 5 minutes
- Cron-job.org (https://cron-job.org) - free monitoring

---

## 🔧 Troubleshooting

### **Deployment Failed**
Check Render logs for errors:
- Missing dependencies → Ensure `requirements.txt` is complete
- Port binding error → Ensure using `--port $PORT` in start command
- Import errors → Check all files are committed to Git

### **API Key Error**
- Verify `MISTRAL_API_KEY` is set in Render environment variables
- Check for typos in the key
- Ensure no extra spaces

### **Database Not Working**
- SQLite creates `assessment.db` automatically on first run
- Check logs for SQLAlchemy errors
- Verify `database.py` is committed to Git

### **Static Files Not Loading**
- Ensure `static/` folder is committed to Git
- Check file paths use forward slashes `/`
- Verify CORS is enabled in `main.py`

---

## 🔄 Update Your Deployed App

When you make changes locally:

```powershell
git add .
git commit -m "Description of changes"
git push origin main
```

Render will automatically redeploy! ⚠️ **Remember: SQLite data will be lost.**

---

## 📊 Monitor Your App

1. **Render Dashboard**: View logs, metrics, events
2. **Logs Tab**: Real-time application logs
3. **Metrics**: Request count, response time, memory usage
4. **Events**: Deployment history

---

## 🎉 Success Checklist

- [ ] Code pushed to GitHub
- [ ] Web service created on Render
- [ ] Environment variable `MISTRAL_API_KEY` set
- [ ] Deployment successful (green checkmark)
- [ ] App URL accessible
- [ ] Frontend loads at root URL
- [ ] API docs accessible at `/docs`
- [ ] Test all 5 tabs (Profile, Resume Analyzer, Answer Generator, Job Matcher, Dashboard)

---

## 📞 Need Help?

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- FastAPI Docs: https://fastapi.tiangolo.com/deployment/

---

**Your app will be live at:** `https://YOUR-APP-NAME.onrender.com` 🎊
