import json
import os
import subprocess

from configparser import ConfigParser
from openai import OpenAI

# Initialize the ConfigParser
config = ConfigParser()

# Read the configuration file
config.read('config.ini')

# Retrieve the API key (specify section and key name)
OPENAI_API_KEY = config.get('api_keys', 'openai_api_key')

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

MODEL = "gpt-5.4-mini"

SYSTEM_PROMPT = """You are a coding agent running in the user's terminal. You can list files, read files, write files and run shell commands. Use your tools to complete the user's task, then briefly summarize what you did. The working directory is folder the user launched you from"""  

def list_files(path="."):
    entries = []
    for entry in os .scandir(path):
       entries.append(entry.name + ("/" if entry.is_dir() else ""))
    return "\n".join(sorted(entries)) or "(empty directory)"

def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return file.read()
    except Exception as e:
        return f"Error reading file: {e}"

def write_file(path, content):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Saved {path} ({len(content)} characters)"
    except Exception as e:
        return f"Error writing file: {e}"

def run_command(command):
    try:
        answer = input(f"Run '{command}'? (y/n): ")
        if answer.strip().lower() != 'y':
            return "The user declined to run the command." 
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=120)
        output = (result.stdout + result.stderr).strip()
        return output or f"(No output, exit code {result.returncode})"
    except Exception as e:
        return f"Error running command: {e}"

TOOLS = {
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
    "run_command": run_command
}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List the files in a directory. Folders end with /.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory to the list, e.g. '.'"},
                },
                "required": ["path"],
            },
        },
    }, 
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the text file and return its contents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "The path to the file to read."}
                },
                "required": ["path"],
            },
        },      
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Create or overwrite a text file with the given content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path of the file to write."},
                    "content": {"type": "string", "description": "Full contents of the file."},
                },
                "required": ["path", "content"],
            },
        },      
    },
        {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Run a shell command and return its output. The user approves it first.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The shell command to run."},
                },
                "required": ["command"],
            },
        },      
    },
]

def run_tool(tool_call):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    print(f" tool: {name}({args})")
    try:
        return str(TOOLS[name](**args))
    except Exception as error:
        return f"Error: {error}"

def run_agent(messages):
    while True:
        # Generate a response from the model
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOL_SCHEMAS,
        )

        # Extract the assistant's reply from the response
        message = response.choices[0].message
        messages.append(message)

        # Print the assistant's reply
        if not message.tool_calls:
            return message.content
            #print(message.content)
            #break

        # If the model wants to call a tool, handle the tool call
        for tool_call in message.tool_calls:
            result = run_tool(tool_call)
            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})

def main():
    #print(SYSTEM_PROMPT)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("Mini agent is ready. Type 'exit' to quit.")

    while True:
        user_input = input("\nYou: ")
        if user_input.strip().lower() in ("exit", "quit"):
            break
        messages.append({"role": "user", "content": user_input})
        reply = run_agent(messages)
        print(f"\nAgent: {reply}")

if __name__ == "__main__":  
    main()
