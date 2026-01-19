from django.shortcuts import render, redirect, get_object_or_404
from .models import Analysis, Consumable, EquipmentBooking
from django.contrib.auth.decorators import login_required
from .forms import EquipmentBookingForm, MaterialUsageForm, ConsumableForm # <--- Adicionei ConsumableForm
from django.contrib import messages

# --- NOVAS IMPORTAÇÕES NECESSÁRIAS PARA A CLASS-BASED VIEW ---
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
# -------------------------------------------------------------

import json
from django.utils import timezone
from datetime import timedelta

# Lista todas as análises (Dashboard)
@login_required
def analysis_list(request):
    analyses = Analysis.objects.filter(researcher=request.user).order_by('-created_at')
    return render(request, 'laboratory/analysis_list.html', {'analyses': analyses})

# Cria uma nova análise
@login_required
def analysis_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        Analysis.objects.create(
            title=title,
            description=description,
            researcher=request.user
        )
        return redirect('analysis_list')
        
    return render(request, 'laboratory/analysis_create.html')

@login_required
def analysis_detail(request, pk):
    analysis = get_object_or_404(Analysis, pk=pk, researcher=request.user)
    context = {
        'analysis': analysis,
    }
    return render(request, 'laboratory/analysis_detail.html', context)

@login_required
def add_booking(request, analysis_id):
    analysis = get_object_or_404(Analysis, pk=analysis_id, researcher=request.user)
    
    if request.method == 'POST':
        form = EquipmentBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.analysis = analysis
            try:
                booking.full_clean()
                booking.save()
                messages.success(request, "Equipamento reservado com sucesso!")
                return redirect('analysis_detail', pk=analysis.pk)
            except Exception as e:
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

# Essa view registra o USO de um insumo (Gasto)
@login_required
def add_consumable(request, analysis_id):
    analysis = get_object_or_404(Analysis, pk=analysis_id, researcher=request.user)
    
    if request.method == 'POST':
        form = MaterialUsageForm(request.POST)
        if form.is_valid():
            usage = form.save(commit=False)
            usage.analysis = analysis # Vincula à análise atual
            
            # --- O PULO DO GATO: BAIXA DE ESTOQUE ---
            item_estoque = usage.consumable # Pega o objeto do estoque
            
            # 1. Verifica se tem saldo suficiente
            if item_estoque.quantity >= usage.quantity_used:
                
                # 2. Subtrai a quantidade
                item_estoque.quantity -= usage.quantity_used
                item_estoque.save() # SALVA A NOVA QUANTIDADE NO BANCO
                
                # 3. Salva o registro de uso
                usage.save()
                
                messages.success(request, f"Uso registrado! Restam {item_estoque.quantity} {item_estoque.unit} no estoque.")
                return redirect('analysis_detail', pk=analysis.pk)
            
            else:
                # Se tentar usar mais do que tem, dá erro
                messages.error(request, f"Estoque insuficiente! Você tentou usar {usage.quantity_used}, mas só tem {item_estoque.quantity}.")
                
    else:
        form = MaterialUsageForm()

    return render(request, 'laboratory/consumable_form.html', {
        'form': form, 
        'analysis': analysis
    })

@login_required
def dashboard(request):
    today = timezone.now()
    start_date = today - timedelta(days=2)
    end_date = today + timedelta(days=14)

    bookings = EquipmentBooking.objects.filter(
        start_time__gte=start_date,
        start_time__lte=end_date
    ).select_related('equipment', 'analysis')

    gantt_data = []
    
    for booking in bookings:
        color = '#2563EB' if booking.analysis.researcher == request.user else '#9CA3AF'
        
        gantt_data.append({
            'x': booking.equipment.name,
            'y': [
                int(booking.start_time.timestamp() * 1000),
                int(booking.end_time.timestamp() * 1000)
            ],
            'fillColor': color,
            'meta': {
                'analise': booking.analysis.title,
                'researcher': booking.analysis.researcher.username
            }
        })

    context = {
        'gantt_data': json.dumps(gantt_data)
    }
    return render(request, 'laboratory/dashboard.html', context)

@login_required
def consumable_list(request):
    consumables = Consumable.objects.all().order_by('name')
    return render(request, 'laboratory/consumable_list.html', {'consumables': consumables})

# --- NOVA VIEW: CADASTRAR NOVO TIPO DE INSUMO (Estoque) ---
class ConsumableCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Consumable
    form_class = ConsumableForm
    # MUDEI O NOME AQUI PARA NÃO CONFLITAR COM O DE CIMA
    template_name = 'laboratory/consumable_create.html' 
    success_url = reverse_lazy('consumable_list')

    def test_func(self):
        return self.request.user.is_staff
    
class ConsumableUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Consumable
    form_class = ConsumableForm
    template_name = 'laboratory/consumable_edit.html' # Vamos criar um template específico
    success_url = reverse_lazy('consumable_list')

    def test_func(self):
        return self.request.user.is_staff