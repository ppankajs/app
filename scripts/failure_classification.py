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

def classify_failures():
    print("[INFO] Starting Failure Classification...")

    result = subprocess.run(
        ["kubectl", "get", "pods", "-A", "-o", "json"],
        capture_output=True, text=True
    )

    try:
        pods = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print("[ERROR] Failed to parse kubectl output.")
        return

    found_failure = False

    for pod in pods["items"]:
        pod_name = pod["metadata"]["name"]
        namespace = pod["metadata"]["namespace"]
        container_statuses = pod.get("status", {}).get("containerStatuses", [])

        for container in container_statuses:
            container_name = container.get("name")
            restart_count = container.get("restartCount", 0)
            state = container.get("state", {})
            waiting = state.get("waiting", {})
            reason_waiting = waiting.get("reason", "")
            last_state = container.get("lastState", {})
            terminated_reason = last_state.get("terminated", {}).get("reason", "")

            print(f"[DEBUG] Checking Pod: {pod_name}, Container: {container_name}, RestartCount: {restart_count}, WaitingReason: {reason_waiting}, TerminatedReason: {terminated_reason}")

            if reason_waiting == "CrashLoopBackOff" or terminated_reason == "Error" or restart_count >= 3:
                print(f"[FAILURE] Pod: {pod_name} (ns: {namespace})")
                print(f"  Container: {container_name}")
                print(f"  Restart Count: {restart_count}")
                print(f"  Waiting Reason: {reason_waiting}")
                print(f"  Terminated Reason: {terminated_reason}")
                print("[CLASSIFICATION] Type: ApplicationFailure")
                found_failure = True

    if not found_failure:
        print("[INFO] No failures detected.")

if __name__ == "__main__":
    classify_failures()
