# Necessarry libraries
from spacy.lang.tr import Turkish

# Create the NLP models
nlp = Turkish()

# Add a sentenciser pipeline
nlp.add_pipe("sentencizer")

# A function to decide the sentences
def sentencize_sentences(pages_and_texts):
    for item in pages_and_texts: # For each item in the list 
        item["sentences"] = list(nlp(item["text"]).sents) # Create the sentences
        item["sentences"] = [str(sentence) for sentence in item["sentences"]] # Convert them into str
        item["page_sentence_count_spacy"] = len(item["sentences"]) # Count the sentences

# A function to split sentences using the give slice_size parameter
def split_list(input_list: list,
               slice_size: int ) -> list[list[str]]:
    # Split the list and return it
    return [input_list[i: i+slice_size] for i in range(0, len(input_list), slice_size)]

# A function to create sentence_chunks
def create_sentence_chunks(pages_and_texts, slice_size):
    for item in pages_and_texts: # For each item in the list
        item["sentence_chunks"] = split_list(input_list = item["sentences"],
                                             slice_size = slice_size) # Split the sentences and create sentence chunks
        item["num_chunks"] = len(item["sentence_chunks"]) # Get the length of the sentence chunks