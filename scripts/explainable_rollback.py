import json
import os
import subprocess

SCORE_THRESHOLD = 70
ROLLBACK_TO_TAG = "v89"

def get_score(filepath, key):
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            return data.get(key, 0)
    except Exception as e:
        print(f"[WARN] Could not read {key}: {e}")
        return 0

def get_latest_scores():
    return {
        "failure": get_score("/data/failure_score.json", "failure"),
        "trust": get_score("/data/trust_score.json", "trust"),
        "health": get_score("/data/health_score.json", "health")
    }

def trigger_rollback():
    print(f"[ROLLBACK] Score too low. Rolling back to {ROLLBACK_TO_TAG}...")
    subprocess.run([
        "kubectl", "set", "image", "deployment/flask-app",
        f"flask-app=ppankajs/self-healing-app:{ROLLBACK_TO_TAG}"
    ])

def main():
    scores = get_latest_scores()
    print(f"[SCORES] {scores}")
    avg_score = sum(scores.values()) // len(scores)
    print(f"[EVALUATION] Average Score: {avg_score}")

    if avg_score < SCORE_THRESHOLD:
        print("[ACTION] Triggering rollback...")
        trigger_rollback()
    else:
        print("[OK] Deployment score is healthy.")

if __name__ == "__main__":
    main()
