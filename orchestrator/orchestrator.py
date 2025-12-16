# orchestrator/orchestrator_ai.py
import asyncio
import json
from typing import Dict, List
from agents.agent_conservative import AgentConservative
from agents.agent_optimistic import AgentOptimistic
import openai

class OrchestratorAI:
    MAX_AGENTS = 3  # Guardrail

    async def choose_agents(self, input_data: Dict) -> List:
        text = input_data.get("text", "")
        prompt = f"""
        You are an AI orchestrator.
        Input: {text}

        Task: Recommend which agents should handle this input. 
        Rules:
        - If the input is low-risk, straightforward, positive feedback, or minor requests that don't require legal or financial risk analysis, select only the 'Optimistic' agent.
        - If the input is high-risk, urgent, involves legal/financial implications, or could lead to significant negative consequences, include the 'Conservative' agent.
        - You may choose one or both agents, but only select agents that are necessary based on the input.

        Options: ['Conservative', 'Optimistic'].
        Output JSON: {{ "agents": ["Conservative", "Optimistic"] }}.
        Max number of agents: {self.MAX_AGENTS}.
        """

        # Run GPT asynchronously
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        ))

        content = response.choices[0].message.content
        print(f"[Orchestrator GPT Output] {content}")  # log raw GPT output

        try:
            output_json = json.loads(content)
            agent_names = output_json.get("agents", [])
        except Exception:
            agent_names = ["Conservative"]

        agent_map = {
            "Conservative": AgentConservative,
            "Optimistic": AgentOptimistic
        }

        agents = [agent_map[name]() for name in agent_names if name in agent_map]
        print(f"[Orchestrator Instantiated Agents] {[a.name for a in agents]}")  # log final agents

        return agents[:self.MAX_AGENTS]
