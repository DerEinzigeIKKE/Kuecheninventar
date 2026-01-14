import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: GOOGLE_API_KEY not found.")
else:
    try:
        client = genai.Client(api_key=api_key)
        print("Listing available models:")
        # The method to list models in the new SDK might differ, 
        # but typically it's client.models.list() or similar.
        # We'll try the standard pattern for the new SDK.
        for model in client.models.list():
            print(f"- {model.name} (Display: {model.display_name})")
            
    except Exception as e:
        print(f"Error listing models: {e}")
