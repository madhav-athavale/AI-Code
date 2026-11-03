from anthropic import Anthropic

# Initialize client with your Anthropic API key
#API key has been removed. needs to be added back
client = Anthropic()

# Or use environment variable (recommended)
# export ANTHROPIC_API_KEY="sk-ant-your-api-key-here"
# client = Anthropic()

# Actual message content
messages = [
    {"role": "user", "content": "Hello, how are you?"}
]

# Call the API directly - no JSON serialization needed!
response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=messages
)

print(response.content[0].text)