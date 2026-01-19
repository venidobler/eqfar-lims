from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

# IMPORTANTE: Importe a view que serve arquivos estáticos manualmente
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Reload do Tailwind
    path("__reload__/", include("django_browser_reload.urls")),

    # --- AUTENTICAÇÃO (Adicione esta linha) ---
    # Isso cria as rotas: /accounts/login/ (nome='login') e /accounts/logout/
    path('accounts/', include('django.contrib.auth.urls')), 
    path('logout/', LogoutView.as_view(), name='logout'),

    # --- SEUS APPS ---
    # Rota para a lista de equipamentos (Home do site)
    path('equipamentos/', include('equipments.urls')), 
    
    # Rota para o módulo de laboratório (Análises, etc)
    path('', include('laboratory.urls')),

    # --- O PULO DO GATO ---
    # Esta linha obriga o Django a servir a mídia, mesmo com DEBUG=False/Gunicorn
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)