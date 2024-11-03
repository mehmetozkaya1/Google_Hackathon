# Importing necessarry libraries
from tqdm.auto import tqdm
import fitz

# Performs minor formatting on text.
def text_formatter(text: str) -> str:
    cleaned_text = text.replace("\n", " ").strip() # Reformat the text

    # Return the cleaned text
    return cleaned_text

# Open and read the pdf and create a dict.
def open_and_read_pdf(pdf_path: str) -> list[dict]:
    doc = fitz.open(pdf_path) # Open the file
    pages_and_texts = [] # Create an empty list

    # For each page and the page number 
    for page_number, page in tqdm(enumerate(doc)):
        text = page.get_text() # Get the text
        text = text_formatter(text = text) # Format the text

        # Get some data about the file
        pages_and_texts.append({"page_number": page_number - 41,
                                "page_char_count": len(text),
                                "page_word_count": len(text.split(" ")),
                                "page_sentence_count": len(text.split(". ")),
                                "page_token_count": len(text) / 4,
                                "text": text})
        
    # Return the list
    return pages_and_texts