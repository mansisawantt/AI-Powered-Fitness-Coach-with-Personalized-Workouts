import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print("API Key loaded successfully!")
else:
    print("API Key is missing! Check your .env file.")