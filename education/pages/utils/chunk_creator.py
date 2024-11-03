# Necessarry libraries 
from tqdm.auto import tqdm
import pandas as pd
import re

# A function to readjust the chunks
def readjust_chunks(pages_and_texts):
    pages_and_chunks = [] # Create list
    
    for item in tqdm(pages_and_texts): # For each item in the dictionary
        for sentence_chunk in item["sentence_chunks"]: # For each sentence chunk of the item
            chunk_dict = {} # Create a dict
            chunk_dict["page_number"] = item["page_number"] # Get the page number

            # Join the sentences together into a paragraph like structure, aka join the  list of sentences into one paragraph.
            joined_sentence_chunk = "".join(sentence_chunk).replace("  ", " ").strip()
            joined_sentence_chunk = re.sub(r"\.([A-Z])", r'. \1', joined_sentence_chunk)
            chunk_dict["sentence_chunk"] = joined_sentence_chunk

            # Get some stats
            chunk_dict["chunk_char_count"] = len(joined_sentence_chunk)
            chunk_dict["chunk_word_count"] = len([word for word in joined_sentence_chunk.split(" ")])
            chunk_dict["chunk_token_count"] = len(joined_sentence_chunk) / 4

            # Append the dict to the list
            pages_and_chunks.append(chunk_dict)

    # Return the list
    return pages_and_chunks

# A function to filter short sentences
def filter_chunks(pages_and_chunks, min_token_len: int):
    df = pd.DataFrame(pages_and_chunks) # Create a dataframe using the list
    pages_and_chunks_over_min_token_len = df[df["chunk_token_count"] > min_token_len].to_dict(orient = "records") # Filter the chunks
 
    # Return the final list
    return pages_and_chunks_over_min_token_len