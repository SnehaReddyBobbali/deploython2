import requests
from bs4 import BeautifulSoup
from datetime import datetime
from database import save_crypto_data

def scrape_crypto_prices():
    """
    Scrape cryptocurrency prices by parsing the CoinGecko homepage HTML.
    This avoids using the public API and extracts visible values from the page.
    """
    print(f"\n⏰ [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting crypto price scrape (HTML)...")

    url = "https://www.coingecko.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Network error fetching CoinGecko page: {e}")
        return False

    soup = BeautifulSoup(resp.content, 'html.parser')

    # Try to find rows in common table structures
    rows = []
    table = soup.find('table')
    if table:
        tbody = table.find('tbody')
        if tbody:
            rows = tbody.find_all('tr')

    # Fallback: rows with data-coin-id (CoinGecko often includes this attribute)
    if not rows:
        rows = soup.find_all('tr', attrs={'data-coin-id': True})

    # Final fallback: any top-level tr elements
    if not rows:
        rows = soup.find_all('tr')

    if not rows:
        print('❌ Could not find crypto rows on CoinGecko page - structure may have changed')
        return False

    def parse_money(s):
        """Convert strings like '$3.38T', '$82.65B', '$1,234' to float."""
        if not s:
            return 0.0
        s = s.replace('$', '').replace(',', '').strip()
        try:
            if s.endswith('T'):
                return float(s[:-1]) * 1e12
            if s.endswith('B'):
                return float(s[:-1]) * 1e9
            if s.endswith('M'):
                return float(s[:-1]) * 1e6
            if s.endswith('K'):
                return float(s[:-1]) * 1e3
            return float(s)
        except:
            # Try to extract a number from the string
            import re
            m = re.search(r"[-+]?[0-9]*\.?[0-9]+", s)
            return float(m.group()) if m else 0.0

    scraped = 0
    for row in rows[:15]:
        try:
            # Collect text candidates
            texts = [el.get_text(separator=' ', strip=True) for el in row.find_all(['td', 'span', 'a', 'div']) if el.get_text(strip=True)]

            # Name: first alphabetic long token
            name = None
            for t in texts:
                if len(t) > 2 and any(c.isalpha() for c in t):
                    name = t
                    break

            # Symbol: look for uppercase tokens of length 2-6
            symbol = None
            import re
            for t in texts:
                match = re.search(r"\b([A-Z]{2,6})\b", t)
                if match:
                    symbol = match.group(1)
                    break

            # Price: first text containing '$' and a digit
            price = 0.0
            market_cap = 0.0
            vol_24h = 0.0
            change_24h = 0.0

            for t in texts:
                if '$' in t and any(ch.isdigit() for ch in t):
                    # parse as price if price not set
                    if price == 0.0:
                        price = parse_money(t)
                        continue
                    # next $ amount -> market cap or volume
                    if market_cap == 0.0:
                        market_cap = parse_money(t)
                        continue
                    if vol_24h == 0.0:
                        vol_24h = parse_money(t)
                        continue

                if '%' in t and any(ch.isdigit() for ch in t):
                    try:
                        change_24h = float(t.replace('%', '').replace('−', '-').strip())
                    except:
                        change_24h = 0.0

            # Image
            img = row.find('img')
            image_url = img['src'] if img and img.get('src') else ''

            if not name and not symbol:
                # skip rows without usable info
                continue

            crypto_data = {
                'symbol': (symbol or (name.split()[0] if name else 'N/A')).upper()[:10],
                'name': name or symbol or 'Unknown',
                'price': price,
                'market_cap': market_cap,
                'volume_24h': vol_24h,
                'change_24h': change_24h,
                'image_url': image_url
            }

            save_crypto_data(crypto_data)
            scraped += 1
            print(f"  ✓ Saved {crypto_data['name']} ({crypto_data['symbol']}) price: {crypto_data['price']}")

        except Exception as e:
            print(f"❌ Failed to parse a row: {e}")
            continue

    print(f"✅ Scraping complete, saved {scraped} items\n")
    return scraped > 0

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
