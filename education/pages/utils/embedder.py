# Necessarry libraries 
from sentence_transformers import SentenceTransformer
from tqdm.auto import tqdm
import pandas as pd

# Create an embedding model
embedding_model = SentenceTransformer(model_name_or_path = "all-mpnet-base-v2", device = "cuda")

# A function to create text chunks
def create_text_chunks(pages_and_chunks_over_min_token_len):
    for item in tqdm(pages_and_chunks_over_min_token_len): # For each item in the chunks
        item["embedding"] = embedding_model.encode(item["sentence_chunk"]) # Encode each sentence chunk and create an embedding key

    # Create the text chunks
    text_chunks = [item["sentence_chunk"] for item in pages_and_chunks_over_min_token_len]

    # Return the text chunks
    return text_chunks

# A function to embed text in batches
def embed_texts_in_batches(text_chunks, batch_size, convert_to_tensor = True):
    text_chunk_embeddings = embedding_model.encode(text_chunks, batch_size = batch_size, convert_to_tensor = convert_to_tensor) # Embed the text chunks and convert them into a torch.Tensor

    # Return the text_chunks_embeddings
    return text_chunk_embeddings

# A function to save embeddings file
def save_embeddings_file(pages_and_chunks_over_min_token_len):
    text_chunks_and_embeddings_df = pd.DataFrame(pages_and_chunks_over_min_token_len) # Create a dataframe

    embeddings_df_save_path = f"pages/static/embeddings/text_chunks_and_embeddings_df.csv" # Create a path to save the file
    text_chunks_and_embeddings_df.to_csv(embeddings_df_save_path, index = False) # Save the file as a .csv file.