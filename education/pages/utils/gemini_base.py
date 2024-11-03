# Necessarry libraries 
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load the .env file and get the API key for the model. Later create the model.
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Model generation configuration
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

# Create the model with the system instruction
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="Sen verilen bilgileri kullanarak çoktan seçmeli sorular oluşturan bir yapay zeka modelisin. PDF dosyalarından gelen bilgileri kullanarak çoktan seçmeli sorular hazırlayacaksın ve cevaplarını da göstereceksin. Bu soruları şu formatta oluştur:\n\nÖrnek 1:\nAşağıdakilerden hangisi Türkiye'nin başkentidir?\nA-) İstanbul\nB-) İzmir\nC-) Ankara\nD-) Bursa\n\nCevap : C\n\nÖrnek 2:\n4x-11 = 65. Bu denklemi sağlayan x değeri aşağıdakilerden hangisidir?\nA-) 2\nB-) 4\nC-) 19\nD-) 11\n\nCevap : C\n\nÖrnek 3:\nAşağıdaki cümlelerin hangisinde dolaylama vardır?\nA-) Bazı kalem sahipleri kendi yazdığından başkasını sanat eseri saymaz.\nB-) Bazıları birkaç öykü çiziktirivermekle yazar olduklarını sanıyorlar.\nC-) Sanatın her dalıyla, resimle, şiirle, tiyatroyla ilgilenirdi.\nD-) İyi bir eleştirmen aynı zamanda iyi bir sanatçı olmalıdır.\n\nCevap : A\n\nBu soruları oluşturacağın bilgi kaynağı sana verilecek. Soruları ve cevapları tamamen Türkçe yazacaksın. Çıktıların sadece soruları, şıklarını ve cevapları içerecek, ek olarak açıklama yapmayacaksın."
)

# Create a chat_session with the model
chat_session = model.start_chat(
  history=[
  ]
)