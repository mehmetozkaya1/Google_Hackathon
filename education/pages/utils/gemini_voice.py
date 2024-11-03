# Necessarry libraries
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load the .env file and get the API key for the model. Later create the model.
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_VOICE_API_KEY"])

# Model generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the model with the system instruction
model_voice = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="""
        Verilen metin bir ders videosuna ait. Senden bu metni kullanarak ilgili özet notlar çıkarmanı istiyorum. Notlar tamamen Türkçe olacak ve sadece not kısımlarını içerecek. Aşağıda bir örnek var.
        Örnek:
        Orta Asya Türk Tarihi:
        1. Göktürkler Dönemi (552-745)
        Kuruluş: Türk Kağanlığı, Bumin Kağan tarafından 552 yılında kuruldu.
        Yönetim: İlk Türk devleti olan Göktürkler, Orta Asya'da büyük bir imparatorluk kurarak Batı ve Doğu Göktürkleri olarak ikiye ayrıldılar.
        Yazılı Kaynaklar: Orhun Yazıtları, Türklerin tarihsel belgeleri arasında yer alır.
        Yıkılış: 745 yılında Uygurların saldırılarıyla zayıflayarak yıkıldılar.
        2. Uygur Kağanlığı (744-840)
        Yönetim: Uygurlar, Göktürkler’in ardından Orta Asya'da güçlü bir devlet kurdular.
        Din: Maniheizm, Budizm ve şamanizm etkili oldu.
        Kültür: Uygurlar, tarım ve ticaretle uğraştılar; yazılı kültürü geliştirdiler.
        Yıkılış: 840 yılında Kırgızlar tarafından yıkıldılar.
        3. Karahanlılar Dönemi (840-1212)
        Kuruluş: Karahanlılar, Uygur Kağanlığı'nın yıkılmasından sonra ortaya çıktı.
        İslamlaşma: 10. yüzyılda İslamiyet’i kabul ettiler ve bu durum Orta Asya’da İslam kültürünün yayılmasında etkili oldu.
        Ticaret: İpek Yolu üzerindeki stratejik konumları sayesinde zenginleştiler.
        Yıkılış: 1212’de Cengiz Han’ın istilaları sonucu zayıfladılar.
        4. Selçuklu İmparatorluğu (1037-1194)
        Kuruluş: Selçuklular, Oğuz Türkleri’nin bir koludur. 11. yüzyılda kuruldular.
        İran’a Hakimiyet: Selçuklular, İran ve Anadolu'ya hakim oldular, Büyük Selçuklu Devleti’ni kurdular.
        Kültürel Gelişmeler: Mimari eserler, medreseler ve bilimsel çalışmalar ile kültürel birikim sağladılar.
        """
)

# Create a chat session for the model
chat_session_voice = model_voice.start_chat(
  history=[
  ]
)

model_voice = genai.GenerativeModel(model_name="gemini-1.5-flash")