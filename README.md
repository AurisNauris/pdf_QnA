# pdf_QnA
This is a simple project intended to learn how to interact with a pdf using a LLM.

# Installation
To install the required libraries:
```
pip install -r requirements.txt
```
Create a .env file in the directory and insert "ANTHROPIC_API_KEY=<YOUR_API_KEY>"

# Usage

python main.py "path-to-your-pdf.pdf" "Database query to extract relevant information about your pdf" "Question to LLM about database"

# Short description

This is a learning project aimed to understand how to write a pipeline that:
1. Loads a pdf
2. Extracts text
3. Performs simple chunking of text into 500 character long strings, with 100 character long overlap
4. The chunks get embedded
5. ChromaDB is used to retrieve relevant information for context (Database is in memory only)
6. The anthropic api is used to ask a question wrt to the context

# Obvious improvements

1. Database in long storage
2. Improved chunking strategy
3. Improved retrieval of context strategy
4. Support for follow up questions.

# Personal take (2026-03-14)

- It was a fun small project to understand how the tools are interconnecting with each other.
- I would definitely recommend a similar small project to someone else who wants to start learning about AI engineering.
- While the project could grow a lot with a lot of extra engineering, a simple implemention to be done yourself is enough to learn skills about AI engineering and even general computing.
- The vector database clicked well with other ML concepts, that I was using analysing hyperspectral data. In particular, the representation of the text chunk as a point in a high dimensional space that can then be clustered or searched in similarity.
- I can see how even a "simple" pipeline like this with extra engineering can be very useful tool to interact with information when you have a lot of pdfs without (a) having to spend A LOT of money on the API calls that charge per token, and (b) getting more accurate answers b/c the context for the LLM is much better targeted.
