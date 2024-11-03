# Necessarry libraries
from django.contrib import admin
from django.urls import path, include

# URL patterns
urlpatterns = [
    path('', include('pages.urls')),
    path("admin/", admin.site.urls),
]
