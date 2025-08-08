import subprocess
import json
import os

output_file = "/data/failure_score.json"

def classify_crashloopbackoff():
    print("[INFO] Starting Failure Classification...")
    result = subprocess.run(
        ["kubectl", "get", "pods", "-A", "-o", "json"],
        capture_output=True, text=True
    )

    found_crash = False
    try:
        pods = json.loads(result.stdout)
        for pod in pods["items"]:
            statuses = pod.get("status", {}).get("containerStatuses", [])
            for container in statuses:
                waiting = container.get("state", {}).get("waiting", {})
                if waiting.get("reason") == "CrashLoopBackOff":
                    print(f"[FAILURE] CrashLoopBackOff in {pod['metadata']['name']}")
                    found_crash = True
    except json.JSONDecodeError:
        print("[ERROR] Failed to parse kubectl output.")

    score = 30 if found_crash else 100
    print(f"[FAILURE SCORE] {score}")
    with open(output_file, "w") as f:
        json.dump({"failure": score}, f)

if __name__ == "__main__":
    classify_crashloopbackoff()
