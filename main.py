from fastapi import FastAPI
import chromadb

app = FastAPI()

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("reachex_search")


@app.post("/add_document/")
async def add_document(id: str, text: str):
    collection.add(ids = [id], documents = [text], metadatas = [{"text": text}])
    return {"status": "Document added"}

@app.post("/search/")
async def search(query_text: str, top_k: int =5):
    results = collection.query(query_texts = [query_text], n_results = top_k)
    return results


