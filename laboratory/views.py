from django.shortcuts import render, redirect, get_object_or_404
from .models import Analysis
from django.contrib.auth.decorators import login_required
from .forms import EquipmentBookingForm, MaterialUsageForm
from django.contrib import messages

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