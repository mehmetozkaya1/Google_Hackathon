# Necessarry libraries
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

# URL patterns
urlpatterns = [
    path('', views.index, name = 'index'),
    path('about', views.about, name="about"),
    path('teacher', views.teacher, name="teacher"),
    path('pdf-creator', views.pdf_creator, name="pdf-creator"),
    path('upload_pdf', views.upload_pdf, name='upload_pdf'),
    path('upload_pdf_teacher', views.upload_pdf_teacher, name='upload_pdf_teacher'),
    path('create-questions', views.create_questions, name="create_questions"),
    path('teacher_chatbot', views.teacher_chatbot, name='teacher_chatbot'),
    path('video-summarizer', views.video_summarizer, name="video_summarizer"),
    path('summarize_video', views.summarize_video, name="summarize_video"),
    path('visual_ai', views.visual_ai, name="visual_ai"),
    path('upload_image', views.upload_image, name="upload_image"),
    path('ask', views.ask, name="ask")
]

# For the static files and media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)