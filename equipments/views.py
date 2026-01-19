from django.shortcuts import render, get_object_or_404, redirect # <--- Importe o 404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q  # <--- IMPORTANTE: Permite buscas com "OU" (OR)
from .models import Equipment
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import EquipmentForm
from django.contrib import messages

def list_equipments(request):
    query = request.GET.get('q', '')
    equipments = Equipment.objects.all()
    
    if query:
        equipments = equipments.filter(
            Q(name__icontains=query) |   # Busca no Nome
            Q(model__icontains=query) |  # Busca no Modelo
            Q(brand__icontains=query)    # Busca na Marca
        )

    context = {
        'equipments': equipments,
        'query': query
    }
    return render(request, 'equipments/list.html', context)

# --- ADICIONE ESTA NOVA FUNÇÃO ABAIXO ---
def equipment_detail(request, id):
    # Tenta pegar o equipamento pelo ID, se não existir, dá erro 404
    equipment = get_object_or_404(Equipment, pk=id)
    
    context = {
        'equipment': equipment
    }
    return render(request, 'equipments/detail.html', context)

# Nova View de Cadastro
class EquipmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'equipments/equipment_form.html'
    success_url = reverse_lazy('equipment_list') # Volta para a lista ao terminar

    # Teste de segurança: Só entra se for Admin/Staff
    def test_func(self):
        return self.request.user.is_staff
    
class EquipmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'equipments/equipment_form.html' # Reaproveitamos o template!
    success_url = reverse_lazy('equipment_list')

    # Só Admin/Staff altera
    def test_func(self):
        return self.request.user.is_staff
        
    # Hackzinho para mudar o título da página de "Cadastrar" para "Editar"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Editar Equipamento'
        return context
    
@login_required
def archive_equipment(request, pk):
    # Verificação de segurança: Só staff
    if not request.user.is_staff:
        messages.error(request, "Você não tem permissão para arquivar equipamentos.")
        return redirect('equipment_list')
        
    equipment = get_object_or_404(Equipment, pk=pk)
    
    # Lógica de Toggle usando o TextChoices
    if equipment.status != Equipment.Status.DESATIVADO:
        equipment.status = Equipment.Status.DESATIVADO
        messages.warning(request, f"O equipamento '{equipment.name}' foi desativado.")
    else:
        # Se reativar, volta para DISPONÍVEL por padrão
        equipment.status = Equipment.Status.DISPONIVEL 
        messages.success(request, f"O equipamento '{equipment.name}' foi reativado.")
        
    equipment.save()
    return redirect('equipment_list')