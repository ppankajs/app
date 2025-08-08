import subprocess
import json
import os

SCORE_THRESHOLD = 70
ROLLBACK_TO_TAG = "v93"
DATA_DIR = "/data"

def load_score(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        print(f"[WARNING] Score file {filename} not found.")
        return 0
    try:
        with open(path, 'r') as f:
            data = json.load(f)
            return data.get("score", 0)
    except Exception as e:
        print(f"[ERROR] Failed to load {filename}: {e}")
        return 0

def trigger_rollback():
    print(f"[ROLLBACK] Deployment score is too low. Initiating rollback to {ROLLBACK_TO_TAG}...")
    patch_cmd = [
        "kubectl", "set", "image", "deployment/flask-app",
        f"flask-app=ppankajs/self-healing-app:{ROLLBACK_TO_TAG}"
    ]
    subprocess.run(patch_cmd)

def main():
    failure = load_score("failure_score.json")
    trust = load_score("trust_score.json")
    health = load_score("health_score.json")

    print(f"[SCORES] failure={failure}, trust={trust}, health={health}")
    scores = [failure, trust, health]
    avg_score = sum(scores) // len(scores)

    print(f"[EVALUATION] Deployment Score: {avg_score}")

    if avg_score < SCORE_THRESHOLD:
        print("[TRIGGERED] Deployment is unhealthy. Rollback required.")
        trigger_rollback()
    else:
        print("[OK] Deployment score is healthy.")

if __name__ == "__main__":
    main()
