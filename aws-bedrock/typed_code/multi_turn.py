import boto3

def multi_turn_conversation():
    bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
    model_id = "us.amazon.nova-lite-v1:0"

    system_prompt = [
        {"text": "You are a helpful cooking assistant. Please provide concise recipe suggestion."}    ]

    conversation_history = [ ]
    user_message_1 = "I have chicken and broccoli. What can I make for dinner?"
    conversation_history.append({
        "role": "user",
        "content": [{"text": user_message_1}]
    })

    try:
        response_1 = bedrock_runtime.converse(
            modelId=model_id,
            system=system_prompt,
            messages=conversation_history,
            inferenceConfig={
                "temperature": 0.7,
                "maxTokens": 2000
            }
        )

        assistant_reply_1 = response_1['output']['message']['content'][0]['text']
        print("Assistant Response to User Message 1:")
        print(assistant_reply_1)

        print ("=" * 60)
        usage = response_1.get('usage', {})
        print(f"Token Usage for User Message 1:")
        print(f"  Input tokens: {usage.get('inputTokens', 'N/A')}")
        print(f"  Output tokens: {usage.get('outputTokens', 'N/A')}")
        print(f"  Total tokens: {usage.get('totalTokens', 'N/A')}")
        print(f"\nStop Reason: {response_1['stopReason']}")

        print ("=" * 60)

        conversation_history.append({
            "role": "assistant",
            "content": [{"text": assistant_reply_1}]
        })

        user_message_2 = "That sounds great! Can you give me a quick recipe?"
        conversation_history.append({
            "role": "user",
            "content": [{"text": user_message_2}]
        })

        response_2 = bedrock_runtime.converse(
            modelId=model_id,
            system=system_prompt,
            messages=conversation_history,
            inferenceConfig={
                "temperature": 0.7,
                "maxTokens": 2000
            }
        )

        assistant_reply_2 = response_2['output']['message']['content'][0]['text']
        print("\nAssistant Response to User Message 2:")
        print(assistant_reply_2)      

        print ("=" * 60)
        usage_2 = response_2.get('usage', {})
        print(f"Token Usage for User Message 2:")
        print(f"  Input tokens: {usage_2.get('inputTokens', 'N/A')}")
        print(f"  Output tokens: {usage_2.get('outputTokens', 'N/A')}")
        print(f"  Total tokens: {usage_2.get('totalTokens', 'N/A')}")
        print(f"\nStop Reason: {response_2['stopReason']}")
        print ("=" * 60)  
    except Exception as e:
        print(f"Error during multi-turn conversation: {e}")
        raise   

if __name__ == "__main__":
    multi_turn_conversation()