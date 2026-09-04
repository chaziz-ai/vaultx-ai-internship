from fastapi import FastAPI
from pydantic import BaseModel
from rag_query import generate_answer,retrieve_chunks

app=FastAPI()

class Question(BaseModel):
    question:str
    k: int=5

@app.post('/ask')
def ask(payload : Question):
    answer=generate_answer(payload.question,payload.k)
    results=retrieve_chunks(payload.question,payload.k)

    sources=[]
    for meta in results['metadatas'][0]:
        sources.append(meta['source_file'])

    return{
        'question': payload.question,
        'answer': answer,
        'sources': sources
    }