from django.shortcuts import render, get_object_or_404 # <--- Importe o 404
from django.db.models import Q  # <--- IMPORTANTE: Permite buscas com "OU" (OR)
from .models import Equipment

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