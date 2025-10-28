import logging
import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_file = os.path.join(LOG_DIR, f"api_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def log_request_response(response):
    logging.info(f"REQUEST: {response.request.method} {response.request.url}")
    logging.info(f"REQUEST BODY: {response.request.body}")
    logging.info(f"RESPONSE CODE: {response.status_code}")
    logging.info(f"RESPONSE BODY: {response.text}")
