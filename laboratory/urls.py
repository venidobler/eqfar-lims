from django.urls import path
from . import views

urlpatterns = [
    # Nova rota para o dashboard
    path('', views.dashboard, name='dashboard'),

    # Ex: /laboratory/
    path('analises/', views.analysis_list, name='analysis_list'),
    
    # Ex: /laboratory/nova-analise/
    path('analises/nova/', views.analysis_create, name='analysis_create'),

    # Nova Rota: Detalhes da Análise (ex: /laboratorio/1/)
    path('analises/<int:pk>/', views.analysis_detail, name='analysis_detail'),

    # Nova rota: Adicionar Reserva na Análise X
    path('analises/<int:analysis_id>/reservar/', views.add_booking, name='add_booking'),

    # Nova rota: Adicionar Insumo na Análise X
    path('analises/<int:analysis_id>/insumo/', views.add_consumable, name='add_consumable'),

    # Rota para listar insumos (ex: /laboratorio/insumos/)
    path('insumos/', views.consumable_list, name='consumable_list'),

    # NOVA ROTA:
    path('insumos/novo/', views.ConsumableCreateView.as_view(), name='consumable_create'),

    # NOVA ROTA:
    path('insumos/<int:pk>/editar/', views.ConsumableUpdateView.as_view(), name='consumable_edit'),
]