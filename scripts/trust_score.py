import subprocess
import json
import sys
import os

TRUSTED_TAGS = ["v78", "v77", "v76", "v89"]
output_file = "/data/trust_score.json"

def evaluate_trust():
    print("[INFO] Checking image trust score...")
    result = subprocess.run(
        ["kubectl", "get", "deployment", "flask-app", "-o", "json"],
        capture_output=True, text=True
    )

    try:
        deployment = json.loads(result.stdout)
        image = deployment['spec']['template']['spec']['containers'][0]['image']
        tag = image.split(":")[-1]
        trust_score = 100 if tag in TRUSTED_TAGS else 40
        print(f"[IMAGE] {image}")
        print(f"[TRUST SCORE] {trust_score}")
    except Exception as e:
        print(f"[ERROR] Failed to evaluate trust: {e}")
        trust_score = 40

    with open(output_file, "w") as f:
        json.dump({"trust": trust_score}, f)

if __name__ == "__main__":
    evaluate_trust()
