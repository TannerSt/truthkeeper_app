# main.py

import sys
import os
import argparse

# Ensure local modules are importable
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from examples.simulate_drift import simulate_drift
from examples.multi_agent_validation import simulate_multi_agent_drift

def main():
    parser = argparse.ArgumentParser(description="Run Truthkeeper simulations")
    parser.add_argument(
        "--mode",
        choices=["single", "multi"],
        default="single",
        help="Which simulation to run: 'single' for one truthkeeper, 'multi' for multi-agent"
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=20,
        help="Number of iterations to simulate"
    )

    args = parser.parse_args()

    if args.mode == "single":
        simulate_drift(iterations=args.iterations)
    elif args.mode == "multi":
        simulate_multi_agent_drift(iterations=args.iterations)
    else:
        print("❌ Invalid mode selected.")


if __name__ == "__main__":
    main()
