# Hugging Face Spaces version of the application
import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.INFO)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "hf-crypto-forex-analysis-secret")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database - use SQLite for HF Spaces
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///crypto_forex_hf.db"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import models to ensure tables are created
    import models
    db.create_all()

# Import routes
import routes

if __name__ == "__main__":
    from scheduler import start_scheduler
    import threading
    
    # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()
    logging.info("Scheduler started in background thread")
    
    # Start the Flask app
    app.run(host="0.0.0.0", port=7860, debug=False)  # HF Spaces uses port 7860