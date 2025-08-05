# agents/predefined_sentinels.py

from .truthkeeper import TruthkeeperAgent

# Physical constant: Melting point of water at 1 atm (°C)
WaterSentinel = TruthkeeperAgent(
    name="WaterSentinel-01",
    truth=0.0,
    tolerance=0.01
)

# Physical constant: Speed of light in vacuum (m/s)
LightSpeedSentinel = TruthkeeperAgent(
    name="LightSpeedSentinel-01",
    truth=299_792_458,  # meters per second
    tolerance=0  # No drift tolerated
)
