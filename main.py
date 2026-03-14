import pymupdf
import sys
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import matplotlib.pyplot as plt
import chromadb
import pprint

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
#embedding = model.encode(chunks[:2])
#print("-"*10)
#print(embedding)
#print("embedding shape:", embedding.shape)

# test_sentences = ["The cat sat on the mat",
#                  "The kitten was sitting on the rug",
#                  "Stock prices rose sharply today",
#                  "The mat sat on the cat",
#                  "The dog sat on the cat",
#                  "The stock market is devasted by the recent crisis",
#                  "I am running out of money to pay for my rent"
#                  ]

#basic_similarity_check(test_sentences)
# print(list(range(len(test_sentences))))
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="test_collection")

ids = [str(i) for i in range(len(chunks))]

collection.add(ids=ids,
               documents=chunks)

results = collection.query(query_texts = ["I am intereted in the very first neural network."],
                           n_results=3,)

print(results["documents"][0])
