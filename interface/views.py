from django.http import HttpRequest
from django.shortcuts import render
from .models import Sections, Sub_sections


# Create your views here.
def header(request):
    return render(request, 'interface/header/header.html')


def blocks(request):
    sections = Sections.objects.all()
    return render(request, 'interface/blocks.html',
                  {
                      'sections': sections
                  }
                  )


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


def table_list(request):
    subsections = Sub_sections.objects.all()
    sections = Sections.objects.all()
    url = request.GET['block']
    return render(request, 'interface/table_list.html',
                  {
                      'sub': subsections,
                      'seс': sections,
                      'url': int(url),
                      'url1': url
                  }
                  )




