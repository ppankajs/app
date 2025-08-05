import requests
import logging

logging.basicConfig(level=logging.INFO)

def perform_health_scoring():
    try:
        r = requests.get("http://flask-service:5000/health", timeout=5)
        if r.status_code == 200:
            logging.info("Health score: 100")
        else:
            logging.warning("Health score: 20")
    except Exception as e:
        logging.error(f" Health score: 0 – Unreachable ({e})")

if __name__ == "__main__":
    perform_health_scoring()
