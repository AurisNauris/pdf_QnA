import pymupdf
import sys

def extract_text(file_path):
    doc = pymupdf.open(file_path)
    pages = []
    
    for page in doc:
        pages.append(page.get_text())
    doc.close()

    return pages

file_path = sys.argv[1]
extracted_pages = extract_text(file_path)
print(extracted_pages[0])