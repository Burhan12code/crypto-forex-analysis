# Crypto & Forex Analysis System

## Overview

This is a Flask-based web application that collects, analyzes, and displays real-time cryptocurrency and forex market data with sentiment analysis from Twitter. The system provides a comprehensive dashboard for monitoring market trends, price movements, and social media sentiment to support financial analysis and decision-making.

## User Preferences

Preferred communication style: Simple, everyday language.
User language: Indonesian - communicate in Bahasa Indonesia when appropriate.
Deployment preference: Hugging Face Spaces for public deployment.

## System Architecture

The application follows a modular Flask architecture with the following key design decisions:

### Backend Architecture
- **Flask Web Framework**: Chosen for its simplicity and flexibility in building web APIs and serving templates
- **SQLAlchemy ORM**: Used for database operations with a declarative base model approach
- **Modular Design**: Separated concerns with dedicated modules for data collection, analysis, RSS generation, and scheduling

### Database Architecture
- **SQLite/PostgreSQL**: Uses SQLite for development with PostgreSQL support through environment configuration
- **Three Main Entities**: CryptoData, ForexData, and TwitterSentiment models
- **Connection Pooling**: Configured with pool recycling and pre-ping for reliability

### Scheduling System
- **Background Threading**: Runs data collection tasks in separate daemon threads
- **Schedule Library**: Uses the `schedule` library for periodic data collection every 30 minutes
- **Concurrent API Calls**: Manages delays between API calls to respect rate limits

## Key Components

### Data Collection (`data_collector.py`)
- **CoinGecko Integration**: Collects top 50 cryptocurrency data including prices, market cap, and volume
- **Exchange Rate API**: Gathers forex data for major currency pairs
- **Error Handling**: Comprehensive logging and error recovery mechanisms
- **Database Persistence**: Stores collected data with timestamps for historical analysis

### Twitter Sentiment Analysis (`twitter_analyzer.py`)
- **Twitter API v2**: Uses bearer token authentication for tweet collection
- **TextBlob Sentiment**: Analyzes sentiment polarity and subjectivity of tweets
- **Keyword Filtering**: Searches for crypto and forex-related keywords
- **Rate Limiting**: Handles Twitter API rate limits gracefully

### RSS Feed Generation (`rss_generator.py`)
- **FeedGen Library**: Creates RSS feeds for crypto and forex data
- **Real-time Updates**: Generates feeds with latest market data and price changes
- **Rich Content**: Includes market indicators and formatted descriptions

### Web Interface
- **Bootstrap Dark Theme**: Modern, responsive UI with dark theme support
- **Real-time Updates**: JavaScript-based dashboard with periodic data refresh
- **Chart Integration**: Chart.js for data visualization
- **Feather Icons**: Clean iconography throughout the interface

## Data Flow

1. **Scheduled Collection**: Background scheduler triggers data collection every 30 minutes
2. **API Integration**: Data collector fetches from CoinGecko, Exchange Rate API, and Twitter
3. **Data Processing**: Raw data is processed, analyzed, and stored in the database
4. **Web APIs**: Flask routes serve processed data as JSON APIs
5. **Frontend Display**: JavaScript fetches data and updates the dashboard interface
6. **RSS Generation**: RSS feeds are generated on-demand for external consumption

## External Dependencies

### APIs
- **CoinGecko API**: Free tier for cryptocurrency market data
- **Exchange Rate API**: Currency exchange rates
- **Twitter API v2**: Social media sentiment data (requires bearer token)

### Libraries
- **Flask**: Web framework and routing
- **SQLAlchemy**: Database ORM and connection management
- **Requests**: HTTP client for API calls
- **TextBlob**: Natural language processing for sentiment analysis
- **FeedGen**: RSS feed generation
- **Schedule**: Task scheduling
- **Tweepy**: Twitter API client

### Frontend
- **Bootstrap**: UI framework with dark theme
- **Chart.js**: Data visualization
- **Feather Icons**: Icon library

## Deployment Strategy

### Environment Configuration
- **Database URL**: Configurable via `DATABASE_URL` environment variable
- **Session Secret**: Uses `SESSION_SECRET` for Flask sessions
- **Twitter Credentials**: Multiple environment variables for Twitter API access

### Development Setup
- **Debug Mode**: Flask debug mode enabled for development
- **Host Configuration**: Binds to `0.0.0.0:5000` for external access
- **Proxy Support**: ProxyFix middleware for proper header handling

### Production Considerations
- **Connection Pooling**: Configured for production database connections
- **Logging**: Structured logging throughout the application
- **Thread Safety**: Background tasks run in daemon threads
- **Error Recovery**: Comprehensive exception handling and system logging

The system is designed to be easily deployable on platforms like Replit, with environment-based configuration and automatic database initialization.