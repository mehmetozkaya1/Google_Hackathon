# Necessarry libraries
import numpy as np
import torch

# Set the device
device = "cuda" if torch.cuda.is_available() else "cpu"

# A function to create embeddings tensors
def create_embeddings_tensor(text_chunks_and_embeddings_df):
    # Convert embedding column back to np.array (it got converted to str when it saved to csv)
    text_chunks_and_embeddings_df["embedding"] = text_chunks_and_embeddings_df["embedding"].apply(lambda x: np.fromstring(x.strip("[]"), sep = "  "))

    # Convert our embeddings into a torch.tensor
    embeddings = torch.tensor(np.stack(text_chunks_and_embeddings_df["embedding"].tolist(), axis = 0), dtype = torch.float32).to(device)

    # Convert texts and embedding df to list of dicts
    pages_and_chunks = text_chunks_and_embeddings_df.to_dict(orient = "records")

    # Return the embeddings and pages_and_chunks list
    return embeddings, pages_and_chunks