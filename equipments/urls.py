from django.urls import path
from . import views

urlpatterns = [
    # A Home (lista) e o Detalhe
    path('', views.list_equipments, name='equipment_list'),
    path('novo/', views.EquipmentCreateView.as_view(), name='equipment_create'),
    path('<int:id>/', views.equipment_detail, name='equipment_detail'),
]