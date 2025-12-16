from pydantic import BaseModel
from typing import List

class AgentOutput(BaseModel):
    decision: str  # ACCEPT | REJECT | ESCALATE
    confidence: float
    primary_evidence: List[str]
    assumptions: List[str]
    failure_modes: List[str]

class EvaluatorOutput(BaseModel):
    consensus_strength: float
    decision_distribution: dict
    outlier_analysis: List[str]
    risk_summary: List[str]
    recommended_action: str
    justification: str = ""
