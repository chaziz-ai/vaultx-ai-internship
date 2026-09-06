from fastapi import FastAPI
from pydantic import BaseModel
from rag_query import generate_answer

app=FastAPI()

class Question(BaseModel):
    question:str
    k: int=5

@app.post('/ask')
def ask(payload : Question):
    result=generate_answer(payload.question,payload.k)

    return{
        'question': payload.question,
        'answer': result['answer'],
        'grounded': result['grounded'],
        'sources': result['sources']
    }