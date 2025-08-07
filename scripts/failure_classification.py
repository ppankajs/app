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

    pods = json.loads(result.stdout)

    for pod in pods['items']:
        name = pod['metadata']['name']
        namespace = pod['metadata']['namespace']
        phase = pod['status'].get('phase', '')
        container_statuses = pod['status'].get('containerStatuses', [])

        for status in container_statuses:
            state = status.get('state', {})
            restart_count = status.get('restartCount', 0)

            terminated = state.get('terminated')
            waiting = state.get('waiting')
            waiting_reason = waiting.get('reason') if waiting else None
            terminated_reason = terminated.get('reason') if terminated else None

            if (
                phase in ["Failed", "Unknown"] or
                terminated_reason is not None or
                (waiting_reason and waiting_reason in ["CrashLoopBackOff", "Error"]) or
                restart_count > 3  # Consider high restarts as failure
            ):
                print(f"[FAILURE] Pod: {name} (ns: {namespace})")
                print(f"  Phase: {phase}")
                print(f"  Reason: {waiting_reason or terminated_reason or 'Unknown'}")
                print(f"  Restarts: {restart_count}")
                print("[CLASSIFICATION] Type: ApplicationFailure")

if __name__ == "__main__":
    classify_failures()
