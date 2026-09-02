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

messages = []

while True:
    user_input = input("You: ")
    if user_input.strip().lower() in ['exit', 'quit']:
        break

    # Append the user's message to the conversation history
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=messages,
    )

    reply = response.choices[0].message.content

    # Append the assistant's reply to the conversation history
    messages.append({"role": "assistant", "content": reply})

    print("Bot:", reply)
