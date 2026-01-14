from django.shortcuts import render, get_object_or_404 # <--- Importe o 404
from .models import Equipment

def list_equipments(request):
    # ... (código que já estava aqui) ...
    equipments = Equipment.objects.all().order_by('name')
    context = {'equipments': equipments}
    return render(request, 'equipments/list.html', context)

# --- ADICIONE ESTA NOVA FUNÇÃO ABAIXO ---
def equipment_detail(request, id):
    # Tenta pegar o equipamento pelo ID, se não existir, dá erro 404
    equipment = get_object_or_404(Equipment, pk=id)
    
    context = {
        'equipment': equipment
    }
    return render(request, 'equipments/detail.html', context)