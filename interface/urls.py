from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.header),
    path('blocks', views.blocks),
    path('analisys', views.analisys),
    path('events', views.events),
    path('reports', views.reports),
    path('table', views.table_list),
    path('table_view', views.table_view),
    path('add', views.add),
    path('excel', views.excel_report),
    path('delete', views.delete),
    path('edit', views.edit),
    path('access', views.access)
]