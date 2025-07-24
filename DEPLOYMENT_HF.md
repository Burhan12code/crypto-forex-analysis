# Panduan Deployment ke Hugging Face Spaces

## Langkah-langkah Deployment

### 1. Persiapan Repository
1. Buat repository baru di GitHub dengan nama `crypto-forex-analysis`
2. Upload semua file dari project ini ke repository tersebut
3. Pastikan file `README_HF.md` direnamed menjadi `README.md`

### 2. Buat Hugging Face Space
1. Buka [Hugging Face Spaces](https://huggingface.co/spaces)
2. Klik "Create new Space"
3. Isi informasi:
   - **Space name**: `crypto-forex-analysis`
   - **License**: MIT
   - **SDK**: Gradio
   - **Hardware**: CPU basic (gratis)
4. Pilih "Connect to GitHub" dan hubungkan dengan repository Anda

### 3. Konfigurasi Environment Variables (Opsional)
Untuk mengaktifkan analisis Twitter, tambahkan secrets di HF Spaces:
1. Buka Settings > Repository secrets
2. Tambahkan:
   - `TWITTER_BEARER_TOKEN`: Bearer token dari Twitter API

### 4. File Penting untuk HF Spaces

**app_hf.py**: Entry point aplikasi yang dikonfigurasi untuk HF Spaces
- Port 7860 (standar HF Spaces)
- SQLite database (tidak perlu PostgreSQL)
- Logging yang sesuai

**README.md**: Metadata dan dokumentasi space
- Header YAML dengan konfigurasi HF
- Deskripsi fitur dan cara penggunaan

**Dockerfile**: Kontainer konfigurasi (opsional)
- Python 3.11 base image
- Dependency installation
- Port exposure

### 5. Struktur File yang Diperlukan
```
├── app_hf.py              # Entry point untuk HF Spaces
├── README.md              # Dokumentasi (dari README_HF.md)
├── models.py              # Database models
├── routes.py              # Flask routes
├── data_collector.py      # API data collection
├── twitter_analyzer.py    # Sentiment analysis
├── rss_generator.py       # RSS feed generation
├── scheduler.py           # Background task scheduler
├── templates/             # HTML templates
├── static/               # CSS, JS, assets
└── .gitignore           # Git ignore rules
```

### 6. Fitur yang Akan Berfungsi di HF Spaces

✅ **Yang Akan Bekerja:**
- Dashboard web dengan data real-time
- Pengumpulan data crypto dari CoinGecko API
- Pengumpulan data forex dari ExchangeRate-API
- RSS feeds untuk semua data
- Background scheduler (setiap 30 menit)
- Analisis sentimen Twitter (jika token disediakan)

⚠️ **Pertimbangan:**
- Free tier HF Spaces memiliki timeout 48 jam untuk apps yang tidak digunakan
- SQLite database akan reset jika space di-restart
- Background tasks mungkin terbatas pada free tier

### 7. URL Akses Setelah Deploy
- **Dashboard**: `https://username-crypto-forex-analysis.hf.space/`
- **RSS Crypto**: `https://username-crypto-forex-analysis.hf.space/rss/crypto`
- **RSS Forex**: `https://username-crypto-forex-analysis.hf.space/rss/forex`
- **RSS Sentiment**: `https://username-crypto-forex-analysis.hf.space/rss/sentiment`

### 8. Troubleshooting

**Jika aplikasi tidak start:**
- Cek logs di HF Spaces dashboard
- Pastikan `app_hf.py` ada di root directory
- Periksa dependencies di `pyproject.toml`

**Jika data tidak muncul:**
- Tunggu 30 menit untuk pengumpulan data pertama
- Cek API endpoints secara manual: `/api/crypto/latest`
- Periksa system logs di tab "System Logs"

**Untuk analisis Twitter:**
- Pastikan `TWITTER_BEARER_TOKEN` sudah diset di secrets
- Token harus valid dan memiliki akses ke Twitter API v2

### 9. Upgrade ke Hardware Lebih Baik
Jika diperlukan performa lebih baik:
1. Upgrade ke CPU persistent atau GPU di HF Spaces
2. Database akan persistent dan tidak reset
3. Background tasks akan lebih stabil

Dengan konfigurasi ini, aplikasi analisis crypto & forex Anda akan berjalan penuh di Hugging Face Spaces dengan fitur RSS feeds dan analisis sentimen Twitter!