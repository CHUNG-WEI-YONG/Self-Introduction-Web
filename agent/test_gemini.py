import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

try:
  client = genai.Client(api_key=api_key)
  response = client.models.generate_content(
      model="gemini-3.8-flash",
      contents="Hello, confirm that you are online and working!",
  )
  print("\n✅ API Success! Response:")
  print(response.text)
except Exception as e:
  print("\n❌ Error:", e)