# 🚀 Deployment Guide - Crypto Tracker

This guide will help you deploy your crypto tracker application to various platforms.

## 📋 Pre-Deployment Checklist

- [x] Git repository initialized
- [x] All files committed
- [x] requirements.txt created
- [x] Procfile for deployment
- [x] .gitignore configured

## 🌐 Deployment Options

### Option 1: Deploy to Render (Recommended - Free Tier Available)

**Steps:**

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub account

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `deploython2` repository

3. **Configure Service**
   ```
   Name: crypto-tracker
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app --bind 0.0.0.0:$PORT
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait 2-3 minutes for deployment
   - Your app will be live at: https://crypto-tracker-xxxx.onrender.com

**Auto-Deploy:** Render automatically deploys when you push to GitHub!

---

### Option 2: Deploy to Railway

**Steps:**

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign in with GitHub

2. **New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `deploython2` repository

3. **Configure**
   - Railway auto-detects Python
   - Add start command: `gunicorn app:app`
   - Click "Deploy"

4. **Generate Domain**
   - Go to Settings → Generate Domain
   - Your app will be live!

---

### Option 3: Deploy to Heroku

**Steps:**

1. **Install Heroku CLI**
   ```powershell
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   cd c:\Users\Sneha\OneDrive\Desktop\deploython2
   heroku create your-crypto-tracker
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **Open Your App**
   ```bash
   heroku open
   ```

---

### Option 4: Deploy to PythonAnywhere (Free)

**Steps:**

1. **Create Account**
   - Go to https://www.pythonanywhere.com
   - Sign up for free account

2. **Upload Code**
   - Use Git or upload files manually
   - Clone your repository in Bash console

3. **Create Web App**
   - Go to Web tab → Add new web app
   - Choose Flask
   - Set path to your app.py

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure WSGI**
   - Edit WSGI configuration file
   - Point to your Flask app

---

## 🔧 Environment Variables (If Needed)

Some platforms require environment variables:

```
FLASK_ENV=production
DATABASE_PATH=crypto_data.db
SCRAPE_INTERVAL=10
PORT=5000
```

Set these in your platform's dashboard:
- **Render**: Environment → Add Environment Variable
- **Railway**: Variables tab
- **Heroku**: Settings → Config Vars

---

## 📊 Post-Deployment Testing

After deployment, test these endpoints:

1. **Main Page**
   ```
   https://your-app-url.com/
   ```

2. **API - Get Cryptos**
   ```
   https://your-app-url.com/api/cryptos
   ```

3. **API - Trigger Scrape**
   ```
   https://your-app-url.com/api/scrape-now
   ```

4. **API - Price History**
   ```
   https://your-app-url.com/api/crypto/BTC/history
   ```

---

## 🎯 GitHub Repository Setup

1. **Create GitHub Repository**
   ```bash
   # Go to github.com and create new repository
   # Then push your code:
   
   git remote add origin https://github.com/YOUR_USERNAME/crypto-tracker.git
   git branch -M main
   git push -u origin main
   ```

2. **Add Repository Description**
   ```
   🚀 Live Crypto Tracker - Real-time cryptocurrency price monitoring with web scraping, database storage, and automated updates
   ```

3. **Add Topics (Tags)**
   ```
   python, flask, web-scraping, cryptocurrency, sqlite, api, beautifulsoup, scheduler
   ```

---

## 🐛 Troubleshooting

### Issue: "Application Error" on deployment

**Solution:**
- Check logs: Look for error messages
- Verify Procfile: Ensure correct start command
- Check requirements.txt: All dependencies listed

### Issue: Database not persisting

**Solution:**
- Use platform's persistent storage
- Or switch to PostgreSQL for production

### Issue: Scraper not running

**Solution:**
- Check scheduler is starting
- Verify API endpoint is accessible
- Check platform logs for errors

---

## 🔄 Continuous Deployment

Once connected to GitHub, any push to `main` branch will automatically deploy:

```bash
# Make changes
git add .
git commit -m "feat: Add new feature"
git push origin main

# Auto-deploys! 🚀
```

---

## 📈 Monitoring

After deployment, monitor:
- **Response time**: Check API speed
- **Error logs**: Watch for crashes
- **Database size**: Monitor storage usage
- **API rate limits**: CoinGecko limits

---

## 💡 Tips

1. **Free Tier Limits**:
   - Render: App sleeps after 15 min inactivity
   - Heroku: 550-1000 free hours/month
   - Railway: $5 free credit/month

2. **Keep App Alive**:
   - Use UptimeRobot to ping your app every 5 minutes
   - Prevents sleeping on free tiers

3. **Database Backup**:
   - Regularly export your SQLite database
   - Consider PostgreSQL for production

---

## 🎉 Success!

Your crypto tracker is now live! Share your URL and showcase your project.

**Next Steps:**
- Add more cryptocurrencies
- Implement price alerts
- Add user authentication
- Create mobile app
- Add charts and graphs

---

**Need Help?** Open an issue on GitHub or check the main README.md
