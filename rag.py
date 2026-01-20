import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class RAGEngine:
    def __init__(self, knowledge_file="knowledge.txt"):
        print("Loading RAG Engine...")
        # Initialize a lightweight model to convert text into embeddings (numbers)
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.chunks = []
        
        # Load data and build the search index
        self._load_and_index(knowledge_file)

    def _load_and_index(self, filepath):
        if not os.path.exists(filepath):
            print(f"Warning: {filepath} not found. RAG will be empty.")
            return

        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()

        # Split text into chunks (paragraphs separated by double newlines)
        # You can improve this logic for better segmentation
        self.chunks = [chunk.strip() for chunk in text.split('\n\n') if chunk.strip()]
        
        if not self.chunks:
            return

        # Convert text chunks to vector embeddings
        embeddings = self.encoder.encode(self.chunks)
        
        # Create the FAISS vector database
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings).astype('float32'))
        print(f"RAG Engine Ready: Indexed {len(self.chunks)} chunks.")

    def search(self, query, top_k=3):
        if not self.index or not self.chunks:
            return "No knowledge base available."

        # Convert the user query into a vector
        query_vector = self.encoder.encode([query])
        
        # Search for the nearest vectors (most similar text)
        distances, indices = self.index.search(np.array(query_vector).astype('float32'), top_k)
        
        results = []
        for i in range(top_k):
            idx = indices[0][i]
            if idx != -1:
                results.append(self.chunks[idx])
        
        return "\n".join(results)