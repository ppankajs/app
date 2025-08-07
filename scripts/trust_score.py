import subprocess
import json
import sys

TRUSTED_TAGS = ["v78", "v77", "v76"]
TRUST_THRESHOLD = 70

def evaluate_trust():
    print("[INFO] Checking image trust score...")

    # Run kubectl
    result = subprocess.run(
        ["kubectl", "get", "deployment", "flask-app", "-o", "json"],
        capture_output=True, text=True
    )

    # Check for errors in kubectl execution
    if result.returncode != 0:
        print("[ERROR] kubectl failed to run.")
        print("[stderr]:", result.stderr.strip())
        sys.exit(1)

    if not result.stdout.strip():
        print("[ERROR] kubectl returned empty output.")
        sys.exit(1)

    try:
        deployment = json.loads(result.stdout)
        image = deployment['spec']['template']['spec']['containers'][0]['image']
        tag = image.split(":")[-1]

        trust_score = 100 if tag in TRUSTED_TAGS else 40
        print(f"[IMAGE] {image}")
        print(f"[TRUST SCORE] Result: {trust_score} (Threshold: {TRUST_THRESHOLD})")

        if trust_score < TRUST_THRESHOLD:
            print("[ALERT] Trust score too low. Deployment is unverified!")

    except json.JSONDecodeError as e:
        print("[ERROR] JSON decoding failed.")
        print("[stdout]:", result.stdout)
        print("Exception:", e)
        sys.exit(1)

    except (KeyError, IndexError) as e:
        print("[ERROR] Unexpected structure in deployment JSON.")
        print("Exception:", e)
        sys.exit(1)

if __name__ == "__main__":
    evaluate_trust()
