import os
from dotenv import load_dotenv
from google import genai

# 加载 .env 中的密钥
load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Missing GEMINI_API_KEY in .env file.")

client = genai.Client(api_key=api_key)

print("Connecting to Google GenAI for embedding...")
result = client.models.embed_content(
    model="gemini-embedding-2",
    contents="Hello, this is a test document."
)

print("\n--- Raw Result Object ---")
print(result)

print("\n--- Extraction Check ---")
if hasattr(result, "embeddings") and result.embeddings:
    values = result.embeddings[0].values
    print("Number of embeddings:", len(result.embeddings))
    print("Vector dimension:", len(values))
elif hasattr(result, "embedding"):
    values = result.embedding.values
    print("Single embedding vector dimension:", len(values))

print("✅ Embedding test passed successfully!")