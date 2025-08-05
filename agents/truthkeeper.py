# agents/truthkeeper.py

from typing import Any, Dict


class TruthkeeperAgent:
    """
    An agent that maintains a single, immutable assertion (a 'truth') and validates incoming data against it.
    """

    def __init__(self, name: str, truth: Any, tolerance: float = 0.0):
        """
        Args:
            name (str): Unique identifier for the agent.
            truth (Any): The canonical value this agent is responsible for protecting.
            tolerance (float, optional): Allowed deviation for numeric comparisons. Default is 0 (exact match).
        """
        self.name = name
        self.truth = truth
        self.tolerance = tolerance

    def validate(self, input_value: Any) -> bool:
        """
        Compares the input against the agent’s truth using equality or a tolerance margin.

        Returns:
            bool: True if the input matches the truth within tolerance, else False.
        """
        if isinstance(self.truth, (int, float)) and isinstance(input_value, (int, float)):
            return abs(input_value - self.truth) <= self.tolerance

        return input_value == self.truth

    def react(self, input_value: Any) -> Dict[str, Any]:
        """
        Evaluates the input and returns a structured result indicating acceptance or rejection.

        Returns:
            dict: {status, agent, reason, expected, received}
        """
        if not self.validate(input_value):
            return {
                "status": "rejected",
                "agent": self.name,
                "reason": "Truth violation",
                "expected": self.truth,
                "received": input_value
            }

        return {
            "status": "accepted",
            "agent": self.name
        }
