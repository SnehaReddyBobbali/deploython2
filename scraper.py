import requests
from bs4 import BeautifulSoup
from datetime import datetime
from database import save_crypto_data, prune_cryptos

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

    # Try to find the main listings table by matching headers
    rows = []
    target_table = None
    for table in soup.find_all('table'):
        thead = table.find('thead')
        if not thead:
            continue
        headers = [th.get_text(strip=True).lower() for th in thead.find_all('th')]
        if any('price' in h for h in headers) and any('market' in h for h in headers):
            target_table = table
            break

    header_map = {}
    if target_table:
        # Build header index map
        thead = target_table.find('thead')
        headers = [th.get_text(strip=True).lower() for th in thead.find_all('th')] if thead else []
        def find_col_idx(names):
            for i, h in enumerate(headers):
                if any(n in h for n in names):
                    return i
            return None
        def find_24h_idx():
            for i, h in enumerate(headers):
                if '24h' in h and '7d' not in h and '1h' not in h and 'volume' not in h:
                    return i
            return None
        header_map = {
            'rank': find_col_idx(['#', 'rank']),
            'coin': find_col_idx(['coin']),
            'price': find_col_idx(['price']),
            'change24': find_24h_idx(),
            'volume24': find_col_idx(['24h volume', 'volume']),
            'marketcap': find_col_idx(['market cap', 'market'])
        }
        tbody = target_table.find('tbody')
        if tbody:
            rows = tbody.find_all('tr', recursive=False)

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
    top_symbols = []
    for row in rows:
        try:
            # Respect rank 1..10 only, when rank cell is present
            rank = None
            tds = row.find_all('td', recursive=False)
            # Use header map for rank when possible
            if tds:
                if header_map.get('rank') is not None and len(tds) > header_map['rank']:
                    rank_text = tds[header_map['rank']].get_text(strip=True)
                else:
                    # Skip favorites column if present (first td has star)
                    rank_td_idx = 1 if len(tds) > 1 and tds[0].find('svg') else 0
                    rank_text = tds[rank_td_idx].get_text(strip=True)
                try:
                    rank = int(rank_text.replace('#', '').strip())
                except:
                    rank = None
            if rank is not None and (rank < 1 or rank > 10):
                continue
            # Prefer column-based parsing when table cells are available
            tds = row.find_all('td', recursive=False)
            name = None
            symbol = None
            price = 0.0
            change_24h = 0.0
            change_dir = None
            vol_24h = 0.0
            market_cap = 0.0

            if tds and len(tds) >= 5:
                # Use header_map to pick the right columns when available
                if header_map.get('coin') is not None and len(tds) > header_map['coin']:
                    coin_cell = tds[header_map['coin']]
                else:
                    # Fallback: if first td is star and second is rank, coin is third
                    if len(tds) > 2 and (('#' in tds[1].get_text()) or tds[1].get_text(strip=True).isdigit()):
                        coin_cell = tds[2]
                    else:
                        coin_cell = tds[1] if len(tds) > 1 else None
                price_cell = tds[header_map.get('price')] if header_map.get('price') is not None and len(tds) > header_map['price'] else (tds[2] if len(tds) > 2 else None)
                change24_cell = tds[header_map.get('change24')] if header_map.get('change24') is not None and len(tds) > header_map['change24'] else None
                vol_cell = tds[header_map.get('volume24')] if header_map.get('volume24') is not None and len(tds) > header_map['volume24'] else None
                mcap_cell = tds[header_map.get('marketcap')] if header_map.get('marketcap') is not None and len(tds) > header_map['marketcap'] else None

                if coin_cell:
                    # Prefer image alt for the name—it’s often clean
                    img = coin_cell.find('img')
                    name = img.get('alt') if img and img.get('alt') else None
                    if not name:
                        a = coin_cell.find('a')
                        name = a.get_text(strip=True) if a else coin_cell.get_text(strip=True)
                    # symbol within coin cell: first uppercase token (2-6)
                    import re
                    text_in_coin = coin_cell.get_text(separator=' ', strip=True)
                    tokens = [t for t in text_in_coin.split() if t.isupper() and 2 <= len(t) <= 6 and t != 'BUY']
                    symbol = tokens[0] if tokens else None

                if price_cell:
                    price = parse_money(price_cell.get_text(strip=True))
                if change24_cell:
                    try:
                        raw_change = change24_cell.get_text(strip=True)
                        change_24h = float(raw_change.replace('%', '').replace('−', '-'))
                        change_dir = 'up' if change_24h > 0 else 'down' if change_24h < 0 else 'flat'
                    except:
                        change_24h = 0.0
                        change_dir = 'flat'
                if vol_cell:
                    vol_24h = parse_money(vol_cell.get_text(strip=True))
                if mcap_cell:
                    market_cap = parse_money(mcap_cell.get_text(strip=True))
                # If either volume or market cap is missing, try to infer from remaining $ cells
                if market_cap == 0.0 or vol_24h == 0.0:
                    money_vals = [parse_money(td.get_text(strip=True)) for td in tds if '$' in td.get_text()]
                    # remove the price value if present
                    money_vals = [v for v in money_vals if v != price and v > 0]
                    if money_vals:
                        # Market cap is typically the largest amount; volume is the next
                        money_vals.sort(reverse=True)
                        if market_cap == 0.0:
                            market_cap = money_vals[0]
                        if vol_24h == 0.0 and len(money_vals) > 1:
                            vol_24h = money_vals[1]
            else:
                # Fallback to heuristic parsing
                texts = [el.get_text(separator=' ', strip=True) for el in row.find_all(['td', 'span', 'a', 'div']) if el.get_text(strip=True)]
                # Name
                for t in texts:
                    if len(t) > 2 and any(c.isalpha() for c in t):
                        name = t
                        break
                # Symbol
                import re
                for t in texts:
                    match = re.search(r"\b([A-Z]{2,6})\b", t)
                    if match:
                        symbol = match.group(1)
                        break
                # Money fields
                for t in texts:
                    if '$' in t and any(ch.isdigit() for ch in t):
                        if price == 0.0:
                            price = parse_money(t)
                            continue
                        if market_cap == 0.0:
                            market_cap = parse_money(t)
                            continue
                        if vol_24h == 0.0:
                            vol_24h = parse_money(t)
                            continue
                    if '%' in t and any(ch.isdigit() for ch in t):
                        try:
                            change_24h = float(t.replace('%', '').replace('−', '-').strip())
                            change_dir = 'up' if change_24h > 0 else 'down' if change_24h < 0 else 'flat'
                        except:
                            change_24h = 0.0
                            change_dir = 'flat'

            # Image
            img = row.find('img')
            image_url = img['src'] if img and img.get('src') else ''

            if not name and not symbol:
                continue

            crypto_data = {
                'symbol': (symbol or (name.split()[0] if name else 'N/A')).upper()[:10],
                'name': name or symbol or 'Unknown',
                'price': price,
                'market_cap': market_cap,
                'volume_24h': vol_24h,
                'change_24h': change_24h,
                'change_dir': change_dir or ('up' if change_24h > 0 else 'down' if change_24h < 0 else 'flat'),
                'image_url': image_url
            }

            save_crypto_data(crypto_data)
            if crypto_data['symbol'] not in top_symbols:
                top_symbols.append(crypto_data['symbol'])
            scraped += 1
            print(f"  ✓ Saved {crypto_data['name']} ({crypto_data['symbol']}) price: {crypto_data['price']}")

        except Exception as e:
            print(f"❌ Failed to parse a row: {e}")
            continue

        # Break once we have 10
        if len(top_symbols) >= 10:
            break

    # Prune to exactly the top 10 we captured
    if top_symbols:
        deleted = prune_cryptos(top_symbols)
        if deleted:
            print(f"🧹 Pruned {deleted} non-top entries from DB")

    print(f"✅ Scraping complete, saved {scraped} items (top 10 enforced)\n")
    return scraped > 0

if __name__ == "__main__":
    # Test the scraper
    scrape_crypto_prices()
