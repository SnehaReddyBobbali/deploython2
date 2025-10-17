# 🚀 Live Crypto Tracker

A dynamic web application that scrapes and displays real-time cryptocurrency prices from CoinGecko API. Built with Python Flask, featuring automated data updates, database storage, and a beautiful responsive UI.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- 📊 **Real-time Data Scraping**: Fetches live cryptocurrency prices from CoinGecko API
- 💾 **Database Storage**: Stores data in SQLite with historical price tracking
- ⏰ **Automated Updates**: Background scheduler updates data every 10 minutes
- 🎨 **Beautiful UI**: Modern, responsive interface with dark theme
- 📈 **Live Statistics**: Market cap, 24h volume, price changes
- 🔄 **Manual Refresh**: Instant data update button
- 📱 **Mobile Responsive**: Works perfectly on all devices

## 🛠️ Tech Stack

**Backend:**
- Python 3.8+
- Flask (Web Framework)
- SQLite (Database)
- APScheduler (Cron Jobs)
- Requests + BeautifulSoup (Web Scraping)

**Frontend:**
- HTML5
- CSS3 (Modern styling with animations)
- Vanilla JavaScript (No frameworks!)

## 📋 Requirements

- Python 3.8 or higher
- pip (Python package manager)
- Git

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd deploython2
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

The app will start on `http://localhost:5000`

## 📁 Project Structure

```
deploython2/
│
├── app.py                 # Main Flask application
├── scraper.py            # Web scraping logic
├── database.py           # Database operations
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore rules
│
├── templates/
│   └── index.html       # Main HTML template
│
├── static/
│   ├── style.css        # Styles
│   └── script.js        # Frontend JavaScript
│
└── README.md            # This file
```

## 🎯 How It Works

1. **Data Scraping**: 
   - Uses CoinGecko public API to fetch top 10 cryptocurrencies
   - Extracts price, market cap, volume, and 24h change data
   - Runs automatically every 10 minutes via APScheduler

2. **Database Storage**:
   - Stores latest prices in `cryptos` table
   - Maintains historical data in `price_history` table
   - Enables price trend analysis over time

3. **Backend API**:
   - `/api/cryptos` - Get all cryptocurrency data
   - `/api/crypto/<symbol>/history` - Get price history
   - `/api/scrape-now` - Trigger immediate scraping

4. **Frontend**:
   - Fetches data from backend APIs
   - Displays in responsive table format
   - Auto-refreshes every 2 minutes
   - Shows statistics and price changes

## 🌐 Deployment

### Deploy to Render

1. Create a `render.yaml`:

```yaml
services:
  - type: web
    name: crypto-tracker
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

2. Push to GitHub
3. Connect repository to Render
4. Deploy!

### Deploy to Railway

1. Install Railway CLI or use web dashboard
2. Push to GitHub
3. Connect repository
4. Add start command: `gunicorn app:app`
5. Deploy!

### Deploy to Heroku

```bash
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

## 🔧 Environment Variables

For production, you can set these environment variables:

```bash
FLASK_ENV=production
DATABASE_PATH=crypto_data.db
SCRAPE_INTERVAL=10  # minutes
PORT=5000
```

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main page |
| `/api/cryptos` | GET | Get all cryptocurrency data |
| `/api/crypto/<symbol>/history` | GET | Get price history for a symbol |
| `/api/scrape-now` | GET | Trigger immediate data scraping |

## 🎨 Features Showcase

- **Live Price Updates**: Real-time cryptocurrency prices
- **24h Change Indicators**: Green (▲) for gains, Red (▼) for losses
- **Market Statistics**: Total tracked, gainers, losers, market cap
- **Price History**: Track price changes over time
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Dark Theme**: Easy on the eyes

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Built with ❤️ using Python Flask and Web Scraping

## 🙏 Acknowledgments

- Data provided by [CoinGecko API](https://www.coingecko.com/)
- Icons and design inspiration from modern UI practices
- Flask documentation and community

## 📞 Support

If you have any questions or run into issues, please open an issue on GitHub.

---

⭐ Star this repo if you find it helpful!
