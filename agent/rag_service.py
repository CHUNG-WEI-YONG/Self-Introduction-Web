import os
import chromadb
from dotenv import load_dotenv
from google import genai
from google.genai import types

from portfolio.models import Project, Technology
from blog.models import Post

load_dotenv()

CHROMA_DATA_PATH = os.path.join(os.path.dirname(__file__), "chroma_db")
client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)

# 模型标识符
EMBEDDING_MODEL_NAME = "gemini-embedding-2"
CHAT_MODEL_NAME = "gemini-3.8-flash"


def get_genai_client():
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY in .env file.")
    return genai.Client(api_key=api_key)


class CloudEmbeddingFunction(chromadb.EmbeddingFunction):
    def __call__(self, input: chromadb.Documents) -> chromadb.Embeddings:
        if not input:
            return []

        embeddings = []
        genai_client = get_genai_client()

        for text in input:
            res = genai_client.models.embed_content(
                model=EMBEDDING_MODEL_NAME,
                contents=text
            )
            # 兼容处理：支持复数形式或单数形式的返回对象
            if hasattr(res, 'embeddings') and res.embeddings:
                values = res.embeddings[0].values
            elif hasattr(res, 'embedding'):
                values = res.embedding.values
            else:
                values = res[0]
            embeddings.append(values)

        return embeddings


emb_adaptor = CloudEmbeddingFunction()


def sync_knowledge_base():
    documents = []
    metadatas = []
    ids = []

    # 1. 抽取技术栈
    for tech in Technology.objects.select_related('category').all():
        doc = (
            f"[Tech Stack] Name: {tech.name}\n"
            f"Category: {tech.category.name}\n"
            f"Proficiency Level: {tech.get_proficiency_display()}\n"
            f"Status: {'Actively learning' if tech.is_learning else 'Mastered'}"
        )
        documents.append(doc)
        metadatas.append({"type": "tech", "name": tech.name})
        ids.append(f"tech_{tech.id}")

    # 2. 抽取项目
    for project in Project.objects.prefetch_related('technologies').all():
        tech_list = ", ".join([t.name for t in project.technologies.all()])
        github = getattr(project, 'github_link', None) or getattr(project, 'github_url', None) or 'Private'
        doc = (
            f"[Project] Title: {project.title}\n"
            f"Summary: {project.description}\n"
            f"Technologies Used: {tech_list}\n"
            f"Repository: {github}"
        )
        documents.append(doc)
        metadatas.append({"type": "project", "title": project.title})
        ids.append(f"proj_{project.id}")

    # 3. 抽取已发布的博客
    for post in Post.objects.filter(status=Post.Status.PUBLISHED).prefetch_related('tags').all():
        tag_list = ", ".join([t.name for t in post.tags.all()])
        summary = post.summary if post.summary else post.content[:200]
        snippet = post.content[:1500].replace('\r\n', ' ')
        doc = (
            f"[Blog Article] Title: {post.title}\n"
            f"Tags: {tag_list}\n"
            f"Summary: {summary}\n"
            f"Content: {snippet}"
        )
        documents.append(doc)
        metadatas.append({"type": "blog", "title": post.title})
        ids.append(f"post_{post.id}")

    if documents:
        try:
            client.delete_collection("portfolio_knowledge_v1")
        except Exception:
            pass

        fresh_collection = client.create_collection(
            name="portfolio_knowledge_v1",
            embedding_function=emb_adaptor,
            metadata={"hnsw:space": "cosine"},
        )
        fresh_collection.add(documents=documents, metadatas=metadatas, ids=ids)
        return len(documents)
    return 0


def query_agent(question: str) -> str:
    try:
        active_col = client.get_collection(
            name="portfolio_knowledge_v1",
            embedding_function=emb_adaptor
        )

        results = active_col.query(
            query_texts=[question],
            n_results=min(4, max(1, active_col.count()))
        )

        retrieved_docs = results['documents'][0] if results['documents'] else []
        context_text = "\n\n---\n\n".join(retrieved_docs) if retrieved_docs else "No specific database records matched."

    except Exception as e:
        context_text = f"Vector search fallback (Error: {str(e)})"

    system_instruction = (
        "You are the official AI Technical Assistant representing software engineer WY.Chung.\n"
        "Your mission is to accurately, professionally, and politely answer visitors' inquiries about Chung's technical capabilities, projects, and engineering blog posts.\n\n"
        "STRICT GUIDELINES:\n"
        "1. Base your statements ONLY on the verified information provided in [Context]. Do not invent skills, experience, or project details.\n"
        "2. If the context does not contain enough information to answer the question, honestly acknowledge that and suggest the visitor contact Chung directly via the email or GitHub links in the footer.\n"
        "3. Reply in the same language as the visitor's question (default to professional Chinese or English).\n"
        "4. Maintain a clean, engineering-oriented, humble yet confident tone."
    )

    prompt = f"""
[Context Information from Site Database]
{context_text}

[Visitor Question]
{question}
"""

    try:
        genai_client = get_genai_client()
        response = genai_client.models.generate_content(
            model=CHAT_MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2,
            )
        )
        return response.text

    except Exception as e:
        return f"System processing error: {str(e)}"