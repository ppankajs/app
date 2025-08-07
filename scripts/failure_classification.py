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
        ["kubectl", "get", "pods", "--all-namespaces", "-o", "json"],
        capture_output=True, text=True
    )

    try:
        pods = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print("[ERROR] Failed to parse kubectl output.")
        return

    found_failure = False

    for pod in pods["items"]:
        name = pod["metadata"]["name"]
        namespace = pod["metadata"]["namespace"]
        status = pod.get("status", {})
        container_statuses = status.get("containerStatuses", [])

        for container in container_statuses:
            container_name = container.get("name", "unknown")
            state = container.get("state", {})
            last_state = container.get("lastState", {})
            restart_count = container.get("restartCount", 0)

            # Check failure conditions
            waiting = state.get("waiting", {})
            terminated = last_state.get("terminated", {})

            if (
                waiting.get("reason") == "CrashLoopBackOff" or
                terminated.get("reason") == "Error" or
                restart_count >= 3
            ):
                print(f"[FAILURE] Pod: {name} (ns: {namespace})")
                print(f"  Container: {container_name}")
                print(f"  Restart Count: {restart_count}")
                print(f"  Waiting Reason: {waiting.get('reason')}")
                print(f"  Terminated Reason: {terminated.get('reason')}")
                print("[CLASSIFICATION] Type: ApplicationFailure")
                found_failure = True

    if not found_failure:
        print("[INFO] No failures detected.")

if __name__ == "__main__":
    classify_failures()
