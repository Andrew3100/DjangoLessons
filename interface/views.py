from django.http import HttpRequest
from django.http import HttpResponse

from django.shortcuts import render
from django import forms
from .models import *
# from .forms import *
import requests

import pandas as pd
import matplotlib.pyplot as plt
from django.urls import resolve

# Проверяет, входит ли заданный GET-параметр в URL
def is_get_param_in_this_url(url, get):
    array = url.split('&')

    del array[0]
    array = array
    dict = {}
    for i in array:
        arr = i.split('=')
        dict[arr[0]] = arr[1]
    gets = list(dict.keys())
    if get in gets:
        return True
    return False

# Функция достаёт данные по фильтрам таблицы
def get_filters_data(class_name, section, subsection):
    filters_data = Subsections_data.objects.filter(section_id = section, subsection_id = subsection)
    dict = {}
    for f_d in filters_data:
        dict[f_d.sql_field_name] = f_d.filter_type
    return dict


# Функция создана для того, чтобы вернуть нужное число диапазона при отборе записей в базе данных
def get_max_value_on_field(model,field,param,request):
    if is_get_param_in_this_url(request.get_full_path_info(), filter_MySQL_field(field)+'___rangestart') == True:
        return request.GET[filter_MySQL_field(field)+'___rangestart']
    field = filter_MySQL_field(field)
    datas = model.objects.filter(is_delete=0)
    dat = []
    for data in datas:
        dat.append(data.__getattribute__(field))
    if param == 'max':
        res = max(dat)
    else:
        res = min(dat)
    return res


# Функция фильтрует GET-параметры до исходного названия полей в MySQL.
def filter_MySQL_field(field):
    f = field.split('___')
    if f != []:
        return (f[0])
    else:
        return field


# Функция создаёт фильтры по полям. Аргумент - массив полей. Возврат - словарь с ключом "описание фильтра", а значением массив данных по полю
def get_field_filters(model, array, url, request):
    arr1 = []
    for i in range(0, len(array)):
        label = Subsections_data.objects.filter(section_id = request.GET['section'], subsection_id = request.GET['sub_section'], sql_field_name = array[i])
        arr = []
        # Имя метки:
        for l in label:
            arr.append(l.html_descriptor)
            arr.append(l.sql_field_name)
            arr.append('Все значения')
            if is_get_param_in_this_url(url, l.sql_field_name) or is_get_param_in_this_url(url, l.sql_field_name+'___rangestart'):
                if is_get_param_in_this_url(url, l.sql_field_name + '___rangestart'):
                    arr.append(request.GET[l.sql_field_name + '___rangestart'])
                else:
                    arr.append(request.GET[l.sql_field_name + '___rangeend'])
            else:
                arr.append('Выберите значение')
            if is_get_param_in_this_url(url, l.sql_field_name + '___rangeend'):
                arr.append(request.GET[l.sql_field_name + '___rangeend'])
        datas = model.objects.filter(is_delete=0)
        for data in datas:
            if data.__getattribute__(array[i]) not in arr:
                arr.append(data.__getattribute__(array[i]))

        arr1.append((list((arr))))
    return arr1




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


def get_a_set_of_filters(filters):
    filters_types = list(filters.values())
    filters_fields = list(filters.keys())
    counts_f = []
    fields_f = []
    dates_f = []

    for i in range(0, len(filters_types)):
        if filters_types[i] == 'count':
            counts_f.append(filters_fields[i])
        if filters_types[i] == 'date':
            dates_f.append(filters_fields[i])
        if filters_types[i] == 'field':
            fields_f.append(filters_fields[i])
    return fields_f, counts_f, dates_f


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
    off_words = []
    for t in table_structure:
        off_words.append(t.sql_field_name)
        off_words.append(t.html_descriptor)
    class_name = get_class_name_by_section_subsection(sub_section)

    # Достаём данные по фильтрам таблицы
    # переменная filters это словарь где ключ - поле БД, которое фильтруется, а значение - тип фильтра.
    # Типы фильтров:
    # если пусто - фильтра нет
    # count - фильтр по количественным данным
    # date -  фильтр по дате
    # field - фильтр по полю БД
    filters = get_filters_data(get_model_name(class_name), section_id,sub_section_id)
    # 0 - поля
    # 1 - кол-во (диапазон)
    # 2 - кол-во (даты)
    # передаём эти элементы в методы получения фильтров
    filters = get_a_set_of_filters(filters)
    current_url = (request.get_full_path_info())
    # Получаем фильтры по полям
    filters_by_fields_labels = get_field_filters(get_model_name(class_name),filters[0], current_url, request)

    # Получаем фильтры по количественным данным. Принцип создания селекторов такой же как и в типе field, поэтому используем функцию get_field_filters
    filters_by_counts_datas = get_field_filters(get_model_name(class_name), filters[1], current_url, request)

    l = list(request.GET)
    dict = {}
    for i in range(0, len(l)):
        if l[i] != 'section' and l[i] != 'sub_section':
            if request.GET[l[i]] != 'Все значения' and '_range' not in l[i]:
               dict[filter_MySQL_field(l[i])] = request.GET[l[i]]
            if '_rangestart' in l[i] and request.GET[l[i]] != 'Все значения':
               dict[filter_MySQL_field(l[i]) + '__range'] = (filter_MySQL_field(request.GET[l[i]]), get_max_value_on_field(get_model_name(class_name),l[i],'max',request))
            if '_rangeend' in l[i] and request.GET[l[i]] != 'Все значения':
               dict[filter_MySQL_field(l[i]) + '__range'] = (get_max_value_on_field(get_model_name(class_name),l[i],'min',request), filter_MySQL_field(request.GET[l[i]]))
    # Запрос к базе данных
    table_data = get_model_name(class_name).objects.filter(**dict)
    # Обращаемся к функции получения данных и получаем в ответ двумерный массив
    data = get_table_data(table_structure, table_data)

    return render(request, 'interface/table_view.html', {


        'filter_fields_labels': filters_by_fields_labels,
        'filters_by_counts_datas': filters_by_counts_datas,
        'off_words': off_words,
        'dict': dict,
        # 'filter_fields_datas': filters_by_fields_datas,
        # Раздел
        'section': section,
        'section_id': section_id,
        'url': current_url,
        # 'parse': parse,

        # 'indexes': indexes,
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
        t = type(file)
        # Тут хранится файл
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

        # Если заголовки базы не совпадают с теми, которые загрузил юзер - заг ружен неверный файл
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
                    log = 'В строке ' + str(i + 2) + 'файла Excel найдена ошибка в наименовании страны. Исправьте её и повторите импорт снова.'
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