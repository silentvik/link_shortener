"""
    shortener_project URL Configuration
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('very_secret_administration/', admin.site.urls),
    path('', include('shortener_app.urls'))
]
