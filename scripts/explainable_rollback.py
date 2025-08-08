import json
import os
import subprocess

SCORE_THRESHOLD = 70
DATA_DIR = "/data"
ROLLBACK_TO_TAG = "v95"

def read_score(file_name):
    try:
        with open(os.path.join(DATA_DIR, file_name), "r") as f:
            data = json.load(f)
            return list(data.values())[0]
    except Exception as e:
        print(f"[ERROR] Failed to read {file_name}: {e}")
        return 0

def get_latest_scores():
    scores = {
        "failure": read_score("failure_score.json"),
        "trust": read_score("trust_score.json"),
        "health": read_score("health_score.json"),
    }
    print(f"[SCORES] {scores}")
    return scores

def trigger_rollback():
    print(f"[ROLLBACK] Deployment score too low. Rolling back to {ROLLBACK_TO_TAG}")
    subprocess.run([
        "kubectl", "set", "image", "deployment/flask-app",
        f"flask-app=ppankajs/self-healing-app:{ROLLBACK_TO_TAG}"
    ])

def main():
    scores = get_latest_scores()
    avg_score = sum(scores.values()) // len(scores)
    print(f"[EVALUATION] Deployment Score: {avg_score}")

    if avg_score < SCORE_THRESHOLD:
        print("[TRIGGERED] Score unhealthy. Triggering rollback...")
        trigger_rollback()
    else:
        print("[OK] Deployment score healthy.")

if __name__ == "__main__":
    main()
