import subprocess
import json

SCORE_THRESHOLD = 70
ROLLBACK_TO_TAG = "v35"

def get_latest_scores():
    # Normally fetch real output from logs or monitoring systems
    return {
        "failure": 30,
        "trust": 40,
        "health": 60
    }

def trigger_rollback():
    print(f"[ROLLBACK] Deployment score is too low. Initiating rollback to {ROLLBACK_TO_TAG}...")
    patch_cmd = [
        "kubectl", "set", "image", "deployment/flask-app",
        f"flask-app=ppankajs/self-healing-app:{ROLLBACK_TO_TAG}"
    ]
    subprocess.run(patch_cmd)

def main():
    scores = get_latest_scores()
    avg_score = sum(scores.values()) // len(scores)
    print(f"[EVALUATION] Deployment Score: {avg_score}")

    if avg_score < SCORE_THRESHOLD:
        print("[TRIGGERED] Deployment is unhealthy. Rollback required.")
        trigger_rollback()
    else:
        print("[OK] Deployment score is healthy.")

if __name__ == "__main__":
    main()
