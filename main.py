from fastapi import FastAPI, UploadFile, File
import pandas as pd
import chromadb

app = FastAPI()

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("reachex_search")


@app.post("/add_document/")
async def add_document(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_excel(contents, engine='openpyxl')

        if 'id' not in df.columns or 'text' not in df.columns:
            return {"error" : "Excel must contain 'id' and 'text' columns"}
        
        ids = df['id'].astype(str).tolist()
        texts = df['text'].astype(str).tolist()
        metadatas = [{"text": text} for text in texts]

        collection.add(ids = ids, documents = texts, metadatas = metadatas)

        return {"status": f"{len(ids)} documents added successfully"}
    
    except Exception as e:
        return {"error": str(e)}
    



@app.post("/add_keyword/")
async def add_keyword(id: str, text: str):
    try:
        collection.add(ids = [id], documents = [text], metadatas = [{"text": text}])
        return {"status": "Keyword added"}
    
    except Exception as e:
        return {"error": str(e)}


@app.get("/get_all_elements/")
async def get_all_elements():
    try:
        results = collection.get()
        return results
    
    except Exception as e:
        return {"error": str(e)}

@app.post("/search/")
async def search(query_text: str, top_k: int =5):
    try:
        results = collection.query(query_texts = [query_text], n_results = top_k)
        return results
    except Exception as e:
        return {"error": str(e)}


