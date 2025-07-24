import schedule
import time
import logging
import threading
from data_collector import data_collector
from twitter_analyzer import twitter_analyzer

def run_data_collection():
    """Run all data collection tasks"""
    logging.info("Starting scheduled data collection...")
    
    try:
        # Collect crypto data
        data_collector.collect_crypto_data()
        
        # Small delay between API calls
        time.sleep(5)
        
        # Collect forex data
        data_collector.collect_forex_data()
        
        # Small delay before Twitter analysis
        time.sleep(5)
        
        # Analyze Twitter sentiment
        twitter_analyzer.analyze_crypto_sentiment()
        
        # Small delay
        time.sleep(5)
        
        twitter_analyzer.analyze_forex_sentiment()
        
        logging.info("Completed scheduled data collection")
        
    except Exception as e:
        logging.error(f"Error in scheduled data collection: {e}")

def start_scheduler():
    """Start the scheduler for data collection"""
    logging.info("Starting scheduler...")
    
    # Schedule data collection every 30 minutes
    schedule.every(30).minutes.do(run_data_collection)
    
    # Run initial collection
    run_data_collection()
    
    # Keep the scheduler running
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
        except Exception as e:
            logging.error(f"Scheduler error: {e}")
            time.sleep(60)
