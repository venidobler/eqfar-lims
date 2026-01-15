from django.urls import path
from . import views

urlpatterns = [
    # A Home (lista) e o Detalhe
    path('', views.list_equipments, name='home'),
    path('equipment/<int:id>/', views.equipment_detail, name='equipment_detail'),
]