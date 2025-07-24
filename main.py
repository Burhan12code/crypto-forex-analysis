from app import app
from scheduler import start_scheduler
import threading
import logging

if __name__ == "__main__":
    # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()
    logging.info("Scheduler started in background thread")
    
    # Start the Flask app
    app.run(host="0.0.0.0", port=5000, debug=True)
