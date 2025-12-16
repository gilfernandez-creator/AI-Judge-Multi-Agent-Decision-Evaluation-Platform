from typing import List, Dict
from schemas import EvaluatorOutput, AgentOutput

class Evaluator:
    """
    Evaluates agent outputs, computes consensus, flags minority risks.
    """

    def evaluate(self, agent_outputs: List[AgentOutput]) -> EvaluatorOutput:
        decision_count: Dict[str, int] = {"ACCEPT": 0, "REJECT": 0, "ESCALATE": 0}
        for ao in agent_outputs:
            decision_count[ao.decision] += 1

        total_agents = len(agent_outputs)
        consensus_strength = max(decision_count.values()) / total_agents

        outliers = [ao.decision for ao in agent_outputs if ao.decision != max(decision_count, key=decision_count.get)]

        # Mock risk summary
        risk_summary = []
        for ao in agent_outputs:
            if ao.decision == "ESCALATE" or ao.confidence < 0.7:
                risk_summary.append(f"Agent {ao.decision} flagged risk")

        return EvaluatorOutput(
            consensus_strength=consensus_strength,
            decision_distribution=decision_count,
            outlier_analysis=outliers,
            risk_summary=risk_summary,
            recommended_action="commit" if consensus_strength >= 0.7 else "escalate"
        )
