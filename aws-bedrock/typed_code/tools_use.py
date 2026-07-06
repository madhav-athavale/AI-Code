import json
import boto3
import requests
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

TOOL_CONFIG ={
    "tools":[
        {
            "toolSpec": {
                "name": "get_weather",
                "description": "Get the current weather for a given location.",
                "inputSchema" :{
                    "json": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The name of the city or location to get the weather for."
                            },
                        },
                        "required": ["location"]
                    } 

                },
            }}
                        
     ]
    
}

TOOL_FUNCTIONS = {
    "get_weather": get_weather, 
}

def run_tool(tool_name, tool_input):
    if tool_name in TOOL_FUNCTIONS:
        return TOOL_FUNCTIONS[tool_name](**tool_input)
    else:
        raise ValueError(f"Tool {tool_name} not found.")    
    
def tool_use_demo():
    bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
    model_id = "us.amazon.nova-lite-v1:0"
    

   
    user_message = "What's the current weather in New York City?"
    
    print("bedrock Tool Use Demo")
    
    print("=" * 60)
    print(f"User Message: {user_message}\n")
    
    messages = [
        {
            "role": "user",
            "content": [{"text": user_message}],
        }
    ]

    try:
        response = bedrock_runtime.converse(
            modelId=model_id,
            messages=messages,
            toolConfig=TOOL_CONFIG,
            inferenceConfig={
                "temperature": 0.7,
                "maxTokens": 2000
            },  
        )
         
        print("Model Response:")    
        print(json.dumps(response, indent=2))
        # Check if the model has decided to use a tool
        stop_reason = response["stopReason"]
        assistant_message = response["output"]["message"]
        
        print(f"\nStop Reason: {stop_reason}")
              
        
        if stop_reason == "tool_use":
            tool_use_block = None
            for block in assistant_message["content"]:
                if "toolUse" in block:
                    tool_use_block= block["toolUse"]
                    break
            tool_name = tool_use_block["name"]
            tool_input = tool_use_block["input"]
            tool_use_id = tool_use_block["toolUseId"]
            
            result = run_tool(tool_name, tool_input)
            
            print(f"\n[Step 3] Function returned: {json.dumps(result, indent=2)}")
            
            messages.append(assistant_message)
            messages.append({
                "role": "user",
                "content": [
                    {
                        "toolResult": {
                            "toolUseId": tool_use_id,
                            "content": [{"json": result}],
                        }
                    }
                ],
            })  
            
            print("\n[Step 4] Sending tool result back to model...")
            final_response = bedrock_runtime.converse(
                modelId=model_id,
                messages=messages,
                toolConfig=TOOL_CONFIG,
                inferenceConfig={
                    "temperature": 0.7,
                    "maxTokens": 2000
                },  
            )
            
            final_text = final_response["output"]["message"]["content"][0]["text"]
            print(f"\nAssistant: {final_text}")
                
        
    except  e:
        print(f"Error using Converse API: {e}")
        raise   
    
if __name__ == "__main__":
    tool_use_demo() 
    
            