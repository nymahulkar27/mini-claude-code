import json

from configparser import ConfigParser
from unittest import result
from unittest import result
from openai import OpenAI

# Initialize the ConfigParser
config = ConfigParser()

# Read the configuration file
config.read('config.ini')

# Retrieve the API key (specify section and key name)
OPENAI_API_KEY = config.get('api_keys', 'openai_api_key')

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"Error reading file: {e}"

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the text file and return its contents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string", "description": "The path to the file to read."
                    }
                },
                "required": ["path"]
            }
        }
        
    }
]

messages = [
    {"role": "user", "content": "YWhat is inside notes1.txt and notes2.txt? Summarize the contents"},
]

while True:
    # Generate a response from the model
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=messages,
        tools=TOOL_SCHEMAS,
    )

    # Extract the assistant's reply from the response
    message = response.choices[0].message
    #print(message)
    messages.append(message)

    # Print the assistant's reply
    if not message.tool_calls:
        print(message.content)
        break
    
    # If the model wants to call a tool, handle the tool call
    for tool_call in message.tool_calls:
        args = json.loads(tool_call.function.arguments)
        print(f"Model wants to run: read_file({args})")

        result = read_file(**args) 

        messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})

    print(messages)