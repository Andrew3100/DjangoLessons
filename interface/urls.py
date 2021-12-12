from django.urls import path
from . import views

urlpatterns = [
    path('', views.header),
    path('blocks', views.blocks),
    # path('tables', views.tables),
    path('analisys', views.analisys),
    path('events', views.events),
    # path('new_block', views.new_block),
    path('reports', views.reports),
    path('table', views.table_list),
]
