import os
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")
print("API Key exists:", bool(api_key))

try:
    client = genai.Client(api_key=api_key)
    print("Client created successfully.")
except Exception as e:
    print("Error creating client:", e)
