---
title: Crypto & Forex Analysis System
emoji: 📈
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.7.1
app_file: app_hf.py
pinned: false
license: mit
---

# Crypto & Forex Analysis System

Sistem analisis real-time untuk data cryptocurrency dan forex dengan analisis sentimen dari Twitter.

## Fitur Utama

- 📊 **Data Cryptocurrency**: Mengumpulkan data harga dan market cap dari CoinGecko API
- 💱 **Data Forex**: Kurs mata uang utama dari ExchangeRate-API  
- 🐦 **Analisis Sentimen Twitter**: Analisis sentimen tweet tentang crypto dan forex
- 📡 **RSS Feeds**: Feed RSS untuk crypto, forex, dan data sentimen
- ⏰ **Update Otomatis**: Pengumpulan data setiap 30 menit untuk menghindari rate limit
- 🌐 **Dashboard Web**: Interface responsif dengan Bootstrap dark theme

## Penggunaan

1. Akses dashboard utama untuk melihat data terkini
2. Gunakan tab berbeda untuk crypto, forex, dan analisis sentimen
3. Akses RSS feeds melalui dropdown menu atau endpoint langsung:
   - `/rss/crypto` - Feed data cryptocurrency
   - `/rss/forex` - Feed data forex
   - `/rss/sentiment` - Feed analisis sentimen

## Konfigurasi Twitter API (Opsional)

Untuk mengaktifkan analisis sentimen Twitter, tambahkan variabel environment:
- `TWITTER_BEARER_TOKEN`: Bearer token dari Twitter API v2

## Teknologi

- **Backend**: Flask, SQLAlchemy, SQLite
- **Frontend**: Bootstrap 5 (dark theme), Chart.js, Feather Icons
- **APIs**: CoinGecko, ExchangeRate-API, Twitter API v2
- **Scheduling**: Schedule library untuk pengumpulan data otomatis
- **RSS**: FeedGen untuk menghasilkan RSS feeds

## Struktur Data

### Cryptocurrency
- Symbol, nama, harga USD
- Perubahan harga 24 jam
- Market cap dan volume

### Forex
- Pasangan mata uang utama
- Kurs terkini
- Timestamp update

### Sentimen Twitter
- Keyword pencarian
- Skor sentimen (-1 sampai 1)
- Label sentimen (positif/negatif/netral)
- Text tweet dan metadata

Sistem ini dirancang untuk memberikan insight lengkap tentang tren pasar crypto dan forex melalui data harga real-time dan analisis sentimen media sosial.
