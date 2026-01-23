from django.urls import path
from . import views

urlpatterns = [
    # Nova rota para o dashboard
    path('', views.dashboard, name='dashboard'),

    # Lista (já fizemos)
    path('analises/', views.AnalysisListView.as_view(), name='analysis_list'),
    
    # Criação (MUDOU: de views.analysis_create para AnalysisCreateView.as_view())
    path('analises/nova/', views.AnalysisCreateView.as_view(), name='analysis_create'),
    
    # Detalhes (MUDOU: de views.analysis_detail para AnalysisDetailView.as_view())
    path('analises/<int:pk>/', views.AnalysisDetailView.as_view(), name='analysis_detail'),
    
    # Edição (NOVO)
    path('analises/<int:pk>/editar/', views.AnalysisUpdateView.as_view(), name='analysis_edit'),

    # Nova rota: Adicionar Reserva na Análise X
    path('analises/<int:analysis_id>/reservar/', views.add_booking, name='add_booking'),

    # Nova rota: Adicionar Insumo na Análise X
    path('analises/<int:analysis_id>/insumo/', views.add_consumable, name='add_consumable'),

    # Rota para listar insumos (ex: /laboratorio/insumos/)
    path('insumos/', views.ConsumableListView.as_view(), name='consumable_list'),

    # NOVA ROTA:
    path('insumos/novo/', views.ConsumableCreateView.as_view(), name='consumable_create'),

    # NOVA ROTA:
    path('insumos/<int:pk>/editar/', views.ConsumableUpdateView.as_view(), name='consumable_edit'),

    # NOVA ROTA:
    path('insumos/<int:pk>/arquivar/', views.archive_consumable, name='consumable_archive'),

]