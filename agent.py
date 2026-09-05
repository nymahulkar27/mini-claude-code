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

model = "gpt-5.4-mini"

SYSTEM_PROMPT = """You are a coding agent running in the user's terminal. You can list files, read files, write files and run shell commands. Use your tools to complete the user's task, then briefly summarize what you did. The working directory is folder the user launched you from"""  

def list_files(path="."):
    entries = []
    for entry in os .scandir(path):
       entried.append(entry.name)