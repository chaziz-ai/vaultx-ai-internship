import os
import json
from pypdf import PdfReader
import re

DOCS_FOLDER = "docs"
OUTPUT_FILE = "chunks.json"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

def extract_text_from_pdf(pdf_path):
    reader=PdfReader(pdf_path)
    full_text=""
    for page in reader.pages:
        page_text=page.extract_text()
        if page_text:
            full_text+=page_text+'\n'
    return full_text

def clean_text(text):
    text=re.sub(r'\s+',' ',text)
    return text.strip()

def chunk_text(text,chunk_size=CHUNK_SIZE,overlap=CHUNK_OVERLAP):
    chunks=[]
    start=0
    text_length=len(text)

    while start<text_length:
        end=start+chunk_size
        chunk=text[start:end]
        chunks.append(chunk)
        start=start+(chunk_size-overlap)
    return chunks

def  main():
    all_chunks=[]

    pdf_files=[f for f in os.listdir(DOCS_FOLDER) if f.endswith('.pdf')]
    print(f'Found {len(pdf_files)} PDF files')

    for filename in pdf_files:
        pdf_path=os.path.join(DOCS_FOLDER,filename)
        print(f'Processing {filename}')

        raw_text=extract_text_from_pdf(pdf_path)
        cleaned=clean_text(raw_text)
        file_chunks=chunk_text(cleaned)

        for i,chunk in enumerate(file_chunks):
            all_chunks.append({
                'text':chunk,
                'source_file':filename,
                'chunk_id':f'{filename}_chunk_{i}'
            })

        print(f'{len(file_chunks)} chunks created')

    with open(OUTPUT_FILE,'w',encoding='utf-8') as f:
        json.dump(all_chunks,f,indent=2,ensure_ascii=False)

    print(f'Total chunks: {len(all_chunks)}, saved to {OUTPUT_FILE}')

if __name__=='__main__':
    main()