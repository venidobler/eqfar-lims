from django.shortcuts import render, redirect, get_object_or_404
from .models import Analysis, Consumable, EquipmentBooking
from django.contrib.auth.decorators import login_required
from .forms import EquipmentBookingForm, MaterialUsageForm, ConsumableForm, AnalysisForm
from django.contrib import messages

# --- NOVAS IMPORTAÇÕES NECESSÁRIAS PARA A CLASS-BASED VIEW ---
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
# -------------------------------------------------------------

from django_filters.views import FilterView
from .filters import AnalysisFilter, ConsumableFilter

import json
from django.utils import timezone
from datetime import timedelta

# Lista todas as análises (Dashboard)
class AnalysisListView(LoginRequiredMixin, FilterView):
    model = Analysis
    template_name = 'laboratory/analysis_list.html'
    context_object_name = 'analyses'
    filterset_class = AnalysisFilter
    paginate_by = 10 # 10 análises por página

    def get_queryset(self):
        # Mostra as análises do usuário logado OU todas se for Staff/Admin
        user = self.request.user
        if user.is_staff:
            queryset = Analysis.objects.all()
        else:
            queryset = Analysis.objects.filter(researcher=user)
        
        # Ordena da mais recente para a mais antiga
        return queryset.order_by('-created_at')

# 1. CRIAÇÃO (Substitui o antigo def analysis_create)
class AnalysisCreateView(LoginRequiredMixin, CreateView):
    model = Analysis
    form_class = AnalysisForm
    template_name = 'laboratory/analysis_form.html'
    success_url = reverse_lazy('analysis_list')

    # NOVO: Passa o usuário para o formulário
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.researcher = self.request.user
        # Garante forçadamente que nasce como 'planned' no Backend
        form.instance.status = 'planned' 
        return super().form_valid(form)


# 2. EDIÇÃO
class AnalysisUpdateView(LoginRequiredMixin, UpdateView):
    model = Analysis
    form_class = AnalysisForm
    template_name = 'laboratory/analysis_form.html'
    success_url = reverse_lazy('analysis_list')
    
    # NOVO: Passa o usuário para o formulário
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Analysis.objects.all()
        return Analysis.objects.filter(researcher=user)

# 3. DETALHES (Substitui o antigo def analysis_detail)
class AnalysisDetailView(LoginRequiredMixin, DetailView):
    model = Analysis
    template_name = 'laboratory/analysis_detail.html'
    context_object_name = 'analysis'

    def get_queryset(self):
        # CORREÇÃO DO ERRO DE PERMISSÃO:
        # Se for Staff, vê tudo. Se for usuário comum, vê só as suas.
        user = self.request.user
        if user.is_staff:
            return Analysis.objects.all()
        return Analysis.objects.filter(researcher=user)

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

class ConsumableListView(LoginRequiredMixin, FilterView):
    model = Consumable
    template_name = 'laboratory/consumable_list.html'
    context_object_name = 'consumables'
    filterset_class = ConsumableFilter # Conecta com o filtro
    paginate_by = 10 # <--- PAGINAÇÃO AUTOMÁTICA! Mostra 10 itens por página
    
    # Ordenação padrão (os mais novos primeiro ou por nome)
    def get_queryset(self):
        return Consumable.objects.all().order_by('expiration_date', 'name')

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
    
@login_required
def archive_consumable(request, pk):
    # Verificação de segurança: Apenas Staff (Equipe) pode arquivar
    if not request.user.is_staff:
        messages.error(request, "Você não tem permissão para arquivar insumos.")
        return redirect('consumable_list')

    # Busca o insumo pelo ID (pk) ou dá erro 404 se não existir
    item = get_object_or_404(Consumable, pk=pk)
    
    # Lógica de Toggle:
    # Se está ativo -> desativa (arquiva)
    # Se está inativo -> ativa (restaura)
    if item.is_active:
        item.is_active = False
        messages.warning(request, f"O insumo '{item.name}' foi arquivado e não aparecerá em novas listas.")
    else:
        item.is_active = True
        messages.success(request, f"O insumo '{item.name}' foi reativado com sucesso.")
    
    item.save()
    
    # Redireciona de volta para a lista (ou para a edição, se preferir)
    return redirect('consumable_list')