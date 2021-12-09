from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    # Для HTML-шаблонов
    return render(request, 'interface/header/header.html')


def about(request):
    # Для небольшой HTML-строки
    return HttpResponse("<h4>О нас</h4")

