# A function to retrieve relevant data from the PDF file
def retrieve_relevant_passages(query, embedding_model, index, text_chunks, top_k = 5):
    query_embedding = embedding_model.encode([query], convert_to_numpy = True) # Embed the query
    distances, indices = index.search(query_embedding, top_k) # Get the most relevant sentences
    relevant_passages = [text_chunks[idx] for idx in indices[0]] # Get the sentences

    # Return the relevant passages
    return relevant_passages