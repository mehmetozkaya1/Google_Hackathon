# Necessarry libraries
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load the .env file and get the API key for the model. Later create the model.
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_VISUAL_API_KEY"))

# Model generation configuration
generation_config = {
  "temperature": 0.9,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

# Create the model
model_visual = genai.GenerativeModel(model_name="gemini-1.5-pro", generation_config = generation_config)