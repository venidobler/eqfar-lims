from django.urls import path
from . import views

urlpatterns = [
    # A Home (lista) e o Detalhe
    path('', views.list_equipments, name='equipment_list'),
    path('<int:id>/', views.equipment_detail, name='equipment_detail'),
]