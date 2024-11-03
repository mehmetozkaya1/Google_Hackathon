from pdf_preprocessing import open_and_read_pdf
from sentencizer import sentencize_sentences, create_sentence_chunks
from chunk_creator import readjust_chunks, filter_chunks
from embedder import create_text_chunks, embed_texts_in_batches, save_embeddings_file, embedding_model
from faiss_db import create_faiss_index, add_embeddings_to_faiss
from tensorizer import create_embeddings_tensor
from retriever import retrieve_relevant_passages
from pdf_creator import create_pdf

import pandas as pd
import sys

sys.stdout.reconfigure(encoding = 'utf-8')

from gemini_base import chat_session

NUM_SENTENCE_CHUNK_SIZE = 10
MIN_TOKEN_LEN = 30
BATCH_SIZE = 32

pages_and_texts = open_and_read_pdf(pdf_path = "education/pages/static/pdfs/insan_anatomisi.pdf")
sentencize_sentences(pages_and_texts)
create_sentence_chunks(pages_and_texts, NUM_SENTENCE_CHUNK_SIZE)
pages_and_chunks = readjust_chunks(pages_and_texts)
pages_and_chunks_over_min_token_len = filter_chunks(pages_and_chunks, min_token_len = MIN_TOKEN_LEN)
text_chunks = create_text_chunks(pages_and_chunks_over_min_token_len)
text_chunk_embeddings = embed_texts_in_batches(text_chunks, BATCH_SIZE, convert_to_tensor = True)

save_embeddings_file(pages_and_chunks_over_min_token_len)

text_chunks_and_embeddings_df = pd.read_csv("education/pages/static/embeddings/text_chunks_and_embeddings_df.csv")
embeddings, pages_and_chunks = create_embeddings_tensor(text_chunks_and_embeddings_df)

faiss_vd = create_faiss_index(embedding_dim=len(text_chunk_embeddings[0]))
add_embeddings_to_faiss(faiss_vd, text_chunk_embeddings)

queries = ["Popliteal bölge", "Beyin sapının bölümleri", "Deri’nin eklenti organları"]

questions = ""

for query in queries:
    relevant_passages = retrieve_relevant_passages(query = query, embedding_model = embedding_model, index = faiss_vd, text_chunks = text_chunks, top_k = 10)

    response = chat_session.send_message(relevant_passages)
    final_response = response.text.replace("*", "")

    questions += final_response + "\n"

file_name = "education/pages/static/pdfs/sorular.pdf"
create_pdf(text_data = questions, file_name = file_name)