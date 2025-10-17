import requests
from bs4 import BeautifulSoup
from datetime import datetime
from database import save_crypto_data

def scrape_crypto_prices():
    """
    Scrape cryptocurrency prices from CoinGecko API
    Using their free public API - no authentication needed
    """
    print(f"\n⏰ [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting crypto price scrape...")
    
    try:
        # CoinGecko free API endpoint
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 10,
            'page': 1,
            'sparkline': False,
            'price_change_percentage': '24h'
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Process each cryptocurrency
        for crypto in data:
            crypto_data = {
                'symbol': crypto['symbol'].upper(),
                'name': crypto['name'],
                'price': crypto['current_price'],
                'market_cap': crypto['market_cap'],
                'volume_24h': crypto['total_volume'],
                'change_24h': crypto.get('price_change_percentage_24h', 0),
                'image_url': crypto['image']
            }
            
            # Save to database
            save_crypto_data(crypto_data)
            print(f"  ✓ {crypto_data['name']} ({crypto_data['symbol']}): ${crypto_data['price']:,.2f}")
        
        print(f"✅ Successfully scraped {len(data)} cryptocurrencies\n")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error scraping data: {e}\n")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}\n")
        return False

def scrape_with_beautifulsoup():
    """
    Alternative scraper using BeautifulSoup for web scraping
    This scrapes from CoinMarketCap website directly
    Note: This is more fragile as website structure can change
    """
    try:
        url = "https://coinmarketcap.com/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find cryptocurrency rows (structure may vary)
        # This is an example and may need adjustments
        crypto_rows = soup.find_all('tr', limit=10)
        
        for row in crypto_rows:
            # Parse the row data
            # This will depend on the actual HTML structure
            pass
        
        return True
        
    except Exception as e:
        print(f"❌ BeautifulSoup scraping error: {e}")
        return False

if __name__ == "__main__":
    # Test the scraper
    scrape_crypto_prices()
