from django.db import models


# Create your models here.
# class User(models.Model):
#     department = models.TextField('Организация', max_length=1000)
#     login = models.TextField('Логин', max_length=1000)
#     last_access = models.TextField('Активность', max_length=1000)
#
#     def __str__(self):
#         return self.department


class Sections(models.Model):
    param_name      = models.TextField('Имя таблицы', max_length=1000)
    interface_name  = models.TextField('Пользовательское имя раздела', max_length=1000)
    description     = models.TextField('Описание', max_length=1000)
    include         = models.IntegerField('Статус', max_length=1000)

    def __str__(self):
        return self.interface_name

    class Meta:
        verbose_name = 'Структура разделов'
        verbose_name_plural = 'Структура разделов'

class Sub_sections(models.Model):
    section_id      = models.TextField('Номер раздела', max_length=1000)
    param_name      = models.TextField('Имя таблицы', max_length=1000)
    interface_name  = models.TextField('Пользовательское имя таблицы', max_length=1000)
    description     = models.TextField('Описание', max_length=1000)
    include         = models.IntegerField('Статус', max_length=1000)

    def __str__(self):
        return self.interface_name

    class Meta:
        verbose_name = 'Структура подразделов'
        verbose_name_plural = 'Структура подразделов'

class Subsections_data(models.Model):
    section_id              = models.TextField('Номер раздела', max_length=1000)
    subsection_id           = models.TextField('Номер подраздела', max_length=1000)
    html_form_data_type     = models.TextField('Тип данных HTML-формы для ввода записи', max_length=1000)
    sql_field_data_type     = models.TextField('Тип данных для поля таблицы БД', max_length=1000)
    html_descriptor         = models.TextField('Метка HTML-формы для ввода записи', max_length=1000)
    sql_field_name          = models.TextField('Имя поля таблицы БД', max_length=1000)
    required                = models.TextField('Обязательность заполнения', max_length=1000)

    def __str__(self):
        return self.html_form_data_type

    class Meta:
        verbose_name = 'Структура таблиц'
        verbose_name_plural = 'Структура таблиц'
