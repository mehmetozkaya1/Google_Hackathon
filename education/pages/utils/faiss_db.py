# Necessarry libraries 
import faiss
import numpy as np

# A function to create an index of FAISS vector database 
def create_faiss_index(embedding_dim): 
    index = faiss.IndexFlatL2(embedding_dim) # Create the index
    
    # Return the index of FAISS vector database
    return index

# A function to add the embeddings to the faiss index
def add_embeddings_to_faiss(index, embeddings):
    embeddings_np = np.array([embedding.cpu().numpy() for embedding in embeddings]) # convert each embedding into a numpy array
    index.add(embeddings_np) # Add them to the faiss index

    # Return the faiss index
    return index