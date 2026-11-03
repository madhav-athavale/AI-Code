import os
from strands import Agent, tool
from strands.models import BedrockModel
from strands_tools import retrieve
import json
import requests

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
def get_weather(location):
    api_key = "b5cd2f38a8c37fc39dfc85ce74c1af5c"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
    response = requests.get(url)
    weather_data = response.json()
    print(weather_data)
    print(f"Weather in {location}: {weather_data['weather'][0]['description']}")
    print(weather_data['coord']['lat'], weather_data['coord']['lon'])       
    print(weather_data['main']['temp'])
    return weather_data

# ============================================================
# Build the Agent
# ============================================================

def create_new_agent(): 
    
    """Create new  chatbot agent."""

    # The built-in retrieve tool reads this env var to find the KB
    
    bedrock_model = BedrockModel(
        model_id=MODEL_ID,
        region_name=REGION,
        temperature=0.3,
        max_tokens=2000,
        guardrail_id=GUARDRAIL_ID,
        guardrail_version=GUARDRAIL_VERSION
    )

    system_prompt = """You are a new agent Answer questions about weather
    

Your responsibilities:
- Answer questions about weather
Guidelines:
- Be friendly and welcoming

- Keep answers concise and helpful."""

    agent = Agent(
        model=bedrock_model,
        tools=[get_weather],
        system_prompt=system_prompt,
    )

    return agent


# ============================================================
# Run the Agent
# ============================================================

def main():
    print("New chatbot.")
    print("=" * 60)
    print("Ask me about weather")
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
