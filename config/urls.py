from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Reload do Tailwind
    path("__reload__/", include("django_browser_reload.urls")),

    # --- AUTENTICAÇÃO (Adicione esta linha) ---
    # Isso cria as rotas: /accounts/login/ (nome='login') e /accounts/logout/
    path('accounts/', include('django.contrib.auth.urls')), 

    # --- SEUS APPS ---
    # Rota para a lista de equipamentos (Home do site)
    path('', include('equipments.urls')), 
    
    # Rota para o módulo de laboratório (Análises, etc)
    path('laboratorio/', include('laboratory.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)