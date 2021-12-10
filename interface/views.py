from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def header(request):
    return render(request, 'interface/header/header.html')


def blocks(request):
    return render(request, 'interface/blocks.html')


def tables(request):
    return render(request, 'interface/tables.html')


def analisys(request):
    return render(request, 'interface/analisys.html')


def events(request):
    return render(request, 'interface/events.html')


def new_block(request):
    return render(request, 'interface/new_block.html')


def reports(request):
    return render(request, 'interface/reports.html')


