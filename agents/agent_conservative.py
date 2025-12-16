import asyncio
from typing import Dict
from schemas import AgentOutput
import openai
import json

class AgentConservative:
    name = "AgentConservative"

    async def propose_decision(self, input_data: Dict) -> AgentOutput:
        text = input_data.get("text", "")

        prompt = f"""
        You are a conservative AI evaluator.
        Input: {text}

        Task: Decide whether to ACCEPT, REJECT, or ESCALATE. Provide confidence (0-1), reasoning, assumptions, and possible failure modes.
        Output as JSON with keys: decision, confidence, primary_evidence, assumptions, failure_modes.
        """

        # Run GPT asynchronously in a thread to not block event loop
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        ))

        content = response.choices[0].message.content
        try:
            output_json = json.loads(content)
        except json.JSONDecodeError:
            # fallback if GPT outputs text not JSON
            output_json = {
                "decision": "REJECT",
                "confidence": 0.5,
                "primary_evidence": [content[:50]],
                "assumptions": [],
                "failure_modes": ["GPT output not JSON"]
            }

        return AgentOutput(
    decision=output_json.get("decision", "REJECT"),
    confidence=output_json.get("confidence", 0.8),
    primary_evidence=(
        output_json.get("primary_evidence")
        if isinstance(output_json.get("primary_evidence"), list)
        else [output_json.get("primary_evidence", "No evidence provided")]
    ),
    assumptions=(
        output_json.get("assumptions")
        if isinstance(output_json.get("assumptions"), list)
        else [output_json.get("assumptions", "No assumptions stated")]
    ),
    failure_modes=(
        output_json.get("failure_modes")
        if isinstance(output_json.get("failure_modes"), list)
        else [output_json.get("failure_modes", "No failure modes identified")]
    )
)
