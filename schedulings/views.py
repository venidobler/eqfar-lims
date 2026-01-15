from django.contrib.auth.decorators import login_required # <--- Importe isso no topo
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required # <--- Só staff pode acessar
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

#------------------- GESTÃO ----------------------------#

# 1. A TELA DE GESTÃO
@staff_member_required
def manage_requests(request):
    # Busca só os pendentes, ordenados pelos mais antigos primeiro
    pending_schedulings = Scheduling.objects.filter(status='PEND').order_by('created_at')
    
    context = {
        'pending_schedulings': pending_schedulings
    }
    return render(request, 'schedulings/manage.html', context)

# 2. A AÇÃO DE APROVAR
@staff_member_required
def approve_scheduling(request, id):
    scheduling = get_object_or_404(Scheduling, id=id)
    scheduling.status = 'CONF'
    scheduling.save()
    messages.success(request, f'Agendamento de {scheduling.user} confirmado!')
    return redirect('manage_requests')

# 3. A AÇÃO DE REJEITAR
@staff_member_required
def reject_scheduling(request, id):
    scheduling = get_object_or_404(Scheduling, id=id)
    scheduling.status = 'CANC'
    scheduling.save()
    messages.warning(request, f'Agendamento cancelado.')
    return redirect('manage_requests')