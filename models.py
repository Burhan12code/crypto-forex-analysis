from app import db
from datetime import datetime
from sqlalchemy import Text, Float, Integer, String, DateTime, Boolean

class CryptoData(db.Model):
    __tablename__ = 'crypto_data'
    
    id = db.Column(Integer, primary_key=True)
    symbol = db.Column(String(10), nullable=False)
    name = db.Column(String(100), nullable=False)
    price_usd = db.Column(Float, nullable=False)
    price_change_24h = db.Column(Float)
    price_change_percentage_24h = db.Column(Float)
    market_cap = db.Column(Float)
    volume_24h = db.Column(Float)
    timestamp = db.Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'name': self.name,
            'price_usd': self.price_usd,
            'price_change_24h': self.price_change_24h,
            'price_change_percentage_24h': self.price_change_percentage_24h,
            'market_cap': self.market_cap,
            'volume_24h': self.volume_24h,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

class ForexData(db.Model):
    __tablename__ = 'forex_data'
    
    id = db.Column(Integer, primary_key=True)
    base_currency = db.Column(String(3), nullable=False)
    target_currency = db.Column(String(3), nullable=False)
    exchange_rate = db.Column(Float, nullable=False)
    timestamp = db.Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'base_currency': self.base_currency,
            'target_currency': self.target_currency,
            'exchange_rate': self.exchange_rate,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

class TwitterSentiment(db.Model):
    __tablename__ = 'twitter_sentiment'
    
    id = db.Column(Integer, primary_key=True)
    keyword = db.Column(String(50), nullable=False)
    tweet_text = db.Column(Text)
    sentiment_score = db.Column(Float)  # -1 to 1, negative to positive
    sentiment_label = db.Column(String(20))  # 'positive', 'negative', 'neutral'
    tweet_id = db.Column(String(50))
    user_followers = db.Column(Integer)
    timestamp = db.Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'keyword': self.keyword,
            'tweet_text': self.tweet_text,
            'sentiment_score': self.sentiment_score,
            'sentiment_label': self.sentiment_label,
            'user_followers': self.user_followers,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

class SystemLog(db.Model):
    __tablename__ = 'system_logs'
    
    id = db.Column(Integer, primary_key=True)
    log_type = db.Column(String(20), nullable=False)  # 'info', 'error', 'warning'
    message = db.Column(Text, nullable=False)
    component = db.Column(String(50))  # 'crypto_collector', 'forex_collector', 'twitter_analyzer'
    timestamp = db.Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'log_type': self.log_type,
            'message': self.message,
            'component': self.component,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
