import logging
import random

logging.basicConfig(level=logging.INFO)

def calculate_trust_score():
    # Simulate trust score between 0 and 1
    score = round(random.uniform(0, 1), 2)
    if score < 0.5:
        logging.warning(f" Low trust score: {score}")
    else:
        logging.info(f"Trust score is acceptable: {score}")

if __name__ == "__main__":
    calculate_trust_score()
