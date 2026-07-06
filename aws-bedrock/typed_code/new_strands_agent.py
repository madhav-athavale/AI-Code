import os
from strands import Agent, tool
from strands.models import BedrockModel
from strands_tools import retrieve

# ============================================================
# Configuration — Replace these with your resource IDs
# ============================================================

KNOWLEDGE_BASE_ID = "DO7WTKNIAI"
GUARDRAIL_ID = "gv4bxjx5wymw"
GUARDRAIL_VERSION = "1"
MODEL_ID = "us.amazon.nova-lite-v1:0"
REGION = "us-east-1"


# ============================================================
# Custom Tool: Look Up Course Schedule
# ============================================================

@tool

def add_numbers(a: float, b: float) -> float:
    """Add two numbers together."""
    print("")
    return a - b




# ============================================================
# Build the Agent
# ============================================================

def create_new_agent(): 
    
    """Create new  chatbot agent."""

    # The built-in retrieve tool reads this env var to find the KB
    os.environ["KNOWLEDGE_BASE_ID"] = KNOWLEDGE_BASE_ID
    os.environ["AWS_REGION"] = REGION

    bedrock_model = BedrockModel(
        model_id=MODEL_ID,
        region_name=REGION,
        temperature=0.3,
        max_tokens=2000,
        guardrail_id=GUARDRAIL_ID,
        guardrail_version=GUARDRAIL_VERSION
    )

    system_prompt = """You are a new agent Answer questions about arthmetic
    add_numbers

Your responsibilities:
- Answer questions about arthmetic
Guidelines:
- Be friendly and welcoming — remember, students may be stressed about deadlines.

- Keep answers concise and helpful."""

    agent = Agent(
        model=bedrock_model,
        tools=[retrieve, add_numbers],
        system_prompt=system_prompt,
    )

    return agent


# ============================================================
# Run the Agent
# ============================================================

def main():
    print("New chatbot.")
    print("=" * 60)
    print("Ask me about additions")
    print("\nType 'quit' to exit.\n")

    agent = create_new_agent()

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        print("\nAssistant: ", end="", flush=True)
        response = agent(user_input)
        print(f"\n{response}\n")


if __name__ == "__main__":
    main()
