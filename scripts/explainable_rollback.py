import logging
import subprocess

logging.basicConfig(level=logging.INFO)

def explain_and_rollback():
    logging.warning("Initiating rollback due to failure or poor trust score...")
    try:
        # Replace this with actual rollback if needed
        # subprocess.run(["kubectl", "rollout", "undo", "deployment/flask-app"], check=True)
        logging.info("Rollback simulated successfully.")
    except Exception as e:
        logging.error(f"Rollback failed: {e}")

if __name__ == "__main__":
    explain_and_rollback()
