from django.http import HttpRequest

from django.shortcuts import render
from django import forms
from .models import *
# from .forms import *
import requests
import pandas as pd
import matplotlib.pyplot as plt

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


# Функция формирует двумерный массив данных
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


def add(request):
    section = Sections.objects.filter(id=request.GET['section'])
    sub_section = Sub_sections.objects.filter(id=request.GET['sub_section'])
    table_structure = Subsections_data.objects.filter(section_id=request.GET['section'], subsection_id=request.GET['sub_section'])
    posts_names = []
    posts_names_dict = {}
    for table_structure1 in table_structure:
        # Исключаем служебные поля из форм, так как они не заполняются
        if table_structure1.sql_field_name != 'year_load' and table_structure1.sql_field_name != 'author':
            # Собираем посты и запаковываем их в словарь
            posts_names_dict[table_structure1.sql_field_name] = request.POST[table_structure1.sql_field_name]
    posts_names_dict['year_load'] = 2020;
    posts_names_dict['author'] = 'Funikov';
    posts_names_dict['is_delete'] = 0;
    # Формируем имя создаваемого экземпляра
    class_name = get_class_name_by_section_subsection(sub_section)
    # Аргумент с двумя звёздочками - распаковка словаря обрабатываесых данных
    # За счёт него можно передавать сколько угодно значений, а не фиксированное количество
    save = get_model_name(class_name)(**posts_names_dict).save()
    # Текст урл для редиректа
    new_url = '/table_view?section=' + str(request.GET['section']) + '&sub_section=' + str(request.GET['sub_section'])

    return render(request, 'interface/add.html', {
        'url': new_url
    })


def table_view(request):

    # Достаём имя раздела по идентификатору, указанному в GET параметре
    section_id = request.GET['section']
    sub_section_id = request.GET['sub_section']
    section = Sections.objects.filter(id=request.GET['section'])
    for s_section in section:
        section_id = s_section.id
    # Имя подраздела по тому же принципу
    sub_section = Sub_sections.objects.filter(id=request.GET['sub_section'])
    for s_sub_section in sub_section:
        sub_section_id = s_sub_section.id
    if request.FILES:
        log = upload_file(request, sub_section)
        new_url = '/table_view?section=' + str(request.GET['section']) + '&sub_section=' + str(request.GET['sub_section'])
        return render(request, 'interface/import_results.html', {
            'url': new_url,
            'ms': log
        })
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
        # 'form': form
        # 'file_info': file
    })


def upload_file(request, sub_section):
        file = pd.read_excel(request.FILES['excel'])
        # Тут хранится файл
        # file = pd.DataFrame(file)
        # Массив заголовков
        file_headers = list(file.columns.values)

        section_id = request.GET['section']
        sub_section_id = request.GET['sub_section']
        # Структура обрабатываемой таблицы
        datas = Subsections_data.objects.filter(section_id=section_id, subsection_id=sub_section_id)
        # Собираем заголовки для нужной таблицы из базы.
        database_headers = []

        for data in datas:
            if data.html_descriptor != 'Автор' and data.html_descriptor != 'Год':
                database_headers.append(data.html_descriptor)

        # Если заголовки базы не совпадают с теми, которые загрузил юзер - загружен неверный файл
        if file_headers != database_headers:
            log_message = 'Для данной таблицы выгруженный файл не подходит. Повторите попытку импорта'
            return log_message

        lens = GetCountriesList(request)

        # Массив словарей для записи
        array_dicts = []
        for i in range(0,len(file)):
            if 'Страна прибытия' in database_headers:
                country = file['Страна прибытия'][i]
                if country not in list(lens.keys()):
                    log = 'В строке ' + str(i + 2) + ' найдена ошибка в наименовании страны. Исправьте её и повторите импорт снова.'
                    return log
            # Словарь для записи
            dict_save = {}
            for data in datas:
                if data.html_descriptor != 'Автор' and data.html_descriptor != 'Год':
                    dict_save[data.sql_field_name] = file[data.html_descriptor][i]
            dict_save['year_load'] = 2020
            dict_save['author'] = 'Andre'
            dict_save['is_delete'] = 0
            array_dicts.append(dict_save)

        model = get_model_name(get_class_name_by_section_subsection(sub_section))

        # Перебор созданного словаря
        for dict in array_dicts:
            # Вставка словаря при помощи распаковки словаря аргументов **kwargs. Документация
            model(**dict).save()
        log = "Импорт записей произведён успешно"
        return log


def GetCountriesList(request):
    countries = RefCountry.objects.all()
    list = []
    Dict = {}
    for countr in countries:
        Dict[countr.name] = countr.id
        fn = countr.fullname
        if fn != '':
            Dict[countr.fullname] = countr.id
    return Dict