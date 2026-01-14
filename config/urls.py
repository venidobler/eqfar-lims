from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# IMPORTAR A VIEW AQUI:
from equipments.views import list_equipments, equipment_detail 
from schedulings.views import create_scheduling, my_schedulings, dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    
    # ROTA DA HOME:
    path('', list_equipments, name='home'),

    # --- NOVA ROTA ---
    # O <int:id> captura o número da URL e passa para a view
    path('equipment/<int:id>/', equipment_detail, name='equipment_detail'),

    # NOVA ROTA DE AGENDAMENTO
    path('equipment/<int:equipment_id>/schedule/', create_scheduling, name='create_scheduling'),

    # NOVA ROTA:
    path('my-schedulings/', my_schedulings, name='my_schedulings'),

    # NOVA ROTA DE DASHBOARD
    path('dashboard/', dashboard, name='dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)