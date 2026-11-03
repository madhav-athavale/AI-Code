"""
Complete example from Claude Code: Token counting + API calls + Cost calculation
"""

from anthropic import Anthropic

# Initialize client (reads ANTHROPIC_API_KEY from environment)
client = Anthropic()

# Pricing (check https://www.anthropic.com/pricing for current rates)
PRICING = {
    "claude-opus-4-1-20250805": {
        "input": 0.80,      # $ per million input tokens
        "output": 2.40      # $ per million output tokens
    },
    "claude-haiku-4-5-20251001": {
        "input": 1.00,
        "output": 5.00
    }
}

def count_tokens_for_message(model: str, messages: list) -> int:
    """
    Count tokens for a message before sending it
    """
    response = client.beta.messages.count_tokens(
        model=model,
        messages=messages
    )
    return response.input_tokens


def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """
    Calculate cost based on token counts and pricing
    """
    pricing = PRICING.get(model, PRICING["claude-haiku-4-5-20251001"])
    
    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]
    
    return input_cost + output_cost


def chat_with_token_tracking(user_message: str, model: str = "claude-haiku-4-5-20251001"):
    """
    Complete workflow: count tokens → send message → count output → calculate cost
    """
    
    # Step 1: Prepare the message
    messages = [
        {"role": "user", "content": user_message}
    ]
    
    print(f"\n{'='*60}")
    print(f"User Message: {user_message}")
    print(f"{'='*60}\n")
    
    # Step 2: COUNT TOKENS BEFORE SENDING
    input_tokens = count_tokens_for_message(model, messages)
    print(f"📊 Input Tokens: {input_tokens:,}")
    print(f"📝 Characters: {len(user_message):,}")
    print(f"📐 Char/Token Ratio: {len(user_message) / input_tokens:.2f}\n")
    
    # Step 3: SEND THE MESSAGE
    print("⏳ Waiting for response...\n")
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=messages
    )
    
    # Step 4: EXTRACT OUTPUT TOKENS
    output_tokens = response.usage.output_tokens
    assistant_message = response.content[0].text
    
    print(f"Claude's Response: {assistant_message}\n")
    
    # Step 5: CALCULATE COST
    input_cost = (input_tokens / 1_000_000) * PRICING[model]["input"]
    output_cost = (output_tokens / 1_000_000) * PRICING[model]["output"]
    total_cost = input_cost + output_cost
    
    # Step 6: DISPLAY COST BREAKDOWN
    print(f"{'='*60}")
    print(f"💰 COST BREAKDOWN")
    print(f"{'='*60}")
    print(f"Input Tokens:  {input_tokens:>10,} × ${PRICING[model]['input']:.2f}/M = ${input_cost:.6f}")
    print(f"Output Tokens: {output_tokens:>10,} × ${PRICING[model]['output']:.2f}/M = ${output_cost:.6f}")
    print(f"{'-'*60}")
    print(f"Total Cost:    {input_tokens + output_tokens:>10,} tokens          ${total_cost:.6f}")
    print(f"{'='*60}\n")
    
    return {
        "response": assistant_message,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "cost": total_cost
    }


def batch_chat_with_tracking(messages: list, model: str = "claude-haiku-4-5-20251001"):
    """
    Track multiple messages and show cumulative cost
    """
    total_input = 0
    total_output = 0
    total_cost = 0
    
    print(f"\n{'='*60}")
    print(f"BATCH MODE: Processing {len(messages)} messages")
    print(f"{'='*60}\n")
    
    for i, message in enumerate(messages, 1):
        result = chat_with_token_tracking(message, model)
        total_input += result["input_tokens"]
        total_output += result["output_tokens"]
        total_cost += result["cost"]
        
        print(f"Message {i}/{len(messages)} complete ✓\n")
    
    # Final summary
    print(f"{'='*60}")
    print(f"📊 BATCH SUMMARY")
    print(f"{'='*60}")
    print(f"Total Input Tokens:  {total_input:>10,}")
    print(f"Total Output Tokens: {total_output:>10,}")
    print(f"Total Tokens:        {total_input + total_output:>10,}")
    print(f"Total Cost:          ${total_cost:>15.6f}")
    print(f"{'='*60}\n")
    
    return {
        "total_input": total_input,
        "total_output": total_output,
        "total_tokens": total_input + total_output,
        "total_cost": total_cost
    }


# ============================================================================
# EXAMPLES
# ============================================================================

if __name__ == "__main__":
    
    # Example 1: Single message with full tracking
    print("\n🔵 EXAMPLE 1: Single Message")
    result = chat_with_token_tracking(
        "What is the capital of France?",
        model="claude-haiku-4-5-20251001"
    )
    
    # Example 2: Longer message
    print("\n🔵 EXAMPLE 2: Longer Message")
    result = chat_with_token_tracking(
        "Explain quantum computing in simple terms, including its applications and challenges.",
        model="claude-haiku-4-5-20251001"
    )
    
    # Example 3: Batch processing
    print("\n🔵 EXAMPLE 3: Batch Processing")
    questions = [
        "What is Python?",
        "How do loops work?",
        "What is a function?"
    ]
    summary = batch_chat_with_tracking(questions, model="claude-haiku-4-5-20251001")
    
    # Example 4: Just count tokens WITHOUT calling API (for estimation)
    print("\n🔵 EXAMPLE 4: Count Tokens Only (No API Call)")
    estimation_message = [
        {"role": "user", "content": "Write a 500-word essay about machine learning"}
    ]
    tokens = count_tokens_for_message("claude-haiku-4-5-20251001", estimation_message)
    estimated_cost = calculate_cost("claude-haiku-4-5-20251001", tokens, 2000)  # Estimate 2000 output tokens
    print(f"Request tokens: {tokens:,}")
    print(f"Estimated output: ~2,000 tokens")
    print(f"Estimated cost: ${estimated_cost:.6f}\n")