import requests
import logging
from datetime import datetime
from app import app, db
from models import CryptoData, ForexData, SystemLog

class DataCollector:
    def __init__(self):
        self.crypto_api_url = "https://api.coingecko.com/api/v3"
        self.forex_api_url = "https://api.exchangerate-api.com/v4/latest"
        
    def log_system_event(self, log_type, message, component):
        """Log system events to database"""
        with app.app_context():
            try:
                log_entry = SystemLog()
                log_entry.log_type = log_type
                log_entry.message = message
                log_entry.component = component
                db.session.add(log_entry)
                db.session.commit()
            except Exception as e:
                logging.error(f"Failed to log system event: {e}")
    
    def collect_crypto_data(self):
        """Collect cryptocurrency data from CoinGecko API"""
        try:
            logging.info("Starting crypto data collection...")
            
            # Get top 50 cryptocurrencies
            url = f"{self.crypto_api_url}/coins/markets"
            params = {
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': 50,
                'page': 1,
                'sparkline': False,
                'price_change_percentage': '24h'
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            with app.app_context():
                for coin in data:
                    try:
                        crypto_entry = CryptoData()
                        crypto_entry.symbol = coin.get('symbol', '').upper()
                        crypto_entry.name = coin.get('name', '')
                        crypto_entry.price_usd = coin.get('current_price', 0)
                        crypto_entry.price_change_24h = coin.get('price_change_24h')
                        crypto_entry.price_change_percentage_24h = coin.get('price_change_percentage_24h')
                        crypto_entry.market_cap = coin.get('market_cap')
                        crypto_entry.volume_24h = coin.get('total_volume')
                        db.session.add(crypto_entry)
                    except Exception as e:
                        logging.error(f"Error processing crypto data for {coin.get('name', 'unknown')}: {e}")
                
                db.session.commit()
                logging.info(f"Successfully collected data for {len(data)} cryptocurrencies")
                self.log_system_event('info', f'Collected {len(data)} crypto records', 'crypto_collector')
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error collecting crypto data: {e}"
            logging.error(error_msg)
            self.log_system_event('error', error_msg, 'crypto_collector')
        except Exception as e:
            error_msg = f"Error collecting crypto data: {e}"
            logging.error(error_msg)
            self.log_system_event('error', error_msg, 'crypto_collector')
    
    def collect_forex_data(self):
        """Collect forex data from ExchangeRate-API"""
        try:
            logging.info("Starting forex data collection...")
            
            # Major currency pairs
            major_pairs = [
                ('USD', 'EUR'), ('USD', 'GBP'), ('USD', 'JPY'), ('USD', 'CHF'),
                ('USD', 'CAD'), ('USD', 'AUD'), ('USD', 'NZD'), ('EUR', 'GBP'),
                ('EUR', 'JPY'), ('GBP', 'JPY')
            ]
            
            with app.app_context():
                collected_count = 0
                for base, target in major_pairs:
                    try:
                        url = f"{self.forex_api_url}/{base}"
                        response = requests.get(url, timeout=30)
                        response.raise_for_status()
                        
                        data = response.json()
                        rates = data.get('rates', {})
                        
                        if target in rates:
                            forex_entry = ForexData()
                            forex_entry.base_currency = base
                            forex_entry.target_currency = target
                            forex_entry.exchange_rate = rates[target]
                            db.session.add(forex_entry)
                            collected_count += 1
                    except Exception as e:
                        logging.error(f"Error collecting forex data for {base}/{target}: {e}")
                
                db.session.commit()
                logging.info(f"Successfully collected {collected_count} forex pairs")
                self.log_system_event('info', f'Collected {collected_count} forex records', 'forex_collector')
                
        except Exception as e:
            error_msg = f"Error collecting forex data: {e}"
            logging.error(error_msg)
            self.log_system_event('error', error_msg, 'forex_collector')

# Global instance
data_collector = DataCollector()
