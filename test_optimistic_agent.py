import asyncio
from agents.agent_optimistic import AgentOptimistic

async def test():
    agent = AgentOptimistic()
    input_data = {
        "text": "Customer reports delayed shipment and wants a refund."
    }
    output = await agent.propose_decision(input_data)
    print(output.__dict__)

asyncio.run(test())
