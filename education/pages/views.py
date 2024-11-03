# Importing our necessarry libraries
from django.http import JsonResponse
from django.shortcuts import render
from .forms import PDFUploadForm, ImageUploadForm
from django.conf import settings
import google.generativeai as genai
from yt_dlp import YoutubeDL
from PIL import Image
import mimetypes
import os

# Utils
from .utils.pdf_preprocessing import open_and_read_pdf
from .utils.sentencizer import sentencize_sentences, create_sentence_chunks
from .utils.chunk_creator import readjust_chunks, filter_chunks
from .utils.embedder import create_text_chunks, embed_texts_in_batches, save_embeddings_file, embedding_model
from .utils.faiss_db import create_faiss_index, add_embeddings_to_faiss
from .utils.tensorizer import create_embeddings_tensor
from .utils.retriever import retrieve_relevant_passages
from .utils.pdf_creator import create_pdf
from .utils.gemini_base import chat_session
from .utils.gemini_teacher import chat_session_teacher
from .utils.gemini_voice import model_voice, chat_session_voice
from .utils.gemini_visual import model_visual

# Global Variables
NUM_SENTENCE_CHUNK_SIZE = 10
MIN_TOKEN_LEN = 30
BATCH_SIZE = 32

# The function to return the web page index.html
def index(request):
    return render(request, 'pages/index.html')

# The function to return the web page about.html
def about(request):
    return render(request, 'pages/about.html')

# The function to return the web page teacher.html
def teacher(request):
    return render(request, 'pages/teacher.html')

# The function to return the web page pdf_creator.html
def pdf_creator(request):
    return render(request, 'pages/pdf_creator.html')

# The function to return the web page video_summarizer.html
def video_summarizer(request):
    return render(request, 'pages/video_summarizer.html')

# The function to return the web page visual_ai.html
def visual_ai(request):
    return render(request, 'pages/visual_ai.html')

# The function to upload a pdf file
def upload_pdf(request):
    if request.method == 'POST': # If it is a POST request
        form = PDFUploadForm(request.POST, request.FILES) # Create a form object
        if form.is_valid(): # If the form is valid
            pdf_file = request.FILES['pdf_file']
            file_name = pdf_file.name
            file_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', file_name) # Create the file path

            # Save the pdf file
            with open(file_path, 'wb+') as destination:
                for chunk in pdf_file.chunks():
                    destination.write(chunk)

            # Create a session for the pdf file name
            request.session['pdf_file_name'] = file_name

            # Render the pdf_creator.html page with success and the form object
            return render(request, 'pages/pdf_creator.html', {'form': form, 'success': True})
    else: # If it is an GET request, then only return the empty form
        form = PDFUploadForm()

    # Finally render the original page again
    return render(request, 'pages/pdf_creator.html')

# The function to upload a pdf file in another way for teacher.html page
def upload_pdf_teacher(request):
    if request.method == 'POST': # If it is a POST request
        form = PDFUploadForm(request.POST, request.FILES) # Create a form object
        if form.is_valid(): # If it is valid
            pdf_file = request.FILES['pdf_file']
            file_name = pdf_file.name
            file_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', file_name) # Create the file path

            with open(file_path, 'wb+') as destination: # Save the pdf file
                for chunk in pdf_file.chunks():
                    destination.write(chunk)

            # Create sessions text_chunks and pdf_file_name to use them in another function
            request.session['pdf_file_name'] = file_name
            text_chunks, faiss_vd = preprocessing_pdf_func(request)
            request.session['text_chunks'] = text_chunks

            # Render the teacher_questioner.html page with success and the form object
            return render(request, 'pages/teacher_questioner.html', {'form': form, 'success': True})
    else: # If it is an GET request, then only return the empty form
        form = PDFUploadForm()

    # Finally render the original page again
    return render(request, 'pages/teacher_questioner.html')

# Preprocess the pdf file to use in RAG model.
def preprocessing_pdf_func(request):
    pdf_name = request.session.get("pdf_file_name") # Get the pdf file name

    pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', f'{pdf_name}') # Create a file path
    pages_and_texts = open_and_read_pdf(pdf_path = pdf_path) # Create a dictionary
    sentencize_sentences(pages_and_texts = pages_and_texts) # Sentencize all sentences
    create_sentence_chunks(pages_and_texts = pages_and_texts, slice_size = NUM_SENTENCE_CHUNK_SIZE) # Split the sentences into chunks
    pages_and_chunks = readjust_chunks(pages_and_texts = pages_and_texts) # Readjust the chunks to create paragraphs
    pages_and_chunks_over_min_token_len = filter_chunks(pages_and_chunks = pages_and_chunks, min_token_len = MIN_TOKEN_LEN) # Delete the chunks that are above the min token length
    text_chunks = create_text_chunks(pages_and_chunks_over_min_token_len = pages_and_chunks_over_min_token_len) # Create the text chunks
    text_chunk_embeddings = embed_texts_in_batches(text_chunks=text_chunks, batch_size=BATCH_SIZE, convert_to_tensor=True) # Embed text chunks
    save_embeddings_file(pages_and_chunks_over_min_token_len = pages_and_chunks_over_min_token_len) # Save them as a .csv file

    faiss_vd = create_faiss_index(embedding_dim=len(text_chunk_embeddings[0])) # Create a FAISS Vector Database 
    add_embeddings_to_faiss(index = faiss_vd, embeddings = text_chunk_embeddings) # Add all embeddings to the FAISS vector database 

    # Return text chunks and FAISS vector database
    return text_chunks, faiss_vd 

# A function to generate questions using the given PDF
def create_questions(request):
    if request.method == "POST": # If it is a POST request 
        text_chunks, faiss_vd = preprocessing_pdf_func(request) # Create the text chunks and add them to faiss vector database
        topics = request.POST.get('topics') # Get the topics from the HTML page to generate questions about them

        queries = topics.split(',') # Split the topics from ',' and create a list
        questions = ""

        # For each query, retrieve relevant passages from the PDF, give them to GEMINI to create questions about the passages.
        for query in queries:
            relevant_passages = retrieve_relevant_passages(query = query, embedding_model = embedding_model, index = faiss_vd, text_chunks = text_chunks, top_k = 10)
            response = chat_session.send_message(relevant_passages)
            final_response = response.text.replace("*", "")

            questions += final_response + "\n"

        # Create a path to save the created question's PDF
        file_save_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', 'created_pdf.pdf')

        # Create and save the PDF in the given location
        create_pdf(text_data = questions, file_name = file_save_path)

        # Create a pdf url to reach in the HTML file
        pdf_url = os.path.join(settings.MEDIA_URL, 'pdfs', 'created_pdf.pdf')

        # Render the created_pdf.html page
        return render(request, 'pages/created_pdf.html', {'pdf_url': pdf_url})

# A function that creates answers for the given query. It uses RAG architecture to retrieve relevant passages and generates answers from them
def teacher_chatbot(request):
    if request.method == "POST": # If it is a POST request
        user_message = request.POST.get('message') # Get the user message from the HTML page
        query = user_message

        text_chunks = request.session.get('text_chunks') # Get the created text_chunks using request.session
        
        # Create the embeddings of text chunks and faiss vector database
        text_chunk_embeddings = embed_texts_in_batches(text_chunks=text_chunks, batch_size=BATCH_SIZE, convert_to_tensor=True)
        faiss_vd = create_faiss_index(embedding_dim=len(text_chunk_embeddings[0]))
        add_embeddings_to_faiss(index = faiss_vd, embeddings = text_chunk_embeddings)

        # Get the relevant info about the query
        relevant_info = retrieve_relevant_passages(query = query, embedding_model = embedding_model, index = faiss_vd, text_chunks = text_chunks, top_k = 5)

        # Give them to GEMINI to create an answer using that information
        response = chat_session_teacher.send_message(user_message)
        
        # Reformat the response
        final_response = response.text.replace("*", "")

        # Create a JSONResponse and send them to the HTML page
        return JsonResponse({'response': final_response, 'relevant_info':relevant_info})
    
    return JsonResponse({'response': 'Geçersiz istek'}, status=400)

# A function to download a Youtube video as a .mp3 file using Youtube URL
def download_audio(youtube_url, output_path):
    # ydl options
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'ffmpeg_location': 'C:/Mehmet Genel/Mehmet Yazılım/ffmpeg/ffmpeg-2024-10-31-git-87068b9600-full_build/bin/ffmpeg.exe',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    # Download the Youtube video as a .mp3 file
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

# A function to summarise the the video content
def summarize_video(request):
    if request.method == "POST": # If it is a POST request
        youtube_url = request.POST.get('youtube_url') # Get the URL from the HTML page
        output_path = f"/pages/static/sound/video_sound" # Create an output path to save the audio

        # Download the audio
        download_audio(youtube_url=youtube_url, output_path=output_path)

        # If the meme type is not certain, create a meme type
        mime_type, _ = mimetypes.guess_type(output_path + ".mp3")
        if mime_type is None:
            mime_type = 'audio/mpeg'

        # Upload the audio file
        audio_file = genai.upload_file(path=output_path + ".mp3", mime_type=mime_type)

        # Create the prompt and summarize the video
        prompt = """Verilen ses dosyasının metnini çıkar. Tamamen Türkçe yap."""
        response = model_voice.generate_content([prompt, audio_file])
        response = chat_session_voice.send_message(response.text)
        speech = response.text
 
        # Create a JSONResponse and send it to HTML page
        return JsonResponse({'speech': speech})
    else:
        # Create a JSONResponse and send it to HTML page
        return JsonResponse({'speech': "Geçersiz İstek!"})

# A function to upload an image file
def upload_image(request): 
    if request.method == 'POST': # If it is a POST request 
        form = ImageUploadForm(request.POST, request.FILES) # Create a form object
        if form.is_valid(): # If the form is valid
            img_file = request.FILES['img_file']
            file_name = img_file.name
            file_path = os.path.join(settings.MEDIA_ROOT, 'imgs', file_name) # Create a file path to the image

            # Open and read the image file
            with open(file_path, 'wb+') as destination:
                for chunk in img_file.chunks():
                    destination.write(chunk)

            # Save the image
            with Image.open(file_path) as img:
                static_img_path = f"pages/static/img/{file_name}"
                img.save(static_img_path)

            # Create a session for the image path
            request.session['img_file_path'] = static_img_path

            # Create an image file url to show it in the HTML page
            file_url = os.path.join('img', file_name)

            # Render the visual_ai.html with the form, susscess and image file url
            return render(request, 'pages/visual_ai.html', {'form': form, 'success': True, 'file_url': file_url})
    else:
        form = ImageUploadForm()

    # Render the visual_ai.html with the form, susscess
    return render(request, 'pages/visual_ai.html', {'form': form, 'success': False})

# A function to answer the questions about the image
def ask(request):
    if request.method == "POST": # If it is a POST request
        expectations = request.POST.get('expectations') # Get the expectations from html page
        img_path = request.session.get('img_file_path') # Get the image path

        # Open the image
        img = Image.open(img_path)

        # Create a prompt and generate an asnwer
        prompt = expectations + "Cevabını Türkçe oluştur."
        response = model_visual.generate_content([prompt, img])

        # Create a JSONResponse and send it to HTML page
        return JsonResponse({'response': response.text})
    else:
        # Create a JSONResponse and send it to HTML page
        return JsonResponse({'response': "Geçersiz bilgi girildi!"})