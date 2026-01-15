from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Reload do Tailwind (Crucial para o desenvolvimento)
    path("__reload__/", include("django_browser_reload.urls")),

    # --- INCLUSÃO DOS APPS ---
    
    # 1. Rotas de Agendamento (Colocamos antes para não conflitar com a home vazia)
    path('', include('schedulings.urls')),

    # 2. Rotas de Equipamentos (Onde está a Home)
    path('', include('equipments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)