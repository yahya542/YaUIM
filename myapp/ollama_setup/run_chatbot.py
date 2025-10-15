import os
import requests
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

# Placeholder for data loading
def load_data():
    # Load data from database or files
    # For now, dummy data
    data = [
        "Dosen John Doe mengajar Matematika di ruang 101 pada Senin jam 08:00.",
        "Kelas TI-2023 angkatan 2023.",
        "Mahasiswa Ahmad dengan NPM 123456 di kelas TI-2023."
    ]
    return data

# Create embeddings
def create_embeddings(data):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(data)
    return embeddings, model

# Setup FAISS index
def setup_faiss(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

# Retrieve relevant context
def retrieve_context(question, model, index, data, top_k=3):
    question_embedding = model.encode([question])
    distances, indices = index.search(question_embedding, top_k)
    context = [data[i] for i in indices[0]]
    return ' '.join(context)

# Query Ollama
def query_ollama(question, context):
    prompt = f"Context: {context}\nQuestion: {question}\nAnswer:"
    try:
        response = requests.post('http://localhost:11434/api/generate', json={
            'model': 'tinyllama:latest',
            'prompt': prompt,
            'stream': False
        })
        if response.status_code == 200:
            return response.json().get('response', 'No response key')
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Exception: {str(e)}"


if __name__ == "__main__":
    data = load_data()
    embeddings, model = create_embeddings(data)
    index = setup_faiss(embeddings)
    
    # Example query
    question = "Siapa dosen Matematika?"
    context = retrieve_context(question, model, index, data)
    answer = query_ollama(question, context)
    print(f"Question: {question}")
    print(f"Answer: {answer}")