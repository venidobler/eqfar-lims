from django.urls import path
from . import views

urlpatterns = [
    # Ex: /laboratory/
    path('', views.analysis_list, name='analysis_list'),
    
    # Ex: /laboratory/nova-analise/
    path('nova/', views.analysis_create, name='analysis_create'),

    # Nova Rota: Detalhes da Análise (ex: /laboratorio/1/)
    path('<int:pk>/', views.analysis_detail, name='analysis_detail'),

    # Nova rota: Adicionar Reserva na Análise X
    path('<int:analysis_id>/reservar/', views.add_booking, name='add_booking'),

    # Nova rota: Adicionar Insumo na Análise X
    path('<int:analysis_id>/insumo/', views.add_consumable, name='add_consumable'),

    # Nova rota para o dashboard
    path('dashboard/', views.dashboard, name='dashboard'), 
]