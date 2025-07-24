import tweepy
import os
import logging
import re
from datetime import datetime
from textblob import TextBlob
from app import app, db
from models import TwitterSentiment, SystemLog

class TwitterAnalyzer:
    def __init__(self):
        # Twitter API credentials from environment variables
        self.api_key = os.getenv("TWITTER_API_KEY", "")
        self.api_secret = os.getenv("TWITTER_API_SECRET", "")
        self.access_token = os.getenv("TWITTER_ACCESS_TOKEN", "")
        self.access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "")
        self.bearer_token = os.getenv("TWITTER_BEARER_TOKEN", "")
        
        self.client = None
        self.setup_twitter_client()
        
        # Keywords to search for
        self.crypto_keywords = ['bitcoin', 'ethereum', 'crypto', 'cryptocurrency', 'BTC', 'ETH', 'blockchain']
        self.forex_keywords = ['forex', 'USD', 'EUR', 'GBP', 'JPY', 'currency', 'exchange rate']
    
    def setup_twitter_client(self):
        """Setup Twitter API client"""
        try:
            if self.bearer_token:
                self.client = tweepy.Client(bearer_token=self.bearer_token)
                logging.info("Twitter client initialized successfully")
            else:
                logging.warning("Twitter Bearer Token not found. Twitter analysis will be disabled.")
        except Exception as e:
            logging.error(f"Failed to initialize Twitter client: {e}")
    
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
    
    def clean_tweet_text(self, text):
        """Clean tweet text for sentiment analysis"""
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove user mentions
        text = re.sub(r'@\w+', '', text)
        # Remove hashtags (keep the text)
        text = re.sub(r'#', '', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of text using TextBlob"""
        try:
            clean_text = self.clean_tweet_text(text)
            blob = TextBlob(clean_text)
            
            # Get polarity (-1 to 1)
            sentiment = blob.sentiment
            polarity = sentiment.polarity
            
            # Classify sentiment
            if polarity > 0.1:
                label = 'positive'
            elif polarity < -0.1:
                label = 'negative'
            else:
                label = 'neutral'
                
            return polarity, label
        except Exception as e:
            logging.error(f"Error analyzing sentiment: {e}")
            return 0.0, 'neutral'
    
    def search_and_analyze_tweets(self, keywords, max_results=50):
        """Search for tweets and analyze sentiment"""
        if not self.client:
            logging.warning("Twitter client not available")
            return 0
        
        try:
            query = ' OR '.join(keywords) + ' -is:retweet lang:en'
            
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=max_results,
                tweet_fields=['created_at', 'author_id', 'public_metrics']
            )
            
            if not tweets or not tweets.data:
                logging.info("No tweets found for the query")
                return 0
            
            analyzed_count = 0
            with app.app_context():
                for tweet in tweets.data:
                    try:
                        # Determine which keyword category this tweet belongs to
                        tweet_text_lower = tweet.text.lower()
                        matched_keyword = None
                        
                        for keyword in keywords:
                            if keyword.lower() in tweet_text_lower:
                                matched_keyword = keyword
                                break
                        
                        if not matched_keyword:
                            continue
                        
                        # Analyze sentiment
                        sentiment_score, sentiment_label = self.analyze_sentiment(tweet.text)
                        
                        # Get follower count if available
                        followers = 0
                        if hasattr(tweet, 'public_metrics') and tweet.public_metrics:
                            followers = tweet.public_metrics.get('followers_count', 0)
                        
                        # Store in database
                        twitter_entry = TwitterSentiment()
                        twitter_entry.keyword = matched_keyword
                        twitter_entry.tweet_text = tweet.text[:500]  # Truncate to fit database
                        twitter_entry.sentiment_score = sentiment_score
                        twitter_entry.sentiment_label = sentiment_label
                        twitter_entry.tweet_id = tweet.id
                        twitter_entry.user_followers = followers
                        
                        db.session.add(twitter_entry)
                        analyzed_count += 1
                        
                    except Exception as e:
                        logging.error(f"Error processing tweet {tweet.id}: {e}")
                
                db.session.commit()
                logging.info(f"Analyzed {analyzed_count} tweets")
                return analyzed_count
                
        except Exception as e:
            error_msg = f"Error searching tweets: {e}"
            logging.error(error_msg)
            self.log_system_event('error', error_msg, 'twitter_analyzer')
            return 0
    
    def analyze_crypto_sentiment(self):
        """Analyze sentiment for cryptocurrency tweets"""
        try:
            count = self.search_and_analyze_tweets(self.crypto_keywords)
            self.log_system_event('info', f'Analyzed {count} crypto tweets', 'twitter_analyzer')
            return count
        except Exception as e:
            error_msg = f"Error analyzing crypto sentiment: {e}"
            logging.error(error_msg)
            self.log_system_event('error', error_msg, 'twitter_analyzer')
            return 0
    
    def analyze_forex_sentiment(self):
        """Analyze sentiment for forex tweets"""
        try:
            count = self.search_and_analyze_tweets(self.forex_keywords)
            self.log_system_event('info', f'Analyzed {count} forex tweets', 'twitter_analyzer')
            return count
        except Exception as e:
            error_msg = f"Error analyzing forex sentiment: {e}"
            logging.error(error_msg)
            self.log_system_event('error', error_msg, 'twitter_analyzer')
            return 0

# Global instance
twitter_analyzer = TwitterAnalyzer()
