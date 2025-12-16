# controller/controller.py

from typing import List
from schemas import EvaluatorOutput, AgentOutput

# controller/controller.py

class Controller:
    def decide(self, eval_output, agent_outputs):
        """
        Decide the final action based primarily on the Judge's recommendation.
        - If the judge gives a valid recommended_action, return it.
        - If somehow judge output is missing or invalid, default to ESCALATE.
        """
        if eval_output and hasattr(eval_output, "recommended_action"):
            return eval_output.recommended_action
        
        # Safety fallback
        return "ESCALATE"
