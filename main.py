import asyncio
import time
from orchestrator.orchestrator import OrchestratorAI
from evaluator.evaluator import Evaluator
from controller.controller import Controller
from evaluator.judge import DecisionJudge

async def run_pipeline_async(input_data):
    output_log = []

    # Helper function to capture logs
    def log(*args):
        text = " ".join(str(a) for a in args)
        output_log.append(text)
        print(text)  # still print to console

    orchestrator = OrchestratorAI()
    agents = await orchestrator.choose_agents(input_data)
    log(f"Orchestrator selected agents: {[a.name for a in agents]}")

    async def run_agent(agent):
        start = time.time()
        log(f"[{start:.2f}] {agent.name} starting")
        output = await agent.propose_decision(input_data)
        end = time.time()
        log(f"[{end:.2f}] {agent.name} finished (duration: {end-start:.2f}s)")
        return output

    # Run all agents concurrently
    agent_tasks = [run_agent(agent) for agent in agents]
    outputs = await asyncio.gather(*agent_tasks)

    # Capture each agent's output
    for agent, output in zip(agents, outputs):
        log(f"\nAgent: {agent.name}")
        log(output)

    # Evaluate outputs
    evaluator = Evaluator()
    eval_output = evaluator.evaluate(outputs)

    # Evaluate with Judge
    judge = DecisionJudge()
    eval_output = await judge.evaluate(outputs, input_text=input_data["text"])
    log("\nJudge Output:")
    log("\nJudge Justification:")
    log(eval_output.justification)
    log(eval_output)

    # Controller final decision
    controller = Controller()
    final_decision = controller.decide(eval_output, outputs)
    log("\nFinal Pipeline Output:")
    log(final_decision)

    # Return everything as one string for Gradio
    return "\n".join(output_log)

if __name__ == "__main__":
    sample_input = {
        "text": "A long-time client discovered that we accidentally overcharged them $200,000 over the past year. They are demanding an immediate full refund. Our finance team warns that paying immediately will severely strain cash flow, possibly impacting payroll for other clients. Legal advises that delaying repayment could trigger a lawsuit. The client hints that if we don’t comply quickly, they might switch all future business to a competitor. Meanwhile, the client has been generally positive in past interactions and has left glowing reviews for our services."
    }
    start_pipeline = time.time()
    result = asyncio.run(run_pipeline_async(sample_input))
    end_pipeline = time.time()

    print(result)
    print(f"Total pipeline wall-clock time: {end_pipeline - start_pipeline:.2f}s")
