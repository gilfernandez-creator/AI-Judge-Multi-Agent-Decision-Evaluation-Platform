# AI Judge

AI Judge is a Python-based system that simulates a multi-agent decision-making pipeline. Agents analyze input scenarios, propose decisions, and a Judge AI evaluates outputs to provide a final recommendation. A Gradio interface allows easy, interactive testing.

---

## Features

- **Dynamic Agent Selection:** Orchestrator chooses which AI agents to run based on input complexity.  
- **Agent Outputs:** Each agent produces decisions with confidence, evidence, assumptions, and potential failure modes.  
- **Judge Evaluation:** Considers agent outputs and the original input text to produce a final decision: ACCEPT, REJECT, or ESCALATE.  
- **Interactive Demo:** Test your scenarios via a Gradio web interface.

---

## System Architecture

```mermaid
flowchart TD
    subgraph User
        Input["User Input / Ticket"]
    end

    subgraph Interface
        Gradio["Gradio Web Interface"]
    end

    subgraph CoreLogic
        Orchestrator["OrchestratorAI\n(selects agents based on input)"]
        AgentConservative["AgentConservative\n(proposes decisions)"]
        AgentOptimistic["AgentOptimistic\n(proposes decisions)"]
        Evaluator["Evaluator\n(aggregates agent outputs)"]
        Judge["DecisionJudge\n(analyzes agent outputs + input)"]
        Controller["Controller\n(final decision logic)"]
    end

    subgraph Output
        FinalDecision["Final Decision / Recommendation"]
    end

    Input --> Gradio
    Gradio --> Orchestrator
    Orchestrator --> AgentConservative
    Orchestrator --> AgentOptimistic
    AgentConservative --> Evaluator
    AgentOptimistic --> Evaluator
    Evaluator --> Judge
    Input --> Judge
    Judge --> Controller
    Controller --> FinalDecision
    FinalDecision --> Gradio
```markdown
Installation

Clone the repository:

git clone <your-repo-url>
cd "AI Judge"


Create a virtual environment:

python -m venv venv


Activate the environment:

Windows:

venv\Scripts\activate


Mac/Linux:

source venv/bin/activate


Install dependencies:

pip install -r requirements.txt

Usage
Run the pipeline from command line
python main.py


This will process a sample scenario and output detailed agent reasoning, judge justification, and the final decision.

Launch the Gradio demo
python demo_gradio.py


Open your browser to the local URL provided (default: http://127.0.0.1:7860).

Paste any scenario into the text box to see agent outputs, Judge reasoning, and the final decision.

Folder Structure
AI Judge/
├── agents/               # Agent implementations
├── orchestrator/         # Orchestrator code
├── evaluator/            # Evaluator and Judge code
├── controller/           # Controller logic
├── main.py               # Main async pipeline runner
├── demo_gradio.py        # Gradio demo interface
├── schemas.py            # Pydantic schemas for outputs
├── requirements.txt      # Dependencies
├── .gitignore            # Ignored files

Contributing

Use venv for dependencies.

Follow Python naming conventions.

Push only relevant code; virtual environments, secrets, and caches are ignored via .gitignore.

Notes

The Judge AI evaluates both the agent outputs and the user-submitted input before deciding.

Escalation is used for cases with uncertainty, risk, or conflicting agent outputs.

Accept/Reject is applied when agents largely agree and the input is meaningful.