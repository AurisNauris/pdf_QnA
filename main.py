import pymupdf
import sys
from sentence_transformers import SentenceTransformer 

def extract_text(file_path):
    doc = pymupdf.open(file_path)
    pages = []
    
    for page in doc:
        pages.append(page.get_text())
    doc.close()

    return pages

def simple_chunking(pages):
    pages_str = " ".join(pages)
    chunks = []
    for i in range(0,len(pages_str),400):
        chunk = pages_str[i:i+500]
        chunks.append(chunk)

    if len(chunks[-1]) != 500:
     chunks[-1] = pages_str[-500:]
    return chunks


file_path = sys.argv[1]
extracted_pages = extract_text(file_path)
chunks = simple_chunking(extracted_pages)

print(chunks[0])

model = SentenceTransformer("all-MiniLM-L6-v2")
embedding = model.encode(chunks[:2])
print("-"*10)
print(embedding)
print("embedding shape:", embedding.shape)