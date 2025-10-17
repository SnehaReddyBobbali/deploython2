import sqlite3
from datetime import datetime
import os

# Allow overriding DB path via environment variable for deployments
DATABASE_PATH = os.environ.get('DATABASE_PATH', 'crypto_data.db')

def get_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with required tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create cryptos table for latest prices
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cryptos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            market_cap REAL,
            volume_24h REAL,
            change_24h REAL,
            image_url TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create price_history table for tracking price changes over time
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            price REAL NOT NULL,
            market_cap REAL,
            volume_24h REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (symbol) REFERENCES cryptos (symbol)
        )
    ''')
    
    # Create index for faster queries
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_symbol_timestamp 
        ON price_history (symbol, timestamp)
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully")

def save_crypto_data(crypto_data):
    """Save or update cryptocurrency data"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Insert or update the latest price in cryptos table
        cursor.execute('''
            INSERT INTO cryptos (symbol, name, price, market_cap, volume_24h, change_24h, image_url, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(symbol) DO UPDATE SET
                name = excluded.name,
                price = excluded.price,
                market_cap = excluded.market_cap,
                volume_24h = excluded.volume_24h,
                change_24h = excluded.change_24h,
                image_url = excluded.image_url,
                last_updated = excluded.last_updated
        ''', (
            crypto_data['symbol'],
            crypto_data['name'],
            crypto_data['price'],
            crypto_data['market_cap'],
            crypto_data['volume_24h'],
            crypto_data['change_24h'],
            crypto_data['image_url'],
            datetime.now()
        ))
        
        # Also save to price_history for historical tracking
        cursor.execute('''
            INSERT INTO price_history (symbol, price, market_cap, volume_24h, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            crypto_data['symbol'],
            crypto_data['price'],
            crypto_data['market_cap'],
            crypto_data['volume_24h'],
            datetime.now()
        ))
        
        conn.commit()
    except Exception as e:
        print(f"❌ Error saving {crypto_data['symbol']}: {e}")
        conn.rollback()
    finally:
        conn.close()

def get_all_cryptos():
    """Get all cryptocurrencies with their latest prices"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT symbol, name, price, market_cap, volume_24h, change_24h, image_url, last_updated
        FROM cryptos
        ORDER BY market_cap DESC
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def get_crypto_history(symbol, limit=24):
    """Get price history for a specific cryptocurrency"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT price, market_cap, volume_24h, timestamp
        FROM price_history
        WHERE symbol = ?
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (symbol, limit))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def cleanup_old_data(days=7):
    """Remove price history older than specified days"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM price_history
        WHERE timestamp < datetime('now', '-' || ? || ' days')
    ''', (days,))
    
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    
    print(f"🧹 Cleaned up {deleted} old records")
    return deleted

if __name__ == "__main__":
    # Test database initialization
    init_db()
    print("Database test completed!")
