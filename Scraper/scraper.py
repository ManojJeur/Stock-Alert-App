import yfinance as yf
import json
import time
import requests
from datetime import datetime
import sqlite3
import os

class StockScraper:
    def __init__(self, db_path='stock_alerts.db'):
        self.db_path = db_path
        self.api_url = "http://localhost:8000"  # Backend API URL
        
    def get_stock_price(self, symbol):
        """Fetch current stock price using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
            return float(current_price) if current_price else None
        except Exception as e:
            print(f"Error fetching price for {symbol}: {e}")
            return None
    
    def get_stocks_to_monitor(self):
        """Get list of stocks from database that need monitoring"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, symbol, alert_price, alert_type, current_price
            FROM stocks WHERE is_active = 1
        ''')
        
        stocks = []
        for row in cursor.fetchall():
            stocks.append({
                'id': row[0],
                'symbol': row[1],
                'alert_price': row[2],
                'alert_type': row[3],
                'current_price': row[4]
            })
        
        conn.close()
        return stocks
    
    def check_price_alerts(self, stock_data, current_price):
        """Check if current price triggers any alerts"""
        alerts = []
        
        if stock_data['alert_type'] == 'buy' and current_price <= stock_data['alert_price']:
            alerts.append({
                'type': 'buy_alert',
                'message': f"BUY ALERT: {stock_data['symbol']} is at ${current_price:.2f} (target: ${stock_data['alert_price']:.2f})"
            })
        elif stock_data['alert_type'] == 'sell' and current_price >= stock_data['alert_price']:
            alerts.append({
                'type': 'sell_alert',
                'message': f"SELL ALERT: {stock_data['symbol']} is at ${current_price:.2f} (target: ${stock_data['alert_price']:.2f})"
            })
        
        return alerts
    
    def update_stock_price(self, stock_id, current_price):
        """Update stock price in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE stocks SET current_price = ? WHERE id = ?
        ''', (current_price, stock_id))
        
        conn.commit()
        conn.close()
    
    def send_alert(self, stock_id, message):
        """Send alert to backend API"""
        try:
            response = requests.post(f"{self.api_url}/alerts", 
                                   json={"stock_id": stock_id, "message": message})
            if response.status_code == 200:
                print(f"Alert sent: {message}")
            else:
                print(f"Failed to send alert: {response.status_code}")
        except Exception as e:
            print(f"Error sending alert: {e}")
    
    def scrape_and_check(self):
        """Main scraping function - check all stocks for alerts"""
        print(f"Starting stock check at {datetime.now()}")
        
        stocks = self.get_stocks_to_monitor()
        
        if not stocks:
            print("No stocks to monitor")
            return
        
        for stock in stocks:
            symbol = stock['symbol']
            print(f"Checking {symbol}...")
            
            # Get current price
            current_price = self.get_stock_price(symbol)
            
            if current_price is None:
                print(f"Could not fetch price for {symbol}")
                continue
            
            # Update price in database
            self.update_stock_price(stock['id'], current_price)
            
            # Check for alerts
            alerts = self.check_price_alerts(stock, current_price)
            
            # Send alerts if any
            for alert in alerts:
                self.send_alert(stock['id'], alert['message'])
            
            print(f"{symbol}: ${current_price:.2f}")
            
            # Small delay to avoid rate limiting
            time.sleep(1)
        
        print(f"Stock check completed at {datetime.now()}")
    
    def add_sample_stocks(self):
        """Add some sample stocks for testing"""
        sample_stocks = [
            {"symbol": "AAPL", "name": "Apple Inc.", "alert_price": 150.0, "alert_type": "buy"},
            {"symbol": "GOOGL", "name": "Alphabet Inc.", "alert_price": 2800.0, "alert_type": "sell"},
            {"symbol": "MSFT", "name": "Microsoft Corporation", "alert_price": 300.0, "alert_type": "buy"},
            {"symbol": "TSLA", "name": "Tesla Inc.", "alert_price": 200.0, "alert_type": "buy"},
            {"symbol": "AMZN", "name": "Amazon.com Inc.", "alert_price": 3200.0, "alert_type": "sell"}
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for stock in sample_stocks:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO stocks (symbol, name, alert_price, alert_type)
                    VALUES (?, ?, ?, ?)
                ''', (stock['symbol'], stock['name'], stock['alert_price'], stock['alert_type']))
            except Exception as e:
                print(f"Error adding {stock['symbol']}: {e}")
        
        conn.commit()
        conn.close()
        print("Sample stocks added successfully")

def main():
    scraper = StockScraper()
    
    # Add sample stocks if database is empty
    scraper.add_sample_stocks()
    
    # Run the scraper
    scraper.scrape_and_check()

if __name__ == "__main__":
    main()
