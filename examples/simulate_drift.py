# examples/simulate_drift.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.truthkeeper import TruthkeeperAgent
import time
import random

# Create a single truthkeeper agent for demonstration
water_sentinel = TruthkeeperAgent(
    name="WaterSentinel-01",
    truth=0.0,
    tolerance=0.01
)

def simulate_drift(start=0.0, drift_step=0.005, iterations=20):
    current_value = start

    print("\n🔁 Starting recursive drift simulation...\n")

    for i in range(1, iterations + 1):
        # Simulate small random drift
        drift = random.uniform(-drift_step, drift_step)
        current_value += drift

        print(f"🧪 Iteration {i}: Proposed value = {current_value:.5f}")

        result = water_sentinel.react(current_value)

        if result["status"] == "rejected":
            print(f"❌ Rejected by {result['agent']}:")
            print(f"   Reason: {result['reason']}")
            print(f"   Expected: {result['expected']}, Received: {result['received']:.5f}")
            print("\n💥 Drift exceeded tolerance. Simulation halted.\n")
            break
        else:
            print(f"✅ Accepted by {result['agent']}\n")

        time.sleep(0.5)

    else:
        print("✅ Simulation completed without triggering a violation.\n")


if __name__ == "__main__":
    simulate_drift()
