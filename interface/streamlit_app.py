# interface/streamlit_app.py

import streamlit as st
import sys
import os
import io
import pandas as pd
from contextlib import redirect_stdout

# Add root directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from examples.simulate_drift import simulate_drift
from examples.multi_agent_validation import simulate_multi_agent_drift
from agents.predefined_sentinels import WaterSentinel, LightSpeedSentinel

st.set_page_config(page_title="Truthkeeper Dashboard", layout="centered")
st.title("🛡️ Truthkeeper Simulation Dashboard")

st.markdown("""
This interactive dashboard simulates recursive drift and runs validations through narrow truthkeeping agents.
Choose a mode and observe how agents react over time.
""")

# --- User Inputs ---
mode = st.radio("Select Mode:", options=["Single Agent", "Multi-Agent"])
iterations = st.slider("Number of Iterations", min_value=5, max_value=100, value=20)

if st.button("▶️ Start Simulation"):
    st.markdown("---")
    st.subheader("Simulation Output:")

    output = io.StringIO()
    drift_data = []

    if mode == "Single Agent":
        from agents.truthkeeper import TruthkeeperAgent
        import random

        current_value = 0.0
        drift_step = 0.005

        for i in range(1, iterations + 1):
            drift = random.uniform(-drift_step, drift_step)
            current_value += drift
            result = WaterSentinel.react(current_value)
            drift_data.append({"Iteration": i, "Value": current_value})

            output.write(f"Iteration {i}: {current_value:.5f}\n")
            if result["status"] == "rejected":
                output.write("Drift threshold violated. Halting.\n")
                break

    else:
        import random

        values = {
            "melting_point_water": 0.0,
            "speed_of_light": 299_792_458
        }
        drift_steps = {
            "melting_point_water": 0.005,
            "speed_of_light": 5
        }

        for i in range(1, iterations + 1):
            row = {"Iteration": i}
            for key in values:
                drift = random.uniform(-drift_steps[key], drift_steps[key])
                values[key] += drift
                row[key] = values[key]

                sentinel = WaterSentinel if key == "melting_point_water" else LightSpeedSentinel
                result = sentinel.react(values[key])

                output.write(f"{key} [{i}]: {values[key]:.5f} => {result['status']}\n")
                if result["status"] == "rejected":
                    output.write("Drift threshold violated. Halting.\n")
                    drift_data.append(row)
                    break
            drift_data.append(row)

    # Show simulation log
    st.code(output.getvalue(), language="text")

    # Visualize drift
    if drift_data:
        df = pd.DataFrame(drift_data).set_index("Iteration")
        st.line_chart(df)
