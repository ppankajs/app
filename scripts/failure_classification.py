import subprocess
import json
import time

def classify_failures():
    print("[INFO] Starting Failure Classification...")
    result = subprocess.run(
        ["kubectl", "get", "pods", "-o", "json"],
        capture_output=True, text=True
    )
    pods = json.loads(result.stdout)

    for pod in pods['items']:
        name = pod['metadata']['name']
        phase = pod['status'].get('phase', '')
        state = pod['status'].get('containerStatuses', [{}])[0].get('state', {})

        # if phase == "Failed" or "terminated" in state:
        # if phase in ["Failed", "Unknown"] or "terminated" in state or "waiting" in state:
        #     reason = state.get('terminated', {}).get('reason', 'Unknown')
        #     print(f"[FAILURE] Pod: {name}, Reason: {reason}")
        #     print("[CLASSIFICATION] Type: ApplicationFailure")
        if (
            phase in ["Failed", "Unknown"]
            or "terminated" in state
            or "waiting" in state
            or pod['status'].get('containerStatuses', [{}])[0].get('restartCount', 0) > 0
        ):
            reason = state.get('terminated', {}).get('reason') or \
                     state.get('waiting', {}).get('reason') or \
                     "Unknown"
            print(f"[FAILURE] Pod: {name}, Phase: {phase}, Reason: {reason}")
            print("[CLASSIFICATION] Type: ApplicationFailure")

if __name__ == "__main__":
    classify_failures()
