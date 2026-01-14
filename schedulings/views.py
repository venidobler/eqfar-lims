from django.contrib.auth.decorators import login_required # <--- Importe isso no topo
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from equipments.models import Equipment
from .forms import SchedulingForm
from .models import Scheduling

import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import F

def create_scheduling(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)
    
    if request.method == 'POST':
        # PASSAR O EQUIPAMENTO AQUI:
        form = SchedulingForm(request.POST, equipment=equipment) 
        if form.is_valid():
            scheduling = form.save(commit=False)
            scheduling.equipment = equipment
            scheduling.user = request.user
            scheduling.save()
            messages.success(request, 'Agendamento realizado com sucesso!')
            return redirect('home')
    else:
        # E AQUI TAMBÉM:
        form = SchedulingForm(equipment=equipment)

    context = {
        'form': form,
        'equipment': equipment
    }
    return render(request, 'schedulings/form.html', context)

@login_required
def my_schedulings(request):
    # Busca agendamentos ONDE (filter) o usuário é o atual (request.user)
    schedulings = Scheduling.objects.filter(user=request.user).order_by('-start_time')
    
    context = {
        'schedulings': schedulings
    }
    return render(request, 'schedulings/my_list.html', context)

def dashboard(request):
    # Busca agendamentos confirmados ou em execução
    schedules = Scheduling.objects.filter(status__in=['CONF', 'EXEC'])
    
    gantt_data = []
    
    for schedule in schedules:
        gantt_data.append({
            'x': schedule.equipment.name, 
            'y': [
                # AQUI ESTÁ A MUDANÇA: Convertendo para milissegundos
                int(schedule.start_time.timestamp() * 1000), 
                int(schedule.end_time.timestamp() * 1000)
            ],
            'fillColor': '#008FFB' if schedule.status == 'CONF' else '#00E396'
        })

    context = {
        'gantt_data': json.dumps(gantt_data, cls=DjangoJSONEncoder)
    }
    return render(request, 'schedulings/dashboard.html', context)