# import subprocess
# import json
# import time

# def classify_failures():
#     print("[INFO] Starting Failure Classification...")
#     result = subprocess.run(
#         ["kubectl", "get", "pods", "-o", "json"],
#         capture_output=True, text=True
#     )
#     pods = json.loads(result.stdout)

#     for pod in pods['items']:
#         name = pod['metadata']['name']
#         phase = pod['status'].get('phase', '')
#         state = pod['status'].get('containerStatuses', [{}])[0].get('state', {})

#         # if phase == "Failed" or "terminated" in state:
#         # if phase in ["Failed", "Unknown"] or "terminated" in state or "waiting" in state:
#         #     reason = state.get('terminated', {}).get('reason', 'Unknown')
#         #     print(f"[FAILURE] Pod: {name}, Reason: {reason}")
#         #     print("[CLASSIFICATION] Type: ApplicationFailure")
#         if (
#             phase in ["Failed", "Unknown"]
#             or "terminated" in state
#             or "waiting" in state
#             or pod['status'].get('containerStatuses', [{}])[0].get('restartCount', 0) > 0
#         ):
#             reason = state.get('terminated', {}).get('reason') or \
#                      state.get('waiting', {}).get('reason') or \
#                      "Unknown"
#             print(f"[FAILURE] Pod: {name}, Phase: {phase}, Reason: {reason}")
#             print("[CLASSIFICATION] Type: ApplicationFailure")

# if __name__ == "__main__":
#     classify_failures()


import subprocess
import json

def classify_crashloopbackoff():
    print("[INFO] Starting Failure Classification...")

    result = subprocess.run(
        ["kubectl", "get", "pods", "-A", "-o", "json"],
        capture_output=True, text=True
    )

    try:
        pods = json.loads(result.stdout)
    except json.JSONDecodeError:
        print("[ERROR] Failed to parse kubectl output.")
        return

    found_crash = False

    for pod in pods["items"]:
        pod_name = pod["metadata"]["name"]
        namespace = pod["metadata"]["namespace"]
        container_statuses = pod.get("status", {}).get("containerStatuses", [])

        for container in container_statuses:
            container_name = container.get("name")
            state = container.get("state", {})
            waiting_reason = state.get("waiting", {}).get("reason", "")

            if waiting_reason == "CrashLoopBackOff":
                print(f"[FAILURE] Pod: {pod_name} (ns: {namespace})")
                print(f"  Container: {container_name}")
                print(f"  Waiting Reason: {waiting_reason}")
                print("[CLASSIFICATION] Type: CrashLoopBackOff")
                found_crash = True

    if not found_crash:
        print("[INFO] No CrashLoopBackOff detected.")

if __name__ == "__main__":
    classify_crashloopbackoff()
