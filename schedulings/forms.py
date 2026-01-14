# SUBSTITUA O ARQUIVO COMPLETO POR ESTE:
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import Scheduling

class SchedulingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Retira o equipamento dos argumentos extras antes de iniciar o form
        self.equipment = kwargs.pop('equipment', None) 
        super().__init__(*args, **kwargs)

    class Meta:
        model = Scheduling
        fields = ['purpose', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full p-2 border rounded'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full p-2 border rounded'}),
            'purpose': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Ex: Análise do Lote 123'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')

        if start and end:
            # 1. Validação Básica: Fim deve ser depois do Início
            if end <= start:
                self.add_error('end_time', "O fim deve ser após o início.")
                return

            # 2. Validação de Conflito (A Lógica Poderosa)
            # Procura agendamentos PARA ESSE EQUIPAMENTO que se sobreponham
            conflicts = Scheduling.objects.filter(
                equipment=self.equipment,
                status__in=['PEND', 'CONF', 'EXEC'], # Ignora cancelados
            ).filter(
                # Lógica de Sobreposição: (Início Novo < Fim Existente) E (Fim Novo > Início Existente)
                start_time__lt=end,
                end_time__gt=start
            )

            if conflicts.exists():
                raise ValidationError("Já existe um agendamento para este equipamento neste horário.")
        
        return cleaned_data