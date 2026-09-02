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


response = client.chat.completions.create(
    model="gpt-5.4-mini",
    messages=[
        #{"role": "system", "content": "You are a helpful AI assitant. Answer concisely in short sentences."},
        {"role": "user", "content": "Exaplin what an AI agent is in one sentence."},
        #{"role": "assistant", "content": "An AI agent is simply and LLM connected to tools in a loop."}, 
    ],
)

print(response.choices[0].message.content)
