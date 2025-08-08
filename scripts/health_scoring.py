import random
import json
import os

output_file = "/data/health_score.json"

def get_mock_metrics():
    cpu = random.randint(20, 95)
    memory = random.randint(30, 95)
    return cpu, memory

def calculate_health_score(cpu, memory):
    return 100 - ((cpu + memory) // 2)

if __name__ == "__main__":
    print("[INFO] Evaluating resource health score...")
    cpu, mem = get_mock_metrics()
    score = calculate_health_score(cpu, mem)
    print(f"[HEALTH SCORE] {score}/100")
    with open(output_file, "w") as f:
        json.dump({"health": score}, f)
