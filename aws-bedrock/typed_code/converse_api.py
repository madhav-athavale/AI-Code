import boto3
import json
def use_converse_api():
    bedroc_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
    model_id = "us.amazon.nova-lite-v1:0"
    system_prompt = [
        {"text": "You are a helpful technical assistant who explains concepts clearly and concisely."}
    ]

    user_message = "What is serverless computing?"
    print("Using Bedrock Converse API")
    print("=" * 60)
    print(f"System Prompt: {system_prompt[0]['text']}")
    print(f"User Message: {user_message}\n")
    try:
        repsone= bedroc_runtime.converse(
            modelId=model_id,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": [{"text": user_message}]
                }
            ],
            inferenceConfig={
                "temperature": 0.7,
                "maxTokens": 2000
            }
        )
        output_text = repsone['output']['message']['content'][0]['text']
        print("Assistant Response:")
        print(output_text)
        repsone_usage = repsone.get('usage', {})
        print(f"\nToken Usage:")
        print(f"  Input tokens: {repsone_usage.get('inputTokens', 'N/A')}")
        print(f"  Output tokens: {repsone_usage.get('outputTokens', 'N/A')}")
        print(f"  Total tokens: {repsone_usage.get('totalTokens', 'N/A')}")
        print(f"\nStop Reason: {repsone['stopReason']}")
        return repsone
    except Exception as e:
        print(f"Error using Converse API: {e}")
        raise
if __name__ == "__main__":
    use_converse_api()






