import os
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from bs4 import BeautifulSoup
import httpx
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

documents = []
index = None
embedder = None
KB_FOLDER = os.path.join(os.path.dirname(__file__), "oracle_kbs")
LITELLM_URL = os.environ.get("LITELLM_URL", "http://litellm:4000/v1/chat/completions")
MODEL_NAME = os.environ.get("LITELLM_MODEL", "vertex_ai/gemini-2.5-flash")

@asynccontextmanager
async def lifespan(app: FastAPI):
    global index, embedder, documents
    
    print("Loading Embedding Model...")
    embedder = SentenceTransformer('all-MiniLM-L6-v2') 
    
    print("Parsing HTML...")
    texts = []
    if os.path.exists(KB_FOLDER):
        for fname in os.listdir(KB_FOLDER):
            if fname.endswith(".html"):
                with open(os.path.join(KB_FOLDER, fname), encoding="utf-8", errors="ignore") as f:
                    soup = BeautifulSoup(f, "html.parser")
                    text = " ".join(soup.get_text(separator=" ", strip=True).split())
                    if len(text) > 50:
                        documents.append(text)
                        texts.append(text)
    if texts:
        print(f"Embedding {len(texts)} documents...")
        embeddings = embedder.encode(texts)
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(embeddings))
        print("Index ready.")
    
    yield

app = FastAPI(lifespan=lifespan)

class AskRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask(req: AskRequest):
    context = ""
    found_chunks = []

    if index and embedder and documents:
        query_vector = embedder.encode([req.question])
        D, I = index.search(query_vector, k=3) 
        found_chunks = [documents[i] for i in I[0] if i < len(documents)]

        kb_number = None
        import re
        match = re.search(r'KB\d{5,}', req.question)
        if match:
            kb_number = match.group(0)
            for doc in documents:
                if kb_number in doc and doc not in found_chunks:
                    found_chunks.append(doc)

        ora_match = re.findall(r'ORA-\d{5}', req.question)
        for ora_code in ora_match:
            for doc in documents:
                if ora_code in doc and doc not in found_chunks:
                    found_chunks.append(doc)
                    
        context = "\n---\n".join(found_chunks)

    prompt = f"Context:\n{context}\n\nQuestion: {req.question}"
    
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
    }
    
    async with httpx.AsyncClient() as client:
        resp = await client.post(LITELLM_URL, json=payload, timeout=60)
        resp_json = resp.json()
        if 'choices' in resp_json:
            answer = resp_json['choices'][0]['message']['content']
        else:
            answer = f"Error from LiteLLM: {resp_json}"

    return {"answer": answer, "context": context}