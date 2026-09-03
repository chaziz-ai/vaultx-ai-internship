import json
import csv
from rag_query import generate_answer, retrieve_chunks

def load_questions(path='eval_questions.json'):
    with open(path,'r',encoding='utf-8') as f:
        return json.load(f)

def run_evaluation(questions,k=3):
    results=[]

    for q in questions:
        question_text=q['question']
        print(f'\n[{q["id"]}] Asking: {question_text}')

        answer=generate_answer(question_text,k=k)

        retrieved=retrieve_chunks(question_text,k=k)
        sources_used=[meta['source_file'] for  meta in retrieved['metadatas'][0]]

        results.append({
           'id':q['id'],
           'question':question_text,
           'expected_answer':q['expected_answer'],
           'should_refuse':q['should_refuse'],
           'rag_answer':answer,
           'retrieved_sources':';'.join(sources_used),
           'correct(y/n)':'',
           'grounded(y/n)':'',
           'notes':''
        })

    return results

def save_to_csv(results,path='eval_results.csv'):
    field_names=list(results[0].keys())
    with open(path,'w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=field_names)
        writer.writeheader()
        writer.writerows(results)
    print(f'\nSaved {len(results)} results to {path}')

if __name__=='__main__':
    questions=load_questions('eval_questions.json')
    results=run_evaluation(questions,k=5)
    save_to_csv(results,'eval_results.csv')
    print('\nDone.Open eval_results.csv and fill correct/grounded columns')