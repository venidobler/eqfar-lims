from django.urls import path
from . import views

urlpatterns = [
    # Agendamento do Usuário
    path('equipment/<int:equipment_id>/schedule/', views.create_scheduling, name='create_scheduling'),
    path('my-schedulings/', views.my_schedulings, name='my_schedulings'),
    
    # Dashboard e Gestão
    path('dashboard/', views.dashboard, name='dashboard'),
    path('manage/', views.manage_requests, name='manage_requests'),
    path('manage/approve/<int:id>/', views.approve_scheduling, name='approve_scheduling'),
    path('manage/reject/<int:id>/', views.reject_scheduling, name='reject_scheduling'),
]