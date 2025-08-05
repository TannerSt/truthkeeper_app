# examples/multi_agent_validation.py

import time
import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.predefined_sentinels import WaterSentinel, LightSpeedSentinel

# Simulate a proposal with multiple values
proposed_values = {
    "melting_point_water": 0.0,
    "speed_of_light": 299_792_458
}

# Drift factors per iteration
DRIFT_SETTINGS = {
    "melting_point_water": 0.005,
    "speed_of_light": 5  # Speed of light doesn't tolerate drift at all
}

# Setup sentinels
truthkeepers = {
    "melting_point_water": WaterSentinel,
    "speed_of_light": LightSpeedSentinel
}


def simulate_multi_agent_drift(iterations=20):
    print("\n🌐 Starting multi-agent drift validation...\n")

    for i in range(1, iterations + 1):
        print(f"🔁 Iteration {i}")

        # Apply random drift to each value
        for key, drift_limit in DRIFT_SETTINGS.items():
            drift = random.uniform(-drift_limit, drift_limit)
            proposed_values[key] += drift
            value = proposed_values[key]

            # Validate with the corresponding truthkeeper
            sentinel = truthkeepers[key]
            result = sentinel.react(value)

            print(f" - {sentinel.name} checks {key}: {value:.5f}")

            if result["status"] == "accepted":
                print(f"   ✅ Accepted by {sentinel.name}")
            else:
                print(f"   ❌ Rejected by {sentinel.name}")
                print(f"      Reason: {result['reason']}")
                print(f"      Expected: {result['expected']}, Received: {result['received']:.5f}")
                print("\n💥 Drift threshold violated. Simulation halted.\n")
                return

        print("✅ All values accepted this round.\n")
        time.sleep(0.5)

    print("\n🎉 Simulation completed successfully with no violations.\n")


if __name__ == "__main__":
    simulate_multi_agent_drift()
