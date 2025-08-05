import requests
import logging

logging.basicConfig(level=logging.INFO)

def check_failure():
    try:
        response = requests.get("http://flask-service:5000/health", timeout=5)
        if response.status_code == 200:
            logging.info("Flask service is healthy.")
        else:
            logging.warning(f"Flask health check returned {response.status_code}.")
    except Exception as e:
        logging.error(f"Service failure detected: {e}")
        # Optionally: notify or write to a failure DB

if __name__ == "__main__":
    check_failure()
