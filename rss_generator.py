from feedgen.feed import FeedGenerator
from datetime import datetime, timedelta
import logging
import os
from app import app, db
from models import CryptoData, ForexData, TwitterSentiment

class RSSGenerator:
    def __init__(self):
        # Auto-detect base URL for different environments
        if os.getenv('SPACE_ID'):  # Hugging Face Spaces
            self.base_url = f"https://{os.getenv('SPACE_AUTHOR_NAME', 'user')}-{os.getenv('SPACE_REPO_NAME', 'crypto-forex-analysis')}.hf.space"
        else:
            self.base_url = "http://localhost:5000"
    
    def generate_crypto_feed(self):
        """Generate RSS feed for cryptocurrency data"""
        try:
            fg = FeedGenerator()
            fg.title('Crypto Market Analysis')
            fg.link(href=f'{self.base_url}/crypto', rel='alternate')
            fg.description('Latest cryptocurrency market data and analysis')
            fg.language('en')
            fg.lastBuildDate(datetime.utcnow())
            
            with app.app_context():
                # Get latest crypto data from last 24 hours
                cutoff_time = datetime.utcnow() - timedelta(hours=24)
                latest_crypto = db.session.query(CryptoData).filter(
                    CryptoData.timestamp >= cutoff_time
                ).order_by(CryptoData.timestamp.desc()).limit(50).all()
                
                for crypto in latest_crypto:
                    fe = fg.add_entry()
                    fe.id(f'{self.base_url}/crypto/{crypto.id}')
                    
                    # Create title with price change indicator
                    change_indicator = "📈" if crypto.price_change_percentage_24h and crypto.price_change_percentage_24h > 0 else "📉"
                    title = f"{change_indicator} {crypto.name} ({crypto.symbol}) - ${crypto.price_usd:.2f}"
                    fe.title(title)
                    
                    fe.link(href=f'{self.base_url}/crypto/{crypto.id}')
                    fe.pubDate(crypto.timestamp.replace(tzinfo=None) if crypto.timestamp else datetime.utcnow())
                    
                    # Create description with market data
                    description = f"""
                    <h3>{crypto.name} ({crypto.symbol})</h3>
                    <p><strong>Current Price:</strong> ${crypto.price_usd:.2f}</p>
                    <p><strong>24h Change:</strong> {crypto.price_change_percentage_24h:.2f}% (${crypto.price_change_24h:.2f})</p>
                    <p><strong>Market Cap:</strong> ${crypto.market_cap:,.0f}</p>
                    <p><strong>24h Volume:</strong> ${crypto.volume_24h:,.0f}</p>
                    <p><strong>Last Updated:</strong> {crypto.timestamp.strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
                    """
                    fe.description(description)
                
                return fg.rss_str(pretty=True)
                
        except Exception as e:
            logging.error(f"Error generating crypto RSS feed: {e}")
            return None
    
    def generate_forex_feed(self):
        """Generate RSS feed for forex data"""
        try:
            fg = FeedGenerator()
            fg.title('Forex Market Analysis')
            fg.link(href=f'{self.base_url}/forex', rel='alternate')
            fg.description('Latest forex exchange rates and analysis')
            fg.language('en')
            fg.lastBuildDate(datetime.utcnow())
            
            with app.app_context():
                # Get latest forex data from last 24 hours
                cutoff_time = datetime.utcnow() - timedelta(hours=24)
                latest_forex = db.session.query(ForexData).filter(
                    ForexData.timestamp >= cutoff_time
                ).order_by(ForexData.timestamp.desc()).limit(20).all()
                
                for forex in latest_forex:
                    fe = fg.add_entry()
                    fe.id(f'{self.base_url}/forex/{forex.id}')
                    
                    title = f"{forex.base_currency}/{forex.target_currency} - {forex.exchange_rate:.4f}"
                    fe.title(title)
                    
                    fe.link(href=f'{self.base_url}/forex/{forex.id}')
                    fe.pubDate(forex.timestamp.replace(tzinfo=None) if forex.timestamp else datetime.utcnow())
                    
                    description = f"""
                    <h3>{forex.base_currency}/{forex.target_currency}</h3>
                    <p><strong>Exchange Rate:</strong> {forex.exchange_rate:.4f}</p>
                    <p><strong>Last Updated:</strong> {forex.timestamp.strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
                    """
                    fe.description(description)
                
                return fg.rss_str(pretty=True)
                
        except Exception as e:
            logging.error(f"Error generating forex RSS feed: {e}")
            return None
    
    def generate_sentiment_feed(self):
        """Generate RSS feed for sentiment analysis"""
        try:
            fg = FeedGenerator()
            fg.title('Market Sentiment Analysis')
            fg.link(href=f'{self.base_url}/sentiment', rel='alternate')
            fg.description('Latest market sentiment from social media analysis')
            fg.language('en')
            fg.lastBuildDate(datetime.utcnow())
            
            with app.app_context():
                # Get latest sentiment data from last 24 hours
                cutoff_time = datetime.utcnow() - timedelta(hours=24)
                latest_sentiment = db.session.query(TwitterSentiment).filter(
                    TwitterSentiment.timestamp >= cutoff_time
                ).order_by(TwitterSentiment.timestamp.desc()).limit(30).all()
                
                for sentiment in latest_sentiment:
                    fe = fg.add_entry()
                    fe.id(f'{self.base_url}/sentiment/{sentiment.id}')
                    
                    # Sentiment emoji
                    emoji = "😊" if sentiment.sentiment_label == 'positive' else "😔" if sentiment.sentiment_label == 'negative' else "😐"
                    title = f"{emoji} {sentiment.keyword.upper()} Sentiment: {sentiment.sentiment_label.title()}"
                    fe.title(title)
                    
                    fe.link(href=f'{self.base_url}/sentiment/{sentiment.id}')
                    fe.pubDate(sentiment.timestamp.replace(tzinfo=None) if sentiment.timestamp else datetime.utcnow())
                    
                    description = f"""
                    <h3>Sentiment Analysis for {sentiment.keyword.upper()}</h3>
                    <p><strong>Sentiment:</strong> {sentiment.sentiment_label.title()} ({sentiment.sentiment_score:.2f})</p>
                    <p><strong>Sample Tweet:</strong> "{sentiment.tweet_text[:200]}..."</p>
                    <p><strong>Analyzed:</strong> {sentiment.timestamp.strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
                    """
                    fe.description(description)
                
                return fg.rss_str(pretty=True)
                
        except Exception as e:
            logging.error(f"Error generating sentiment RSS feed: {e}")
            return None

# Global instance
rss_generator = RSSGenerator()
