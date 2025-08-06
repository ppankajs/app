import subprocess
import json

TRUSTED_TAGS = ["v35", "v36", "v37", "v38"]
TRUST_THRESHOLD = 70

def evaluate_trust():
    print("[INFO] Checking image trust score...")
    result = subprocess.run(
        ["kubectl", "get", "deployment", "flask-app", "-o", "json"],
        capture_output=True, text=True
    )
    deployment = json.loads(result.stdout)
    image = deployment['spec']['template']['spec']['containers'][0]['image']
    tag = image.split(":")[-1]

    trust_score = 100 if tag in TRUSTED_TAGS else 40
    print(f"[IMAGE] {image}")
    print(f"[TRUST SCORE] Result: {trust_score} (Threshold: {TRUST_THRESHOLD})")

    if trust_score < TRUST_THRESHOLD:
        print("[ALERT] Trust score too low. Deployment is unverified!")

if __name__ == "__main__":
    evaluate_trust()
