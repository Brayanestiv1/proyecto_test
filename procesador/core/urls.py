from django.urls import path
from .views import procesar_archivo

urlpatterns = [
    path('procesar/', procesar_archivo),
]