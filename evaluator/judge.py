# evaluator/judge_ai.py
import asyncio
import json
from typing import List
from schemas import AgentOutput, EvaluatorOutput
import openai

class DecisionJudge:
    async def evaluate(self, agent_outputs: List[AgentOutput], input_text: str = "") -> EvaluatorOutput:
        # Prepare readable summary for GPT
        outputs_summary = [
            {
                "agent": a.__class__.__name__,
                "decision": a.decision,
                "confidence": a.confidence,
                "primary_evidence": a.primary_evidence,
                "assumptions": a.assumptions,
                "failure_modes": a.failure_modes
            }
            for a in agent_outputs
        ]

        prompt = f"""
You are an AI judge. Review the submitted input text and agent outputs, then provide a final recommendation.

Submitted Input Text:
\"\"\"{input_text}\"\"\"

Agent Outputs:
{json.dumps(outputs_summary, indent=2)}

Rules (priority order):
1. If the input is gibberish, random characters, or cannot be interpreted meaningfully, return REJECT immediately. Ignore agents’ outputs in this case.
2. If the input is positive, harmless, trivial, and agents mostly agree on ACCEPT with high confidence, return ACCEPT.
3. Escalate only if:
   - Agents disagree
   - There is a clear, high-probability risk
   - Significant uncertainty exists in the input
4. Do NOT escalate for minor or theoretical risks mentioned in the agents' failure modes.
5. Always consider both agent outputs and the content of the submitted input when making a decision.
6. If all agents agree on ACCEPT with confidence ≥0.8, and input is valid, return ACCEPT even if minor risks are mentioned.
Task:
- Determine the final decision (ACCEPT / REJECT / ESCALATE)
- Provide consensus strength (0-1)
- Flag any important risks
- Provide a textual justification

Output JSON format:
{{
  "final_decision": "ESCALATE",
  "consensus_strength": 0.5,
  "risk_summary": ["Risk description"],
  "justification": "Text explanation for your decision"
}}
"""

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        ))

        content = response.choices[0].message.content
        try:
            judge_json = json.loads(content)
        except json.JSONDecodeError:
            judge_json = {
                "final_decision": "ESCALATE",
                "consensus_strength": 0.5,
                "risk_summary": ["GPT failed to produce valid JSON, defaulting to ESCALATE"],
                "justification": content[:200]
            }

        return EvaluatorOutput(
            recommended_action=judge_json.get("final_decision", "ESCALATE"),
            consensus_strength=judge_json.get("consensus_strength", 0.5),
            decision_distribution={decision: sum(1 for a in agent_outputs if a.decision == decision)
                       for decision in set(a.decision for a in agent_outputs)},
            outlier_analysis=[a.decision for a in agent_outputs if a.decision != judge_json.get("final_decision")],
            risk_summary=judge_json.get("risk_summary", []),
            justification=judge_json.get("justification", "")
        )
