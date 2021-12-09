from django.urls import path
from . import views

urlpatterns = [
    # Отсылка к файлу маршрутов приложения interface
    path('', views.index),
    path('about', views.about),
]
