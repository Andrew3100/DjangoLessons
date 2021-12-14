from django.http import HttpRequest
from django.shortcuts import render
from .models import *
import pandas as pd
import numpy as np





# Функция формирует имя экземпляра класса (если не понятно, читаем документацию по моделям Django)
def get_class_name_by_section_subsection(sub_section):
    for sub_s in sub_section:
        sub_name = sub_s.param_name.split(sep='_')
        # Узнаём имя класса, через которое надо обратиться к модели
        class_name = ''
        for i in range(0, len(sub_name)):
            class_name = class_name + sub_name[i].title()
    return class_name


# Функция создаёт экземпляр по строковому имени класса
def get_model_name(string):
    if string == 'TableAus':
        return TableAus
    if string == 'TableCultDoc':
        return TableCultDoc
    if string == 'TableCultEvent':
        return TableCultEvent
    if string == 'TableEcDocument':
        return TableEcDocument
    if string == 'TableEcEvents':
        return TableEcEvents
    if string == 'TableGrants':
        return TableGrants
    if string == 'TableGuberDocLinks':
        return TableGuberDocLinks
    if string == 'TableGuberInternational':
        return TableGuberInternational
    if string == 'TableInternational':
        return TableInternational
    if string == 'TableInternationalDocument':
        return TableInternationalDocument
    if string == 'TableMobile':
        return TableMobile
    if string == 'TableOch':
        return TableOch
    if string == 'TableSportDoc':
        return TableSportDoc
    if string == 'TableSportInter':
        return TableSportInter
    if string == 'TableStudentChange':
        return TableStudentChange
    if string == 'TableWork':
        return TableWork
    if string == 'TableYoung':
        return TableYoung
    if string == 'TableZaoch':
        return TableZaoch


# Функция формирует двумерный массив данных (не включая служебные поля)
def get_table_data(table_structure, table_data):
    # Главный массив данных
    full_data = []
    for table_data1 in table_data:
        # Подчинённый массив данных
        data = []
        # Перебираем структуру таблицы и пытаемся сунуть элементы в свойства объекта.
        # Благодаря этому можно не делать милиарды лишних шаблоно
        for table_structure1 in table_structure:
            # Костыль, позволяющий передать совйство объекта в видк строки
            data.append(table_data1.__getattribute__(table_structure1.sql_field_name))
        full_data.append(data)
        del data
    return full_data

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

def table_view(request):
    if request.FILES:
        # Тут будет кусок кода, который обрабатывает Excel
        # Этапы - сохранить файл, прочитать пандасом, кинуть в базу
        ms = ''
    # Достаём имя раздела по идентификатору, указанному в GET параметре
    section = Sections.objects.filter(id=request.GET['section'])

    for s_section in section:
        section_id = s_section.id

    # Имя подраздела по тому же принципу
    sub_section = Sub_sections.objects.filter(id=request.GET['sub_section'])

    for s_sub_section in sub_section:
        sub_section_id = s_sub_section.id

    # Достаём данные по структуре таблицы
    table_structure = Subsections_data.objects.filter(section_id=request.GET['section'], subsection_id=request.GET['sub_section'])
    class_name = get_class_name_by_section_subsection(sub_section)

    # Запрос к базе данных
    table_data = get_model_name(class_name).objects.filter(is_delete=0)

    # Обращаемся к функции получения данных и получаем в ответ двумерный массив
    data = get_table_data(table_structure, table_data)

    return render(request, 'interface/table_view.html', {
        # Раздел
        'section': section,
        'section_id': section_id,
        # Подраздел
        'sub_section': sub_section,
        'sub_section_id': sub_section_id,
        # Заголовки таблицы
        'table_structure': table_structure,
        # Двумерный массив содержимого
        'data': data,
        # 'ms': ''
        'file_info': request.FILES
    })