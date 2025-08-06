import random

def get_mock_metrics():
    # Replace with actual Prometheus API queries in production
    cpu = random.randint(20, 95)
    memory = random.randint(30, 95)
    return cpu, memory

def calculate_health_score(cpu, memory):
    score = 100 - ((cpu + memory) // 2)
    return score

if __name__ == "__main__":
    print("[INFO] Evaluating resource health score...")
    cpu, mem = get_mock_metrics()
    print(f"[METRICS] CPU: {cpu}%, Memory: {mem}%")

    score = calculate_health_score(cpu, mem)
    print(f"[HEALTH SCORE] Result: {score}/100")

    if score < 70:
        print("[WARNING] Health score below acceptable level!")
