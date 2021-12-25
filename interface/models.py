from django.db import models


class Sections(models.Model):
    param_name = models.TextField('Имя таблицы', max_length=1000)
    interface_name = models.TextField('Пользовательское имя раздела', max_length=1000)
    description = models.TextField('Описание', max_length=1000)
    include = models.IntegerField('Статус', max_length=1000)

    def __str__(self):
        return self.interface_name

    class Meta:
        verbose_name = 'Структура разделов'
        verbose_name_plural = 'Структура разделов'

class Sub_sections(models.Model):
    section_id = models.TextField('Номер раздела', max_length=1000)
    param_name = models.TextField('Имя таблицы', max_length=1000)
    interface_name = models.TextField('Пользовательское имя таблицы', max_length=1000)
    description = models.TextField('Описание', max_length=1000)
    include = models.IntegerField('Статус', max_length=1000)

    def __str__(self):
        return self.interface_name

    class Meta:
        verbose_name = 'Структура подразделов'
        verbose_name_plural = 'Структура подразделов'

class Subsections_data(models.Model):
    section_id = models.TextField('Номер раздела', max_length=1000)
    subsection_id = models.TextField('Номер подраздела', max_length=1000)
    html_form_data_type = models.TextField('Тип данных HTML-формы для ввода записи', max_length=1000)
    sql_field_data_type = models.TextField('Тип данных для поля таблицы БД', max_length=1000)
    html_descriptor = models.TextField('Метка HTML-формы для ввода записи', max_length=1000)
    sql_field_name = models.TextField('Имя поля таблицы БД', max_length=1000)
    required = models.TextField('Обязательность заполнения', max_length=1000)

    def __str__(self):
        return self.html_form_data_type

    class Meta:
        verbose_name = 'Структура таблиц'
        verbose_name_plural = 'Структура таблиц'

class TableAus(models.Model):
    country = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    student_count = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    year_load = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    author = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    is_delete = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'table_aus'
        verbose_name = 'Иностранные слушатели'
        verbose_name_plural = 'Иностранные слушатели'


class TableCultDoc(models.Model):
    country = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    contr_agent = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    timestamp_agree_start = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    timestamp_agree_stop = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    agree_subject = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    status = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    year_load = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    author = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    is_delete = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'table_cult_doc'
        verbose_name = 'Культура_договора и соглашения'
        verbose_name_plural = 'Культура_договора и соглашения'

class TableCultEvent(models.Model):
    event_name = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    event_target = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    timestamp_event_start = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    timestamp_event_stop = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    participant_count = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    event_location = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    results = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    status = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    year_load = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    author = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    is_delete = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'table_cult_event'
        verbose_name = 'Культурные мероприятия'
        verbose_name_plural = 'Культурные мероприятия'


class TableEcDocument(models.Model):
    event_name = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    event_target = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    timestamp_event_start = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    timestamp_event_stop = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    participant_count = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    event_location = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    year_load = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    author = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    is_delete = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'table_ec_document'
        verbose_name = 'Экономические договора и соглашения'
        verbose_name_plural = 'Экономические договора и соглашения'


class TableEcEvents(models.Model):
    event_name = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    event_target = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    timestamp_event_start = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    timestamp_event_stop = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    participant_count = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    event_location = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    results = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    status = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    year_load = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    author = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    is_delete = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'table_ec_events'
        verbose_name = 'Экономические мероприятия'
        verbose_name_plural = 'Экономические мероприятия'


class TableGrants(models.Model):
    fund_name = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    grant_name = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    country = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    timestamp_grant_start = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    timestamp_grant_stop = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    year_load = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    author = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    is_delete = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'table_grants'
        verbose_name = 'Гранты_образование'
        verbose_name_plural = 'Гранты_образование'


class TableGuberDocLinks(models.Model):
    belgorod_contr_agent = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    inside_contr_agent = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    agree_name = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    timestamp_agree_start = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    timestamp_agree_stop = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    agree_location = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    year_load = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    author = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    is_delete = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'table_guber_doc_links'
        verbose_name = 'Договора и соглашения Администрации Губернатора Белгородской области'
        verbose_name_plural = 'Договора и соглашения Администрации Губернатора Белгородской области'


class TableGuberInternational(models.Model):
    subject_name = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    siders_guber_agree = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    registr_minust = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    year_load = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    author = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    is_delete = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'table_guber_international'
        verbose_name = 'Международные договора Администрации Губернатора Белгородской области'
        verbose_name_plural = 'Международные договора Администрации Губернатора Белгородской области'


class TableInternational(models.Model):
    event_name = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    timestamp_event_start = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    timestamp_event_stop = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    participant_count = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    results = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    year_load = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    author = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    is_delete = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'table_international'
        verbose_name = 'Международные мероприятия'
        verbose_name_plural = 'Международные мероприятия'


class TableInternationalDocument(models.Model):
    country = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    contr_agent = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    timestamp_agree_start = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    timestamp_agree_stop = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    agree_subject = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    year_load = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    author = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    is_delete = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'table_international_document'
        verbose_name = 'Международные договора и соглашения'
        verbose_name_plural = 'Международные договора и соглашения'


class TableMobile(models.Model):
    country = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    mobile_name = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    year_load = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    author = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    is_delete = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'table_mobile'
        verbose_name = 'Программы мобильности'
        verbose_name_plural = 'Программы мобильности'


class TableOch(models.Model):
    country = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    higher_education = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    mean_education = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    graduate_students = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    first_course = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    excepted = models.TextField(db_column='excepted', db_collation='utf8_general_ci', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    year_load = models.TextField(db_column='year_load', db_collation='utf8_general_ci', blank=True, null=True)
    author = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    is_delete = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'table_och'
        verbose_name = 'Очная форма обучения'
        verbose_name_plural = 'Очная форма обучения'


class TableSportDoc(models.Model):
    country = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    contr_agent = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    timestamp_agree_start = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    timestamp_agree_stop = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    agree_subject = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    status = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    year_load = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    author = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    is_delete = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'table_sport_doc'
        verbose_name = 'Документы спорт'
        verbose_name_plural = 'Документы спорт'


class TableSportInter(models.Model):
    event_name = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    event_target = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    timestamp_event_start = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    timestamp_event_stop = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    participant_count = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    event_location = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    results = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    status = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    year_load = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    author = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    is_delete = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'table_sport_inter'
        verbose_name = 'Мероприятия спорт'
        verbose_name_plural = 'Мероприятия спорт'


class TableStudentChange(models.Model):
    country = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    partner = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    timestamp_practice_start = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    timestamp_practice_stop = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    year_load = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    author = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    is_delete = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'table_student_change'
        verbose_name = 'Обмен студентами'
        verbose_name_plural = 'Обмен студентами'


class TableWork(models.Model):
    municipal_district = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    citizenship = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    field_of_activity = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    employee_count = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    year_load = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    author = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    is_delete = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'table_work'
        verbose_name = 'Информация о труде и занятости'
        verbose_name_plural = 'Информация о труде и занятости'


class TableYoung(models.Model):
    event_name = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    event_target = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    timestamp_event_start = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    timestamp_event_stop = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    participant_count = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    event_location = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    results = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    status = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    year_load = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    author = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    is_delete = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'table_young'
        verbose_name = 'Мероприятия молодёжной политики'
        verbose_name_plural = 'Мероприятия молодёжной политики'


class TableZaoch(models.Model):
    country = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    higher_education = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    mean_education = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    graduate_students = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    first_course = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    excepted = models.TextField(db_column='excepted', db_collation='utf8_general_ci', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    year_load = models.TextField(db_column='year_load', db_collation='utf8_general_ci', blank=True, null=True)
    author = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    is_delete = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'table_zaoch'
        verbose_name = 'Заочная форма обучения'
        verbose_name_plural = 'Заочная форма обучения'

class RefCountry(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)
    fullname = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ref_country'