from flask import render_template, Response, jsonify, request
from datetime import datetime, timedelta
from app import app, db
from models import CryptoData, ForexData, TwitterSentiment, SystemLog
from rss_generator import rss_generator
import json

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/crypto/latest')
def api_crypto_latest():
    """API endpoint for latest crypto data"""
    try:
        # Get latest crypto data (one per symbol, most recent)
        subquery = db.session.query(
            CryptoData.symbol,
            db.func.max(CryptoData.timestamp).label('max_timestamp')
        ).group_by(CryptoData.symbol).subquery()
        
        latest_crypto = db.session.query(CryptoData).join(
            subquery,
            (CryptoData.symbol == subquery.c.symbol) & 
            (CryptoData.timestamp == subquery.c.max_timestamp)
        ).order_by(CryptoData.market_cap.desc()).limit(20).all()
        
        data = [crypto.to_dict() for crypto in latest_crypto]
        return jsonify({'success': True, 'data': data})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/forex/latest')
def api_forex_latest():
    """API endpoint for latest forex data"""
    try:
        # Get latest forex data (one per pair, most recent)
        subquery = db.session.query(
            ForexData.base_currency,
            ForexData.target_currency,
            db.func.max(ForexData.timestamp).label('max_timestamp')
        ).group_by(ForexData.base_currency, ForexData.target_currency).subquery()
        
        latest_forex = db.session.query(ForexData).join(
            subquery,
            (ForexData.base_currency == subquery.c.base_currency) & 
            (ForexData.target_currency == subquery.c.target_currency) &
            (ForexData.timestamp == subquery.c.max_timestamp)
        ).order_by(ForexData.timestamp.desc()).all()
        
        data = [forex.to_dict() for forex in latest_forex]
        return jsonify({'success': True, 'data': data})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/sentiment/summary')
def api_sentiment_summary():
    """API endpoint for sentiment analysis summary"""
    try:
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        
        # Get sentiment distribution for crypto
        crypto_sentiment = db.session.query(
            TwitterSentiment.sentiment_label,
            db.func.count(TwitterSentiment.id).label('count'),
            db.func.avg(TwitterSentiment.sentiment_score).label('avg_score')
        ).filter(
            TwitterSentiment.timestamp >= cutoff_time,
            TwitterSentiment.keyword.in_(['bitcoin', 'ethereum', 'crypto', 'cryptocurrency', 'BTC', 'ETH', 'blockchain'])
        ).group_by(TwitterSentiment.sentiment_label).all()
        
        # Get sentiment distribution for forex
        forex_sentiment = db.session.query(
            TwitterSentiment.sentiment_label,
            db.func.count(TwitterSentiment.id).label('count'),
            db.func.avg(TwitterSentiment.sentiment_score).label('avg_score')
        ).filter(
            TwitterSentiment.timestamp >= cutoff_time,
            TwitterSentiment.keyword.in_(['forex', 'USD', 'EUR', 'GBP', 'JPY', 'currency', 'exchange rate'])
        ).group_by(TwitterSentiment.sentiment_label).all()
        
        crypto_data = {item.sentiment_label: {'count': item.count, 'avg_score': float(item.avg_score or 0)} for item in crypto_sentiment}
        forex_data = {item.sentiment_label: {'count': item.count, 'avg_score': float(item.avg_score or 0)} for item in forex_sentiment}
        
        return jsonify({
            'success': True,
            'data': {
                'crypto': crypto_data,
                'forex': forex_data
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/system/logs')
def api_system_logs():
    """API endpoint for system logs"""
    try:
        logs = db.session.query(SystemLog).order_by(
            SystemLog.timestamp.desc()
        ).limit(50).all()
        
        data = [log.to_dict() for log in logs]
        return jsonify({'success': True, 'data': data})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/rss/crypto')
def rss_crypto():
    """RSS feed for cryptocurrency data"""
    try:
        rss_content = rss_generator.generate_crypto_feed()
        if rss_content:
            return Response(rss_content, mimetype='application/rss+xml')
        else:
            return Response("Error generating RSS feed", status=500)
    except Exception as e:
        return Response(f"Error: {str(e)}", status=500)

@app.route('/rss/forex')
def rss_forex():
    """RSS feed for forex data"""
    try:
        rss_content = rss_generator.generate_forex_feed()
        if rss_content:
            return Response(rss_content, mimetype='application/rss+xml')
        else:
            return Response("Error generating RSS feed", status=500)
    except Exception as e:
        return Response(f"Error: {str(e)}", status=500)

@app.route('/rss/sentiment')
def rss_sentiment():
    """RSS feed for sentiment analysis"""
    try:
        rss_content = rss_generator.generate_sentiment_feed()
        if rss_content:
            return Response(rss_content, mimetype='application/rss+xml')
        else:
            return Response("Error generating RSS feed", status=500)
    except Exception as e:
        return Response(f"Error: {str(e)}", status=500)

@app.route('/crypto')
def crypto_page():
    """Cryptocurrency data page"""
    return render_template('index.html', active_tab='crypto')

@app.route('/forex')
def forex_page():
    """Forex data page"""
    return render_template('index.html', active_tab='forex')

@app.route('/sentiment')
def sentiment_page():
    """Sentiment analysis page"""
    return render_template('index.html', active_tab='sentiment')
