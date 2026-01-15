from django.shortcuts import render, redirect, get_object_or_404
from .models import Analysis, EquipmentBooking
from django.contrib.auth.decorators import login_required
from .forms import EquipmentBookingForm, MaterialUsageForm
from django.contrib import messages

import json
from django.utils import timezone
from datetime import timedelta

# Lista todas as análises (Dashboard)
@login_required
def analysis_list(request):
    analyses = Analysis.objects.filter(researcher=request.user).order_by('-created_at')
    return render(request, 'laboratory/analysis_list.html', {'analyses': analyses})

# Cria uma nova análise (apenas o cabeçalho por enquanto)
@login_required
def analysis_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        # Cria a análise vinculada ao usuário logado
        Analysis.objects.create(
            title=title,
            description=description,
            researcher=request.user
        )
        return redirect('analysis_list')
        
    return render(request, 'laboratory/analysis_create.html')

@login_required
def analysis_detail(request, pk):
    # Busca a análise ou dá erro 404 se não existir
    # O 'researcher=request.user' garante que ninguém veja a análise de outro (segurança básica)
    analysis = get_object_or_404(Analysis, pk=pk, researcher=request.user)
    
    context = {
        'analysis': analysis,
        # O Django já traz os relacionamentos reversos (bookings e materials_used)
        # por causa do related_name que definimos no models.py!
    }
    return render(request, 'laboratory/analysis_detail.html', context)

@login_required
def add_booking(request, analysis_id):
    analysis = get_object_or_404(Analysis, pk=analysis_id, researcher=request.user)
    
    if request.method == 'POST':
        form = EquipmentBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.analysis = analysis # Vincula à análise atual
            try:
                booking.full_clean() # Força a validação do Model (onde está a regra anti-conflito)
                booking.save()
                messages.success(request, "Equipamento reservado com sucesso!")
                return redirect('analysis_detail', pk=analysis.pk)
            except Exception as e:
                # Se der erro de validação (ex: conflito de horário), exibe na tela
                # O Django retorna o erro como dicionário ou lista, pegamos a mensagem
                if hasattr(e, 'message_dict'):
                    for field, errors in e.message_dict.items():
                        for error in errors:
                            messages.error(request, f"{error}")
                else:
                    messages.error(request, str(e))
    else:
        form = EquipmentBookingForm()

    return render(request, 'laboratory/booking_form.html', {
        'form': form, 
        'analysis': analysis
    })

@login_required
def add_consumable(request, analysis_id):
    analysis = get_object_or_404(Analysis, pk=analysis_id, researcher=request.user)
    
    if request.method == 'POST':
        form = MaterialUsageForm(request.POST)
        if form.is_valid():
            usage = form.save(commit=False)
            usage.analysis = analysis # Vincula à análise atual
            usage.save()
            messages.success(request, "Insumo registrado com sucesso!")
            return redirect('analysis_detail', pk=analysis.pk)
    else:
        form = MaterialUsageForm()

    return render(request, 'laboratory/consumable_form.html', {
        'form': form, 
        'analysis': analysis
    })

@login_required
def dashboard(request):
    # 1. Definir o intervalo (Ex: Últimos 2 dias e próximos 14 dias)
    today = timezone.now()
    start_date = today - timedelta(days=2)
    end_date = today + timedelta(days=14)

    # 2. Buscar as reservas nesse período
    bookings = EquipmentBooking.objects.filter(
        start_time__gte=start_date,
        start_time__lte=end_date
    ).select_related('equipment', 'analysis')

    # 3. Formatar para o ApexCharts
    # Formato: {'x': 'Nome do Equipamento', 'y': [Inicio_timestamp, Fim_timestamp]}
    gantt_data = []
    
    for booking in bookings:
        # Define cor: Azul se for minha reserva, Cinza se for de outro
        color = '#2563EB' if booking.analysis.researcher == request.user else '#9CA3AF'
        
        gantt_data.append({
            'x': booking.equipment.name,
            'y': [
                int(booking.start_time.timestamp() * 1000), # JS usa milissegundos
                int(booking.end_time.timestamp() * 1000)
            ],
            'fillColor': color,
            'meta': {
                'analise': booking.analysis.title,
                'researcher': booking.analysis.researcher.username
            }
        })

    # Serializa para JSON para o HTML ler
    context = {
        'gantt_data': json.dumps(gantt_data)
    }
    return render(request, 'laboratory/dashboard.html', context)