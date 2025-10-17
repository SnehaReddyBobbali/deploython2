# 🧪 Testing Guide - Crypto Tracker

## Local Testing Instructions

### Step 1: Setup Environment

```powershell
# Navigate to project directory
cd c:\Users\Sneha\OneDrive\Desktop\deploython2

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Run the Application

```powershell
# Start the Flask app
python app.py
```

**Expected Output:**
```
🚀 Starting Crypto Tracker...
📊 Performing initial data scrape...

⏰ [2025-10-17 12:00:00] Starting crypto price scrape...
  ✓ Bitcoin (BTC): $43,250.00
  ✓ Ethereum (ETH): $2,280.50
  ✓ Tether (USDT): $1.00
  ...
✅ Successfully scraped 10 cryptocurrencies

✅ Initial scrape complete!
 * Running on http://0.0.0.0:5000
```

### Step 3: Test in Browser

1. **Open Main Page**
   - URL: http://localhost:5000
   - Should see: Crypto tracker interface with data

2. **Check Data Display**
   - ✅ 10 cryptocurrencies listed
   - ✅ Prices showing
   - ✅ 24h change percentages (green/red)
   - ✅ Market cap and volume data
   - ✅ Last updated timestamp

3. **Test Manual Refresh**
   - Click "Refresh Now" button
   - Should see: Loading state → Updated data
   - Check timestamp updates

### Step 4: Test API Endpoints

**Using browser or Postman:**

1. **Get All Cryptos**
   ```
   GET http://localhost:5000/api/cryptos
   ```
   **Expected:** JSON with crypto data

2. **Get Price History**
   ```
   GET http://localhost:5000/api/crypto/BTC/history
   ```
   **Expected:** JSON with historical prices

3. **Trigger Manual Scrape**
   ```
   GET http://localhost:5000/api/scrape-now
   ```
   **Expected:** Success message

### Step 5: Test Automated Scheduler

1. **Wait 10 minutes**
   - Scheduler should auto-scrape
   - Check terminal for scrape logs

2. **Verify in UI**
   - Refresh page
   - Data should be updated

### Step 6: Test Database

```powershell
# Open Python shell
python

# Test database
>>> from database import get_all_cryptos, get_crypto_history
>>> cryptos = get_all_cryptos()
>>> print(len(cryptos))  # Should be 10
>>> history = get_crypto_history('BTC')
>>> print(len(history))  # Should have historical data
>>> exit()
```

### Step 7: Test Responsive Design

1. Open browser DevTools (F12)
2. Toggle device toolbar
3. Test different screen sizes:
   - Mobile (375px)
   - Tablet (768px)
   - Desktop (1440px)

**Verify:**
- ✅ Layout adapts to screen size
- ✅ Table remains readable
- ✅ Buttons remain accessible

---

## Feature Checklist

Test each feature:

- [ ] **Web Scraping**
  - [ ] Data fetches from CoinGecko API
  - [ ] 10 cryptocurrencies retrieved
  - [ ] All data fields populated

- [ ] **Database Storage**
  - [ ] Data saves to SQLite
  - [ ] Price history tracked
  - [ ] No duplicate entries

- [ ] **Automated Updates**
  - [ ] Scheduler starts on app launch
  - [ ] Auto-scrapes every 10 minutes
  - [ ] Logs show scraping activity

- [ ] **API Endpoints**
  - [ ] `/api/cryptos` returns data
  - [ ] `/api/crypto/<symbol>/history` works
  - [ ] `/api/scrape-now` triggers scrape

- [ ] **Frontend UI**
  - [ ] Page loads without errors
  - [ ] Data displays correctly
  - [ ] Refresh button works
  - [ ] Auto-refresh works (every 2 min)
  - [ ] Statistics cards update
  - [ ] Price changes show colors (green/red)

- [ ] **Responsive Design**
  - [ ] Works on mobile
  - [ ] Works on tablet
  - [ ] Works on desktop

---

## Common Issues & Solutions

### Issue: "Module not found"
**Solution:**
```powershell
# Ensure virtual environment is activated
.\venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Port 5000 already in use"
**Solution:**
```powershell
# Find and kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or change port in app.py:
# app.run(port=5001)
```

### Issue: "Database locked"
**Solution:**
```powershell
# Delete database and restart
del crypto_data.db
python app.py
```

### Issue: No data showing
**Solution:**
1. Check internet connection
2. Check terminal for error logs
3. Verify CoinGecko API is accessible
4. Try manual scrape: http://localhost:5000/api/scrape-now

---

## Performance Testing

### Test Load Time
```powershell
# Use curl or browser DevTools
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:5000/api/cryptos
```

**Expected:**
- API response: < 500ms
- Page load: < 2s
- Scrape time: 2-5s

### Test Database Size
```powershell
# Check database file size
dir crypto_data.db
```

**Note:** Size grows with historical data. Consider cleanup after 7 days.

---

## Testing Before Deployment

**Pre-deployment checklist:**

1. [ ] All features working locally
2. [ ] No errors in console/terminal
3. [ ] Database creating and updating
4. [ ] All API endpoints responding
5. [ ] UI displaying correctly
6. [ ] Scheduler running automatically
7. [ ] Git repository committed
8. [ ] README.md complete
9. [ ] requirements.txt accurate
10. [ ] .gitignore excluding database

---

## Manual Testing Script

Run this complete test:

```powershell
# 1. Setup
cd c:\Users\Sneha\OneDrive\Desktop\deploython2
.\venv\Scripts\activate
python app.py

# In another terminal:
# 2. Test APIs
curl http://localhost:5000/api/cryptos
curl http://localhost:5000/api/crypto/BTC/history
curl http://localhost:5000/api/scrape-now

# 3. Open browser
start http://localhost:5000

# 4. Test UI manually
# - Click refresh button
# - Check data displays
# - Verify colors and formatting
# - Test on mobile view (DevTools)

# 5. Check logs
# - Verify scraping logs in terminal
# - No error messages
```

---

## Success Criteria

**Application is ready when:**

✅ Data scrapes successfully
✅ Database stores data
✅ Scheduler runs automatically
✅ API endpoints work
✅ UI displays beautifully
✅ No console errors
✅ Responsive on all devices
✅ Git commits present

---

## 📞 Need Help?

If tests fail:
1. Check error messages in terminal
2. Review browser console (F12)
3. Verify all dependencies installed
4. Check internet connection
5. Review code for typos

**All tests passing? Deploy your app! 🚀**
