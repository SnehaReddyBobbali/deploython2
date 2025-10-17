# ⚡ Quick Start Guide

## 🚀 Get Started in 3 Minutes!

### Step 1: Install Dependencies (1 min)

```powershell
# Navigate to project
cd c:\Users\Sneha\OneDrive\Desktop\deploython2

# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### Step 2: Run the App (30 seconds)

```powershell
python app.py
```

### Step 3: Open in Browser (30 seconds)

Open: **http://localhost:5000**

🎉 **Done!** Your crypto tracker is running!

---

## 📸 What You'll See

```
🚀 Starting Crypto Tracker...
📊 Performing initial data scrape...

⏰ [2025-10-17 12:00:00] Starting crypto price scrape...
  ✓ Bitcoin (BTC): $43,250.00
  ✓ Ethereum (ETH): $2,280.50
  ✓ Tether (USDT): $1.00
  ✓ BNB (BNB): $310.50
  ✓ Solana (SOL): $98.75
  ✓ XRP (XRP): $0.56
  ✓ Cardano (ADA): $0.48
  ✓ Dogecoin (DOGE): $0.095
  ✓ Polygon (MATIC): $0.82
  ✓ Polkadot (DOT): $7.25
✅ Successfully scraped 10 cryptocurrencies

 * Running on http://0.0.0.0:5000
```

---

## 🎯 Next Steps

### Test It Out
1. ✅ Click "Refresh Now" button
2. ✅ Watch prices update
3. ✅ Check 24h change colors
4. ✅ View statistics cards

### Deploy It
Choose a platform:
- **Render** (Easiest) - See DEPLOYMENT.md
- **Railway** (Fast) - See DEPLOYMENT.md
- **Heroku** (Popular) - See DEPLOYMENT.md

### Push to GitHub
```powershell
# Create repository on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/crypto-tracker.git
git branch -M main
git push -u origin main
```

---

## 🔥 Key Features

✨ **Live Data**: Real-time crypto prices from CoinGecko
📊 **10 Cryptocurrencies**: Bitcoin, Ethereum, and more
💾 **Database**: SQLite stores all data
⏰ **Auto-Updates**: Refreshes every 10 minutes
🎨 **Beautiful UI**: Modern dark theme
📱 **Responsive**: Works on all devices

---

## 🎓 Learning Resources

**Want to understand the code?**

1. **app.py** - Flask routes and scheduler
2. **scraper.py** - Web scraping logic
3. **database.py** - SQLite operations
4. **templates/index.html** - Frontend HTML
5. **static/style.css** - Styling
6. **static/script.js** - JavaScript logic

---

## 💡 Common Commands

```powershell
# Start app
python app.py

# Stop app
Ctrl + C

# Check git status
git status

# Make new commit
git add .
git commit -m "your message"

# View logs
git log --oneline

# Test API
curl http://localhost:5000/api/cryptos
```

---

## 🆘 Need Help?

**App not starting?**
- Check Python version: `python --version` (need 3.8+)
- Verify virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

**No data showing?**
- Check internet connection
- Wait for initial scrape (takes 2-5 seconds)
- Check terminal for errors

**Port 5000 busy?**
- Change port in app.py: `app.run(port=5001)`

---

## 📚 Full Documentation

- **README.md** - Complete project overview
- **DEPLOYMENT.md** - Deployment instructions
- **TESTING.md** - Testing guide

---

## 🎉 You're Ready!

Your crypto tracker is up and running. Now:
1. Test all features
2. Customize it (add more cryptos, change UI)
3. Deploy it online
4. Share it with friends!

**Happy coding! 🚀**
