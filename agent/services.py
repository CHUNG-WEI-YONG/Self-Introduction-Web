import os
from pathlib import Path
import chromadb
from google import genai
from google.genai import types

BASE_DIR=Path(__file__).resolve().parent.parent
CHROMA_DATA_PATH = os.environ.get("CHROMA_PATH", str(BASE_DIR / "chroma_db"))

class KnowLedgeBaseService:
    def __init__(self):
        self.chroma_client=chromadb.PersistentClient(path=CHROMA_DATA_PATH)
        self.collection=self.chroma_client.get_or_create_collection(name="portfolio_knowledge")
        self.gemini_client=genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    def get_embedding(self,text):
        response=self.gemini_client.models.embed_content(
            model="text-embedding-004",
            contents=text,
        )

        return response.embeddings[0].values

    def chunk_text(self,text,chunk_size,overlap):
        words = text.split()
        if not words:
            return []
        chunks = []
        start = 0
        while start < len(words):
            end = start + chunk_size
            chunks.append(" ".join(words[start:end]))
            start += (chunk_size - overlap)
        return chunks

    def upsert_entity(self, entity_type: str, entity_id: int, title: str, content: str, url: str):
        self.delete_entity(entity_type, entity_id)

        full_text = f"Title: {title}\nType: {entity_type}\nContent: {content}"
        chunks = self.chunk_text(full_text)

        ids, docs, embeddings, metadatas = [], [], [], []
        for idx, chunk in enumerate(chunks):
            chunk_id = f"{entity_type}_{entity_id}_chunk_{idx}"
            ids.append(chunk_id)
            docs.append(chunk)
            embeddings.append(self.get_embedding(chunk))
            metadatas.append({
                "entity_type": entity_type,
                "entity_id": str(entity_id),
                "title": title,
                "url": url,
                "chunk_index": idx
            })

        if ids:
            self.collection.upsert(
                ids=ids,
                documents=docs,
                embeddings=embeddings,
                metadatas=metadatas
            )

    def delete_entity(self, entity_type: str, entity_id: int):
            try:
                self.collection.delete(
                    where={"$and": [
                        {"entity_type": {"$eq": entity_type}},
                        {"entity_id": {"$eq": str(entity_id)}}
                    ]}
                )
            except Exception:
                pass
