# test_agent.py
import asyncio
from agents.agent_conservative import AgentConservative

async def test():
    agent = AgentConservative()
    input_data = {"text": "Customer reports delayed shipment and wants a refund."}
    output = await agent.propose_decision(input_data)
    print(output.__dict__)  # shows decision, confidence, evidence, etc.

asyncio.run(test())
