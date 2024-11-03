# AI-Powered Web Platform with Google Gemini

Bu proje, Google Gemini LLM modelini kullanarak geliştirilmiş, dört benzersiz yapay zeka aracını içeren kapsamlı bir AI tabanlı web platformunun kaynak kodlarını içerir. Platformumuz, belge işleme, etkileşimli öğrenme, video özetleme ve görsel tabanlı soru-cevap özelliklerini şık ve modern bir arayüzde bir araya getirmektedir.

---

## 📌 Proje Özeti

**Google Gemini** modelini kullanan bu çok işlevli AI web uygulaması, **HTML, CSS, JavaScript, Bootstrap** ile frontend ve **JavaScript, Python, Django** ile backend üzerinde geliştirilmiştir. Öne çıkan bir diğer özellik, **Retrieval-Augmented Generation (RAG) mimarisini** sıfırdan yazmamızdır. İşte içerdiğimiz her bir AI aracının işlevleri:

1. **PDF Üzerinden Soru Üretici**  
   - Bir PDF dosyası yükleyin ve soru üretmek istediğiniz konuları belirtin. RAG tabanlı sistem, belirttiğiniz konulara uygun soruları PDF dosyasından üretir. Oluşturulan soruları indirmeniz için PDF olarak sunar.

2. **Etkileşimli PDF Öğretmeni**  
   - PDF dosyanızı yükleyerek içeriği hakkında soru sorabileceğiniz bir sohbet başlatın. Bu araç, PDF içerisindeki konular hakkında ayrıntılı bilgi vererek bir yapay zeka öğretmeni olarak çalışır.

3. **YouTube Video Özetleyici**  
   - Eğitim odaklı bir YouTube videosunun URL'sini girin. Model, videonun ana noktalarını kısa bir özet ve küçük notlar halinde sunar.

4. **Görsel Tabanlı Soru-Cevap ve OCR**  
   - Bir görsel yükleyerek içeriği hakkında sorular sorabilirsiniz. Model, görselden metin çıkarabilir, çeviri yapabilir veya çözülmüş soruların doğruluğunu kontrol edebilir.

Her araçta yanıt üretimi için **Google Gemini** kullanılıyor; RAG mimarisi ise belirli veri getirme görevlerini yönetiyor.

---

## 🔧 Teknoloji Yığını

- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Backend**: JavaScript, Python (Django)
- **AI Mimarisi**: Özel olarak geliştirilmiş RAG sistemi
- **LLM Modeli**: Google Gemini

---

## 🛠️ Kurulum ve Çalıştırma

1. **Depoyu Klonlayın**

   ```bash
   git clone https://github.com/mehmetozkaya1/Google_Hackathon
   cd education

2. **Ortamı Hazırlayın**

    ```bash
    pip install -r requirements.txt

3. **Django Sunucusunu Çalıştırın**

   ```bash
   cd education
   python manage.py runserver

4. **Uygulamayı Açın**

   Tarayıcınızda http://localhost:8000 adresini açın.

---

## 📝 AI Araçlarının Kullanımı

1. **PDF Üzerinden Soru Üretici**  
   - Bir PDF dosyası yükleyin ve ilginizi çeken konuları belirtin.
   - **Soru Üret** butonuna tıklayarak konuyla ilgili soruları oluşturun.
   - Oluşturulan soruları PDF olarak indirmeniz mümkün.

2. **Etkileşimli PDF Öğretmeni**  
   - Bir PDF dosyası yükleyin ve sohbet başlatın.
   - PDF içeriğiyle ilgili sorularınızı sorun ve ayrıntılı cevaplar alın.

3. **YouTube Video Özetleyici**  
   - YouTube video URL'sini girin.
   - **Videoyu Özetle** butonuna tıklayarak kısa bir özet ve notları alın.

4. **Görsel Tabanlı Soru-Cevap ve OCR**  
   - Bir görsel yükleyin ve içeriğiyle ilgili sorular sorun.
   - Model, görseldeki metinleri çıkarabilir, çeviri yapabilir veya doğruluk kontrolü yapabilir.

---

## 🧠 Model Detayları

- **Google Gemini**: RAG tabanlı sistemde veri getirme ve yanıt üretme işlemlerini gerçekleştirir.
- **RAG Mimarisi**: Ek kütüphaneler kullanılmadan sıfırdan geliştirilmiş olup, veri getirme ve sentezleme işlemlerinde verimlilik sağlar.

---

## 🚀 Gelecekteki Geliştirmeler

- PDF dışında diğer belge formatlarını (örneğin Word, TXT) destekleme.
- Video özetleme aracını farklı platformları destekleyecek şekilde genişletme.
- Görsel tabanlı soru-cevap aracı için çoklu dil desteği ekleme.
