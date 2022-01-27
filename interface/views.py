from django.http import HttpRequest
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import render
from django import forms
from .models import *
import requests
import pandas as pd
import matplotlib.pyplot as plt
from django.urls import resolve
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django import *
import urllib.parse


def urlencode(str):
  return urllib.parse.quote(str)


def urldecode(str):
  return urllib.parse.unquote(str)

# Возврашает интерфейсное имя таблицы по разделу и подразделу
def get_table_name(subsection):
    data = Sub_sections.objects.filter(id=subsection)
    for dat in data:
        name = dat.interface_name
    return name


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

# Возвращает тип фильтра фильтра строкой
def get_field_filter_type_name(filter,request):
    datas = Subsections_data.objects.filter(section_id=request.GET['section'], subsection_id=request.GET['sub_section'], filter_type=filter)
    for data in datas:
        d = data.filter_type
    return d

# Функция достаёт данные по фильтрам таблицы
def get_filters_data(class_name, section, subsection):
    filters_data = Subsections_data.objects.filter(section_id = section, subsection_id = subsection)
    dict = {}
    for f_d in filters_data:
        dict[f_d.sql_field_name] = f_d.filter_type
    return dict

# Функция создана для того, чтобы вернуть нужное число диапазона при отборе записей в базе данных
def get_max_value_on_field(model,field,param,request):
    if is_get_param_in_this_url(request.get_full_path_info(), filter_MySQL_field(field)+'___rangestart') == True and '___rangeend' in field == True:
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
    f = field.split('__')
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
            if is_get_param_in_this_url(url, l.sql_field_name):
                arr.append(request.GET[l.sql_field_name])
            else:
                arr.append('Выберите значение')
        datas = model.objects.filter(is_delete=0)
        for data in datas:
            if data.__getattribute__(array[i]) not in arr:
                arr.append(data.__getattribute__(array[i]))

        arr1.append((list((arr))))
    return arr1

def get_count_filters(model, array, url, request):
    arr1 = []
    for i in range(0, len(array)):
        label = Subsections_data.objects.filter(section_id=request.GET['section'],
                                                subsection_id=request.GET['sub_section'], sql_field_name=array[i])
        arr = []
        # Имя метки:
        for l in label:
            arr.append(l.html_descriptor)
            arr.append(l.sql_field_name)
            if is_get_param_in_this_url(url, l.sql_field_name+'__range'):
                arr.append(request.GET[l.sql_field_name+'__range'])
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
def get_table_data(table_structure, table_data, section_id, subsection_id):
    # Главный массив данных
    full_data = []
    ids = []
    for table_data1 in table_data:
        # Подчинённый массив данных
        data = []
        # Перебираем структуру таблицы и пытаемся сунуть элементы в свойства объекта.
        # Благодаря этому можно не делать милиарды лишних шаблонов
        ids.append(table_data1.id)
        for table_structure1 in table_structure:
            # Костыль, позволяющий передать совйство объекта в виде строки
            data.append(table_data1.__getattribute__(table_structure1.sql_field_name))
        id = str(table_data1.id) + '_id'
        data.append(id)
        section_id_str = str(section_id)
        subsection_id_str = str(subsection_id)
        id = str(table_data1.id)
        # data.append(table_data1.id)
        full_data.append(data)
        del data
    return full_data

def get_dict_by_GET(request, list_GET):
    dict = {}
    for i in range(0, len(list_GET)):
        if l[i] != 'section' and l[i] != 'sub_section':
            # Блок условий проверяет, есть ли необходимость добавить ранжирование параметра (для количественных данных)
            if request.GET[l[i]] != 'Всё' and '_range' not in l[i]:
                dict[filter_MySQL_field(l[i])] = request.GET[l[i]]
            if '_rangestart' in l[i] and request.GET[l[i]] != 'Всё':
                dict[filter_MySQL_field(l[i]) + '__range'] = (filter_MySQL_field(request.GET[l[i]]),
                                                              get_max_value_on_field(get_model_name(class_name), l[i],
                                                                                     'max', request))
            if '_rangeend' in l[i] and request.GET[l[i]] != 'Всё':
                dict[filter_MySQL_field(l[i]) + '__range'] = (
                get_max_value_on_field(get_model_name(class_name), l[i], 'min', request),
                filter_MySQL_field(request.GET[l[i]]))
    return list_GET

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

def login(request):
    return render(request, 'interface/login.html')

def delete_record(request,model,id):
    # delete_id
    return render(request, 'interface/delete.html')


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


# Загружает файл из папки сохранённых отчётов
def load_file(path, request, filename):
    import xlwt
    import mimetypes
    import os

    fp = open(path, "rb")
    response = HttpResponse(fp.read())
    fp.close()

    file_type = mimetypes.guess_type(path)
    if file_type is None:
        file_type = 'application/octet-stream'
    response['Content-Type'] = file_type
    response['Content-Length'] = str(os.stat(path).st_size)
    response['Content-Disposition'] = "attachment; filename=report.xlsx"
    return response



# Проверяет является ли поле количественным и получает для него диапазон
def get_filter_diapason(field, model, url, request):
    start = 0
    end = 0

    parse_url = url.split('&')
    del parse_url[0]
    del parse_url[0]

    for i in range(0, len(parse_url)):
        datas = parse_url[i].split('=')

        # Запрос на проверку типа фильтра поля
        is_count = Subsections_data.objects.filter(section_id = request.POST['s'],subsection_id = request.POST['ss'],sql_field_name=filter_MySQL_field(field))
        for is_counted in is_count:
            # Если поле не количественное, то получаем диапазон количественных данных
            if is_counted.filter_type != 'count':
                return False
            else:
                if is_get_param_in_this_url(url, field):
                    if '___rangestart' in datas[0]:
                        start = datas[1]
                    if '___rangeend' in datas[0]:
                        end = datas[1]
    return start,end


def GET_dictionary(url):
    dict = {}
    parse = url.split('&')
    for par in parse:
        parss = par.split('=')
        if 'section' not in parss[0]:
            dict[parss[0]] = urldecode(parss[1])
    return dict

def get_min_or_max(param,field,model):
    datas = model.objects.filter(is_delete=0)
    maxs = []
    for data in datas:
        maxs.append(int(data.__getattribute__(field)))
    if param == 'min':
        return min(list(set(maxs)))
    else:
        return max(list(set(maxs)))


def merge_range_data(dictionary, model):
    vals = list(dictionary.values())
    keys = list(dictionary.keys())
    dict = {}
    starts = {}
    ends = {}
    for i in range(0, len(keys)):
        if '___range' in keys[i]:
            if '___rangestart' in keys[i]:
                if (vals[i]) == 'Всё' or 'Все значения':
                    starts[filter_MySQL_field(keys[i])] = get_min_or_max('min',filter_MySQL_field(keys[i]),model) # взять минимальное по полю
                else:
                    starts[filter_MySQL_field(keys[i])] = vals[i]
            if '___rangeend' in keys[i]:
                if (vals[i]) == 'Всё' or 'Все значения':
                    ends[filter_MySQL_field(keys[i])] = str(get_min_or_max('max',filter_MySQL_field(keys[i]),model)) # взять максимальное по полю
                else:
                    ends[filter_MySQL_field(keys[i])] = str(vals[i])
        else:
            dict[keys[i]] = vals[i]
    keys = list(starts.keys())
    for i in range(0, len(keys)):
        dict[keys[i]+'__range'] = (starts[keys[i]], ends[keys[i]])
    # Словарь, готовый для распаковки
    return starts, ends


def excel_report(request):
    import pandas
    import time as t
    section_id = request.POST['s']
    sub_section_id = request.POST['ss']
    current_url = request.get_full_path_info()
    classname = get_class_name_by_section_subsection(sub_section=Sub_sections.objects.filter(id=sub_section_id))
    model = get_model_name(classname)
    post_array0 = list(request.POST)
    post_array1 = []
    # Из списка постов формируем список полей, забираемых в отчёт. Начало с двух, так как первые два элементы не нужны
    for i in range(2, len(post_array0)):
        post_array1.append((post_array0[i]))
    del post_array1[0]
    del post_array1[0]
    # Заголовки для датафрейма
    headers = []
    headers1 = Subsections_data.objects.filter(section_id=section_id, subsection_id=sub_section_id, sql_field_name__in=post_array1)
    for h in headers1:
        headers.append(h.html_descriptor)
    dict = get_dictionary(request, classname)

    data_full = []
    for post in post_array1:
        data = []
        datas = model.objects.filter(**dict)
        for dat in datas:
            data.append(dat.__getattribute__(post))
        data_full.append(data)

    dictionary = {}
    if is_get_param_in_this_url(current_url, 'template'):
        del data_full
    for i in range(0, len(headers)):
        # Тут датафрейм, из которого формируется Excel и сохраняестя на сервер
        dictionary[headers[i]] = data_full[i]
    pandas_DF = pandas.DataFrame(dictionary)
    time_label_filename = t.time()
    save_path = 'interface/reports/'+str(time_label_filename)+'.xlsx'
    pandas_DF.to_excel(save_path,sheet_name=get_table_name(sub_section_id), index=False)
    writer = pd.ExcelWriter('test_file.xlsx')
    pandas_DF.to_excel(writer, sheet_name='my_analysis', index=False, na_rep='NaN')

    return load_file(save_path, request, get_table_name(sub_section_id))


def get_diap(data,field,class_name):
    get_max = get_min_or_max('max', filter_MySQL_field(field), get_model_name(class_name))
    get_min = get_min_or_max('min', filter_MySQL_field(field), get_model_name(class_name))
    a = list(data)
    array = data.split('-')
    if array[1] == '':
        array[1] = get_max
    if array[0] == '':
        array[0] = get_min
    return array

def get_dictionary(request, class_name):
    l = list(request.GET)
    dict = {}
    diap = ''
    for i in range(0, len(l)):
        if l[i] != 'section' and l[i] != 'sub_section':
            if '__range' in l[i]:
                diap = get_diap(request.GET[l[i]], l[i], class_name)
                dict[l[i]] = diap
            else:
                dict[l[i]] = request.GET[l[i]]
    return dict


# Скрипт удаления записи обновляет поле is_delete на значение 1
def delete(request):
    section_id = request.GET['section_id']
    sub_section_id = request.GET['subsection_id']
    get_table_srtructure = Subsections_data.objects.filter(section_id=section_id,subsection_id=sub_section_id)
    record_delete_id = request.GET['record_delete'].split('_')
    delete = get_model_name(request.GET['model']).objects.filter(id=int(record_delete_id[0])).update(is_delete=1)
    return render(request, 'interface/delete.html', {
        'subsection_id': section_id,
        'section_id': sub_section_id
    })

def edit(request):
    section_id = request.GET['section_id']
    sub_section_id = request.GET['subsection_id']
    record_delete_id = request.GET['record_edit']
    current_url = request.get_full_path_info()
    edit = get_model_name(request.GET['model']).objects.filter(id=int(record_delete_id[0]))
    if is_get_param_in_this_url(current_url,'submitted') == False:
        table_structure = Subsections_data.objects.filter(section_id=section_id, subsection_id=sub_section_id)
        # двумерный массив данных

        dat_full = []
        data = get_table_data(table_structure, edit, section_id, sub_section_id)
        i = 0
        for t in table_structure:
            dat = []
            if t.html_descriptor != 'Автор' and t.html_descriptor != 'Год':
                dat.append(t.html_descriptor)
                dat.append(t.sql_field_name)
                dat.append(t.html_form_data_type)
                dat.append(data[0][i])
                i = i + 1
                dat_full.append(dat)
        return render(request, 'interface/edit.html', {
            'record_delete_id': record_delete_id,
            # 'table_structure': get_table_srtructure,
            'section_id': section_id,
            'sub_section_id': sub_section_id,
            'model': request.GET['model'],
            'values': dat_full,
        })
    else:
        dict = {}
        post_data = list(request.POST)
        del post_data[0]
        for post in post_data:
            dict[post] = request.POST[post]
            # dict[post1[0]] = post1[1]
        delete = get_model_name(request.GET['model']).objects.filter(id=int(record_delete_id[0])).update(**dict)
        return render(request, 'interface/edit.html', {
            'section': section_id,
            'sub_section_id': sub_section_id,
            'post': 'success'
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
        off_words.append('')
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
    # Получаем фильтры по количественным данным.
    filters_by_counts_datas = get_count_filters(get_model_name(class_name), filters[1], current_url, request)

    dict = get_dictionary(request, class_name)
    dict['is_delete'] = 0

    # Запрос к базе данных
    table_data = get_model_name(class_name).objects.filter(**dict)
    # Обращаемся к функции получения данных и получаем в ответ двумерный массив
    data = get_table_data(table_structure, table_data, section_id, sub_section_id)
    dict_val = list(dict.values())
    dict_keys = list(dict.keys())

    current_url_broken = current_url.split('&')
    del current_url_broken[0]
    del current_url_broken[0]
    current_url_brokenn = '&'.join(current_url_broken)
    edit = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil" viewBox="0 0 16 16"><path d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168l10-10zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207 11.207 2.5zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293l6.5-6.5zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325z"/></svg>'
    delete = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-archive-fill" viewBox="0 0 16 16"><path d="M12.643 15C13.979 15 15 13.845 15 12.5V5H1v7.5C1 13.845 2.021 15 3.357 15h9.286zM5.5 7h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1 0-1zM.8 1a.8.8 0 0 0-.8.8V3a.8.8 0 0 0 .8.8h14.4A.8.8 0 0 0 16 3V1.8a.8.8 0 0 0-.8-.8H.8z"/></svg>'
    return render(request, 'interface/table_view.html', {

        'filter_fields_labels': filters_by_fields_labels,
        'filters_by_counts_datas': filters_by_counts_datas,
        'off_words': off_words,
        'dict': dict_val,
        'dict1': dict_keys,
        # 'diap': diap,
        # 'filter_fields_datas': filters_by_fields_datas,
        # Раздел
        'section': section,
        'section_id': section_id,
        'url': current_url,
        'url1': current_url_brokenn,
        'arr1': filters[1],
        # 'parse': parse,
        # 'ids': data[1],
        # 'indexes': indexes,
        # Подраздел
        'sub_section': sub_section,
        'sub_section_id': sub_section_id,
        # Заголовки таблицы
        'table_structure': table_structure,
        # Двумерный массив содержимого
        'data': data,
        'model': class_name,
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



