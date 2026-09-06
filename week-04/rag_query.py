import chromadb
import os
from openai import OpenAI
from dotenv import load_dotenv
from chromadb.utils import embedding_functions

load_dotenv()

client=chromadb.PersistentClient(path='chroma_db')

openai_ef=embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv('OPENAI_API_KEY'),
    model_name='text-embedding-3-small'
)

collection=client.get_or_create_collection(
    name='vaultx_docs',
    embedding_function=openai_ef
)

llm_client=OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

DISTANCE_THRESHOLD = 1.5  


def retrieve_chunks(question,k=3):
    results=collection.query(
        query_texts=[question],
        n_results=k
    )
    return results


def check_hallucination(answer, context):
    """LLM se dobara check karwao ke answer context se supported hai ya nahi."""
    if 'Answer not found in documents' in answer:
        return True  

    check_prompt = f'''Context:
{context}

Answer given: {answer}

Is this answer FULLY supported by the context above? Reply with ONLY one word: "GROUNDED" or "HALLUCINATED".'''

    response = llm_client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': check_prompt}],
        temperature=0
    )
    verdict = response.choices[0].message.content.strip().upper()
    return 'GROUNDED' in verdict


def generate_answer(question,k=3):
    results=retrieve_chunks(question,k)
    documents=results['documents'][0]
    metadatas=results['metadatas'][0]
    distances=results['distances'][0]

    sources_used = [
        {'source_file': metadatas[i]['source_file'], 'distance': distances[i]}
        for i in range(len(documents))
    ]

    if not documents or min(distances) > DISTANCE_THRESHOLD:
        return {
            'answer': 'Answer not found in documents.',
            'sources': [],
            'grounded': True
        }

    context_parts=[]
    for i,doc in enumerate(documents):
        source=metadatas[i]['source_file']
        context_parts.append(f'[Source{i+1}-{source}]\n{doc}')

    context='\n\n'.join(context_parts)

    system_prompt='''You are a helpful assistant that answers questions ONLY using the provided context below.
Rules:
- Use ONLY the information in the context. Do not use outside knowledge.
- If the answer is not in the context, say exactly: "Answer not found in documents."
- Always cite which Source number(s) you used, like [Source 1], [Source 2]'''

    user_prompt=f'Context:\n{context}\n\nQuestion: {question}'

    response=llm_client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role':'system','content':system_prompt},
            {'role':'user','content':user_prompt}
        ]
    )

    answer = response.choices[0].message.content

    is_grounded = check_hallucination(answer, context)
    if not is_grounded:
        answer = 'Answer not found in documents. (Flagged as potentially ungrounded)'

    
    return {
        'answer': answer,
        'sources': sources_used,
        'grounded': is_grounded
    }


if __name__=='__main__':
    test_questions = [
        'What is deadline of week 2 submission?',
        'What is the capital of France?'
    ]
    for q in test_questions:
        print('='*50)
        print('Q:', q)
        result = generate_answer(q)
        print('Answer:', result['answer'])
        print('Grounded:', result['grounded'])
        print('Sources:', result['sources'])