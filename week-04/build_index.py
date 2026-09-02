import chromadb
import os
import json
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()

with open('chunks.json','r',encoding='utf-8') as f:
    chunks=json.load(f)

client=chromadb.PersistentClient(path='chroma_db')

openai_ef=embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv('OPENAI_API_KEY'),
    model_name='text-embedding-3-small'
)

collection=client.get_or_create_collection(
    name='vaultx_docs',
    embedding_function=openai_ef
)

ids=[chunk['chunk_id'] for chunk in chunks]
documents=[chunk['text'] for chunk in chunks]
metadatas=[{'source_file':chunk['source_file']} for chunk in chunks]

collection.add(
    ids=ids,
    documents=documents,
    metadatas=metadatas
)

print(f'{len(ids)} chunks added to vector database.')