from django.urls import path
from . import views

urlpatterns = [
    path('', views.header),
    path('blocks', views.blocks),
    path('analisys', views.analisys),
    path('events', views.events),
    path('reports', views.reports),
    path('table', views.table_list),
    path('table_view', views.table_view),
]
