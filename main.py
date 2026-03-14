import pymupdf
import sys
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import matplotlib.pyplot as plt
import chromadb
import pprint
from dotenv import load_dotenv
from anthropic import Anthropic
load_dotenv()

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

def basic_similarity_check(list_of_sentences):
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(list_of_sentences)
    sim_matrix = np.full(shape=(len(embeddings),len(embeddings)),fill_value=np.nan)
    for i, em1 in enumerate(embeddings):
        for j, em2 in enumerate(embeddings):
            tmp_sim = cosine_similarity(em1.reshape(1,-1),em2.reshape(1,-1))
            sim_matrix[i,j] = tmp_sim[0,0]
    
    tmp = sim_matrix.copy()
    np.fill_diagonal(tmp, -1.0)
    flat_sorted = np.argsort(tmp, axis=None)[::-1]
    
    for k in range(6):
        i, j = np.unravel_index(flat_sorted[k], sim_matrix.shape)
        if i>=j: # prevents duplicates
            continue
        print("-"*5,k,"-"*5)
        print("Most similar sentences are:")
        print(list_of_sentences[i])
        print(list_of_sentences[j])

    plt.figure()
    plt.imshow(sim_matrix)
    plt.show()

file_path = sys.argv[1]
extracted_pages = extract_text(file_path)
chunks = simple_chunking(extracted_pages)

chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="test_collection")
ids = [str(i) for i in range(len(chunks))]
collection.add(ids=ids,
               documents=chunks,
               )

results = collection.query(query_texts = sys.argv[2],
                           n_results=5,
                           )

client = Anthropic() # automatically picks up API key from .env using load_dotenv()

context = "\n\n".join(results["documents"][0])
prompt = f"""Based on the following context, answer the question.

Context:
{context}

Question: {sys.argv[3]}

If information not found in the context, respond that "Information not found in the context"

"""

response = client.messages.create(model="claude-haiku-4-5-20251001",
                                  max_tokens=1024*4,
                                  messages=[{"role":"user","content":prompt}]
                                  )

print(response.content[0].text)