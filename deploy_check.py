#!/usr/bin/env python3
"""
Script untuk mengecek kesiapan deployment ke Hugging Face Spaces
"""

import os
import sys
import requests
from datetime import datetime

def check_file_exists(filename):
    """Check if required file exists"""
    if os.path.exists(filename):
        print(f"✅ {filename} - Found")
        return True
    else:
        print(f"❌ {filename} - Missing")
        return False

def check_api_endpoints():
    """Test API endpoints"""
    print("\n🔍 Testing API connectivity...")
    
    # Test CoinGecko API
    try:
        response = requests.get("https://api.coingecko.com/api/v3/ping", timeout=10)
        if response.status_code == 200:
            print("✅ CoinGecko API - Accessible")
        else:
            print(f"⚠️ CoinGecko API - Status {response.status_code}")
    except Exception as e:
        print(f"❌ CoinGecko API - Error: {e}")
    
    # Test ExchangeRate API
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10)
        if response.status_code == 200:
            print("✅ ExchangeRate API - Accessible")
        else:
            print(f"⚠️ ExchangeRate API - Status {response.status_code}")
    except Exception as e:
        print(f"❌ ExchangeRate API - Error: {e}")

def check_twitter_config():
    """Check Twitter configuration"""
    twitter_token = os.getenv("TWITTER_BEARER_TOKEN")
    if twitter_token:
        print("✅ Twitter Bearer Token - Configured")
        if len(twitter_token) > 50:
            print("✅ Token length looks valid")
        else:
            print("⚠️ Token might be invalid (too short)")
    else:
        print("⚠️ Twitter Bearer Token - Not configured (sentiment analysis will be disabled)")

def check_dependencies():
    """Check if key dependencies are available"""
    print("\n📦 Checking dependencies...")
    
    required_modules = [
        'flask', 'flask_sqlalchemy', 'requests', 'schedule', 
        'tweepy', 'textblob', 'feedgen', 'sqlalchemy'
    ]
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} - Available")
        except ImportError:
            print(f"❌ {module} - Missing")

def main():
    print("🚀 Crypto & Forex Analysis - Deployment Check")
    print("=" * 50)
    
    print("\n📁 Checking required files...")
    required_files = [
        'app_hf.py',
        'models.py',
        'routes.py', 
        'data_collector.py',
        'twitter_analyzer.py',
        'rss_generator.py',
        'scheduler.py',
        'templates/base.html',
        'templates/index.html',
        'static/js/main.js',
        'static/css/custom.css'
    ]
    
    all_files_present = True
    for file in required_files:
        if not check_file_exists(file):
            all_files_present = False
    
    check_dependencies()
    check_api_endpoints()
    check_twitter_config()
    
    print("\n" + "=" * 50)
    if all_files_present:
        print("✅ Deployment Check: READY for Hugging Face Spaces!")
        print("\n📋 Next steps:")
        print("1. Create GitHub repository")
        print("2. Upload all files to GitHub")
        print("3. Create HF Space and connect to GitHub")
        print("4. Add TWITTER_BEARER_TOKEN to HF Spaces secrets (optional)")
        print("5. Wait for deployment to complete")
    else:
        print("❌ Deployment Check: Missing files detected")
        print("Please ensure all required files are present before deployment")
    
    print(f"\n⏰ Check completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()