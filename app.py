from flask import Flask, render_template, jsonify
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import atexit
import os

from database import init_db, get_all_cryptos, get_crypto_history
from scraper import scrape_crypto_prices

app = Flask(__name__)
CORS(app)

# Initialize database
init_db()

# Configure scheduler for automated scraping (interval from env, default 10 min)
try:
    SCRAPE_INTERVAL_MINUTES = int(os.environ.get("SCRAPE_INTERVAL", "10"))
except ValueError:
    SCRAPE_INTERVAL_MINUTES = 10

scheduler = BackgroundScheduler()
scheduler.add_job(func=scrape_crypto_prices, trigger="interval", minutes=SCRAPE_INTERVAL_MINUTES)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    return jsonify({"status": "ok", "time": datetime.now().isoformat()}), 200

@app.route('/api/cryptos')
def get_cryptos():
    """API endpoint to get all latest crypto prices"""
    try:
        cryptos = get_all_cryptos()
        return jsonify({
            'success': True,
            'data': cryptos,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/crypto/<symbol>/history')
def get_history(symbol):
    """API endpoint to get price history for a specific crypto"""
    try:
        history = get_crypto_history(symbol.upper())
        return jsonify({
            'success': True,
            'data': history,
            'symbol': symbol.upper()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/scrape-now')
def scrape_now():
    """Manual trigger to scrape data immediately"""
    try:
        scrape_crypto_prices()
        return jsonify({
            'success': True,
            'message': 'Scraping completed successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Initial scrape on startup
    print("🚀 Starting Crypto Tracker...")
    print("📊 Performing initial data scrape...")
    scrape_crypto_prices()
    print("✅ Initial scrape complete!")
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
