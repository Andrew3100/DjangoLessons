from django.http import HttpRequest
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User, UserModel
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import render
from django import forms
from .models import *
import requests
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from django.urls import resolve
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django import *
import urllib.parse
import pandas
import time as t


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
    if len(array) == 0:
        return False
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
    if 'event' in url:
        sect_id = 8
        subsect_id = 19
    else:
        subsect_id = request.GET['section']
        sect_id = request.GET['sub_section']
    for i in range(0, len(array)):
        label = Subsections_data.objects.filter(section_id = subsect_id, subsection_id = sect_id, sql_field_name = array[i])
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
    if string == 'DjangoLogs':
        return DjangoLogs


# Функция формирует двумерный массив данных
def get_table_data(table_structure, table_data, section_id, subsection_id, request):
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
            # Метод, позволяющий передать совйство объекта в виде строки
            if table_structure1.html_form_data_type == 'date':
                data.append(get_date_from_timestamp(str(table_data1.__getattribute__(table_structure1.sql_field_name))))
            else:
                data.append(table_data1.__getattribute__(table_structure1.sql_field_name))

        if table_data1.author == request.user.first_name:
            auth_label = '_isauth'
        else:
            auth_label = ''

        id = str(table_data1.id) + '_id' + auth_label
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


# Функция перехватывает ошибку авторизации


# Create your views here.
def header(request):
    try:
        username = request.user.first_name
    except AttributeError:
        username = None
        return render(request, 'interface/header/redirect.html')
    return render(request, 'interface/header/header.html', {
        'username': request.user.first_name,
    })

def blocks(request):
    try:
        username = request.user.first_name
    except AttributeError:
        username = None
        return render(request, 'interface/header/redirect.html')
    sections = Sections.objects.filter(id__in=get_access_block_list(request.user.id))
    message = ''
    if get_access_block_list(request.user.id) == []:
        message = 'Для Вас не найдено доступных разделов. Для получения прав доступа обратитесь к администратору информационной системы'

    return render(request, 'interface/blocks.html',
                  {
                      'sections': sections,
                      'message': message,
                      'username': request.user.first_name
                  }
                  )

def analisys(request):
    import matplotlib.pyplot as plt
    import numpy as np
    try:
        username = request.user.first_name
    except AttributeError:
        username = None
        return render(request, 'interface/header/redirect.html')
    # Только суперадминам
    # if request.user.is_superuser != 1:
    #     return render(request, 'interface/access_error.html')
    x = np.arange(0, 15, 0.00001)
    y = np.sin(x)

    plt.plot(x, y)
    # plt.show()
    plt.savefig('interface/matplotlib/saved_figure.jpg')

    return render(request, 'interface/analisys.html',{
        'username': request.user.first_name
    })


def get_user_attr(attr_name,id):
    user_attr = User.objects.get(pk=id)
    attr = user_attr.__getattribute__(attr_name)
    return attr


def get_block_name_by_block_id(block_id,request):
    block_name = Sections.objects.filter(id=block_id)
    for bl_name in block_name:
        return bl_name.interface_name


# Доступен ли пользователю текущий блок
def this_block_access_for_user(request, user_id, block_idd):
    access = AccessBlock.objects.filter(user_id=user_id,is_access=1,block_id=block_idd)
    # return access
    ids = []
    for a in access:
        ids.append(int(a.block_id))
    if block_idd in ids:
        return True
    else:
        return False


# Возвращает массив блоков, доступных авторизованному пользователю
def get_access_block_list(user_id):
    ids = []
    access = AccessBlock.objects.filter(user_id=user_id,is_access=1)
    for a in access:
        ids.append(a.block_id)
    return ids



def access(request):
    try:
        username = request.user.first_name
    except AttributeError:
        username = None
        return render(request, 'interface/header/redirect.html')
    current_url = request.get_full_path_info()
    user_list = User.objects.filter(is_active=1)
    user_name_list = []
    user_name_id = []
    user_datas ={}
    for list in user_list:
        user_datas[list.first_name] = list.id
    dict_status = {
        '1': 'Доступно',
        '0': 'Недоступно'
    }

    if is_get_param_in_this_url(current_url,'block_name_for_close_open'):
        block = Sections.objects.filter(interface_name=request.GET['block_name_for_close_open'])
        for b in block:
            block_id = b.id
        access_id = AccessBlock.objects.filter(user_id=request.GET['user_id'],block_id=block_id)
        for a_id in access_id:
            acc_id = a_id.id
        if request.GET['access_status'] == 'Недоступно':
            label = 1
        else:
            label = 0
        re_assign = AccessBlock.objects.filter(id=acc_id).update(is_access=label)


    access = ''
    access_list = ''
    # Если в селекторе выбран пользователь - выводим таблицу с его правами доступа
    if request.GET['user_id'] != 'all':
        access_list_username = get_user_attr('first_name', request.GET['user_id'])
        access = AccessBlock.objects.filter(user_id=request.GET['user_id'])
        access_list = {}
        access_block = []
        access_status = []
        access_block_dict = {}
        firstname = get_user_attr('first_name',request.GET['user_id'])
        for acc in access:
            access_block_dict[get_block_name_by_block_id(acc.block_id,request)] = dict_status[str(acc.is_access)]
        access_list[firstname] = access_block_dict
    else:
        access_list_username = 'Выберите пользователя для просмотра и редактирования прав доступа'
    return render(request, 'interface/access.html', {
        'username': username,
        'user_datas': user_datas,
        'access': access,
        'access_list': access_list,
        'user_id': request.GET['user_id'],
        'access_list_username': access_list_username
    })


def sync_access(request):
    try:
        username = request.user.first_name
    except AttributeError:
        username = None
        return render(request, 'interface/header/redirect.html')

    user_id_array = []
    user_id_array_in_access = []
    scan_users = User.objects.filter(is_active=1)
    # собираем иды всех пользователей
    for s_u in scan_users:
        user_id_array.append((s_u.id))
    # собираем иды всех пользователей, данные о правах которых есть в таблице прав доступа
    scan_users_access = AccessBlock.objects.all()
    for s_u_a in scan_users_access:
        user_id_array_in_access.append((s_u_a.user_id))
    user_id_array_in_access = list(set(user_id_array_in_access))
    new_user_list = []
    for k in user_id_array:
        if k not in user_id_array_in_access:
            new_user_list.append(k)

    block_list = Sections.objects.filter(include=1)
    blocks = []
    for b in block_list:
        blocks.append(b.id)
    New_access_value = {}
    for new in new_user_list:
        New_access_value = {}
        for b_l in blocks:
            New_access_value['user_id'] = new
            New_access_value['block_id'] = b_l
            New_access_value['is_access'] = 0
            AccessBlock(**New_access_value).save()

    return render(request, 'interface/sync_message.html', {
        'new_user_list': new_user_list
    })

def events(request):
    try:
        username = request.user.first_name
    except AttributeError:
        username = None
        return render(request, 'interface/header/redirect.html')
    if request.user.is_superuser != 1:
        return render(request, 'interface/access_error.html')
    data = DjangoLogs.objects.all()
    table_structure = Subsections_data.objects.filter(section_id=8, subsection_id=19)
    headers = []
    for ts in table_structure:
        headers.append(ts.html_descriptor)

    data = get_table_data(table_structure, data, 8, 19, request)
    for dd in data:
        # Удаляем ИД лога
        del dd[len(dd)-1]
        # Переводим крайний элемент из таймстампа в дату
        dd[len(dd) - 1] = get_date_from_timestamp(dd[len(dd)-1],'%d-%m-%Y, %H:%I:%S')
    filters = get_filters_data(DjangoLogs, 8, 19)
    filters = get_a_set_of_filters(filters)
    # Получаем фильтры по полям
    filters_by_fields_labels = get_field_filters(DjangoLogs, filters[0], request.get_full_path_info(), request)

    return render(request, 'interface/events.html', {
        'headers': headers,
        'data': data,
        'filters_by_fields_labels': filters_by_fields_labels,
        'username': request.user.first_name
    })


def reports(request):
    try:
        username = request.user.first_name
    except AttributeError:
        username = None
        return render(request, 'interface/header/redirect.html')
    return render(request, 'interface/reports.html', {
        'username': request.user.first_name
    })

def login(request):
    return render(request, 'interface/login.html')

def delete_record(request,model,id):
    # delete_id
    return render(request, 'interface/delete.html')


def table_list(request):

    subsections = Sub_sections.objects.all()
    sections = Sections.objects.all()
    url = request.GET['block']
    if int(url) not in get_access_block_list(request.user.id):
        return render(request, 'interface/access_error.html')

    return render(request, 'interface/table_list.html',
                  {
                      'sub': subsections,
                      'seс': sections,
                      'username': request.user.first_name,
                      'url': int(url),
                      'url1': url
                  }
                  )


# Вставка лога по имени события
def insert_log(event,model,request,section,subsection):
    t_n = Sub_sections.objects.filter(section_id=section,id=subsection)
    for tt in t_n:
        table_name = tt.interface_name
    log_dict = {}
    log_dict['timestamp_label'] = str(int(t.time()))
    log_dict['author'] = request.user.first_name
    log_dict['event'] = event
    log_dict['is_delete'] = 0
    log_dict['table'] = table_name
    save = DjangoLogs(**log_dict).save()
    return save

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
            if table_structure1.html_form_data_type == 'date':
                posts_names_dict[table_structure1.sql_field_name] = get_timestamp_from_date(str(request.POST[table_structure1.sql_field_name]))
            else:
                posts_names_dict[table_structure1.sql_field_name] = request.POST[table_structure1.sql_field_name]

    posts_names_dict['year_load'] = 2020;
    posts_names_dict['author'] = request.user.first_name;
    posts_names_dict['is_delete'] = 0;
    # Формируем имя создаваемого экземпляра
    class_name = get_class_name_by_section_subsection(sub_section)
    # Аргумент с двумя звёздочками - распаковка словаря обрабатываесых данных
    # За счёт него можно передавать сколько угодно значений, а не фиксированное количество
    save = get_model_name(class_name)(**posts_names_dict).save()
    log = insert_log('Вставка записи ', class_name,request,request.GET['section'],request.GET['sub_section'])
    # Текст урл для редиректа
    new_url = '/table_view?section=' + str(request.GET['section']) + '&sub_section=' + str(request.GET['sub_section'])

    return render(request, 'interface/add.html', {
        'url': new_url,
        # 'log': log
    })


# Загружает файл из папки сохранённых отчётов
def load_file(path, request, filename,label):
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
    response['Content-Disposition'] = "attachment; filename=Report.xlsx"
    return response


def get_min_or_max(param,field,model):
    datas = model.objects.filter(is_delete=0)
    maxs = []
    if len(datas) == 0:
        return False
    for data in datas:
        maxs.append(int(data.__getattribute__(field)))
    if param == 'min':
        return min(list(set(maxs)))
        # return datas
    else:
        return max(list(set(maxs)))
        # return datas

def excel_report(request):

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
        if headers[i] in ['Дата начала','Дата окончания','Дата начала практики','Дата окончания практики','Начало реализации','Окончание реализации','Дата Заключения','Срок действия','Дата заключения договора']:
            times = []
            for dick in data_full[i]:
                times.append(get_date_from_timestamp(int(dick)))
            if is_get_param_in_this_url(current_url,'template'):
                clear(times)
            dictionary[headers[i]] = times
        else:
            if is_get_param_in_this_url(current_url,'template'):
                clear(data_full[i])
            dictionary[headers[i]] = data_full[i]

    pandas_DF = pandas.DataFrame(dictionary)
    time_label_filename = str(int(t.time())) +'_'+ str(request.user.first_name)
    save_path = 'interface/reports/'+str(time_label_filename)+'.xlsx'
    pandas_DF.to_excel(save_path,sheet_name=get_table_name(sub_section_id), index=False)
    writer = pd.ExcelWriter('test_file.xlsx')
    pandas_DF.to_excel(writer, sheet_name='myanalysis', index=False, na_rep='NaN')
    log = insert_log('Загрузка отчёта', classname, request, section_id, sub_section_id)
    return load_file(save_path, request, get_table_name(sub_section_id),time_label_filename)


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
    log = insert_log('Удаление записи с идентификатором ' + str(record_delete_id[0]),request.GET['model'],request,section_id,sub_section_id)
    return render(request, 'interface/delete.html', {
        'subsection_id': sub_section_id,
        'section_id': section_id
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
        data = get_table_data(table_structure, edit, section_id, sub_section_id,request)
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
        insert_log('Редактирование записи с идентификатором '+str(record_delete_id[0]),request.GET['model'],request,section_id,sub_section_id)
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


def get_format_date(request, filters):
    current_url = (request.get_full_path_info())
    date1_value = ''
    date2_value = ''
    if filters[2] != []:
        if is_get_param_in_this_url(current_url, filters[2][0] + '__range'):
            date1_value = get_date_from_timestamp(request.GET[filters[2][0] + '__range'].split('-')[0])
            date1_value_array = date1_value.split('-')
            date1_value = date1_value_array[2] + '-' + date1_value_array[1] + '-' + date1_value_array[0]

        if is_get_param_in_this_url(current_url, filters[2][1] + '__range'):
            date2_value = get_date_from_timestamp(request.GET[filters[2][1] + '__range'].split('-')[1])
            date2_value_array = date2_value.split('-')
            date2_value = date2_value_array[2] + '-' + date2_value_array[1] + '-' + date2_value_array[0]
        return date1_value, date2_value
    else:
        return False

def get_date_from_timestamp(timestamp,format='%d-%m-%Y'):
    from datetime import datetime
    # Прибавили сутки в секундах, так как почему-то библиотека datetime отнимает сутки от метки timestamp
    date = datetime.utcfromtimestamp(int(timestamp)+86400).strftime(format)
    return date

def get_timestamp_from_date(date):
    from dateutil import parser
    timestamp = parser.parse(date).timestamp()
    return int(timestamp)




def table_view(request):
    # Редирект, на случай если кто-то додумается до очистки куков
    try:
        username = request.user.first_name
    except AttributeError:
        username = None
        return render(request, 'interface/header/redirect.html')
    # Достаём имя раздела по идентификатору, указанному в GET параметре
    section_id = request.GET['section']
    sub_section_id = request.GET['sub_section']
    sub_section_id = request.GET['sub_section']
    section = Sections.objects.filter(id=request.GET['section'])
    # Проверка доступа к блоку чтобы не наебали по GET-параметрам
    if this_block_access_for_user(request, request.user.id, int(section_id)) == False:
        return render(request, 'interface/access_error.html')

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
    # 2 - даты
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
    if len(table_data) == 0:
        count = 0
    else:
        count = 1
    # Обращаемся к функции получения данных и получаем в ответ двумерный массив
    data = get_table_data(table_structure, table_data, section_id, sub_section_id,request)
    dict_val = list(dict.values())
    dict_keys = list(dict.keys())

    current_user = request.user
    dates_value_for_HTML_form = get_format_date(request,filters)
    if dates_value_for_HTML_form == False:
        dates1 = ''
        dates2 = ''
    else:
        dates1 = dates_value_for_HTML_form[0]
        dates2 = dates_value_for_HTML_form[1]

    min_max_dates_array = []
    if len(filters[2]) > 0 and get_min_or_max('max',filters[2][0],get_model_name(class_name)) != False:
        min_max_dates_array.append(get_min_or_max('max',filters[2][0],get_model_name(class_name)))
        min_max_dates_array.append(get_min_or_max('max',filters[2][1],get_model_name(class_name)))
        min_max_dates_array.append(get_min_or_max('min',filters[2][0],get_model_name(class_name)))
        min_max_dates_array.append(get_min_or_max('min',filters[2][1],get_model_name(class_name)))
    if len(min_max_dates_array) > 0:
        dates_isset = 1
    else:
        dates_isset = 0
    current_url_broken = current_url.split('&')
    del current_url_broken[0]
    del current_url_broken[0]
    current_url_brokenn = '&'.join(current_url_broken)


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
        'filters_dates': min_max_dates_array,
        'filters_dates1': filters[2],
        'model': class_name,
        'username': current_user.first_name,
        'date1_value': dates1,
        'date2_value': dates2,
        # Метка для вывода диапазона дат
        'dates_isset': dates_isset,
        # Метка наличия записей
        'count': count,
        # 'sql': sql,
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
            insert_log('Несопоставимый файл',get_class_name_by_section_subsection(sub_section),request,section_id,sub_section_id)
            return log_message

        lens = GetCountriesList(request)

        # Массив словарей для записи
        array_dicts = []
        for i in range(0,len(file)):
            if 'Страна прибытия' in database_headers:
                country = file['Страна прибытия'][i]
                if country not in list(lens.keys()):
                    log = 'В строке ' + str(i + 2) + 'файла Excel найдена ошибка в наименовании страны. Исправьте её и повторите импорт снова.'
                    insert_log('Ошибка в наименовании страны', get_class_name_by_section_subsection(sub_section), request,
                               section_id, sub_section_id)
                    return log
            # Словарь для записи
            dict_save = {}
            for data in datas:
                if data.html_descriptor != 'Автор' and data.html_descriptor != 'Год':
                    # Если попадается поле с датой
                    if data.html_form_data_type == 'date':
                        # переводим дату в таймстамп
                        dict_save[data.sql_field_name] = get_timestamp_from_date(str(file[data.html_descriptor][i]))
                    else:
                        dict_save[data.sql_field_name] = file[data.html_descriptor][i]
            dict_save['year_load'] = 2020
            dict_save['author'] = request.user.first_name
            dict_save['is_delete'] = 0
            array_dicts.append(dict_save)

        model = get_model_name(get_class_name_by_section_subsection(sub_section))

        # Перебор созданного словаря
        for dict in array_dicts:
            # Вставка словаря при помощи распаковки словаря аргументов **kwargs. Документация
            model(**dict).save()
        log = "Импорт записей произведён успешно"
        insert_log('Успешный импорт', get_class_name_by_section_subsection(sub_section), request, section_id,
                   sub_section_id)
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