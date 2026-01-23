from django import forms
from equipments.models import Equipment
from .models import EquipmentBooking, MaterialUsage, Consumable, Analysis

class EquipmentBookingForm(forms.ModelForm):
    class Meta:
        model = EquipmentBooking
        fields = ['equipment', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'border rounded p-2 w-full'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'border rounded p-2 w-full'}),
            'equipment': forms.Select(attrs={'class': 'border rounded p-2 w-full bg-white'}),
        }
        labels = {
            'equipment': 'Equipamento',
            'start_time': 'Início do Uso',
            'end_time': 'Fim do Uso',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # EXCLUI equipamentos com status DESATIVADO e QUEBRADO da lista de reserva
        self.fields['equipment'].queryset = Equipment.objects.exclude(
            status__in=[Equipment.Status.DESATIVADO, Equipment.Status.QUEBRADO]
        )

class MaterialUsageForm(forms.ModelForm):
    class Meta:
        model = MaterialUsage
        fields = ['consumable', 'quantity_used']
        widgets = {
            'consumable': forms.Select(attrs={'class': 'border rounded p-2 w-full bg-white'}),
            'quantity_used': forms.NumberInput(attrs={'class': 'border rounded p-2 w-full', 'placeholder': 'Ex: 10.5'}),
        }
        labels = {
            'consumable': 'Item do Estoque',
            'quantity_used': 'Quantidade Utilizada',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra apenas insumos ATIVOS (is_active=True)
        self.fields['consumable'].queryset = Consumable.objects.filter(is_active=True)

# --- ADICIONE ESTA NOVA CLASSE AO FINAL ---
class ConsumableForm(forms.ModelForm):
    class Meta:
        model = Consumable
        # Estes campos agora existem no model, então vai funcionar!
        fields = ['name', 'quantity', 'unit', 'minimum_stock', 'expiration_date']
        
        labels = {
            'name': 'Nome do Insumo',
            'quantity': 'Quantidade Inicial',
            'unit': 'Unidade (ex: cx, ml, g)',
            'minimum_stock': 'Estoque Mínimo (Alerta)',
            'expiration_date': 'Validade',
        }
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
            'quantity': forms.NumberInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
            'unit': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
            'minimum_stock': forms.NumberInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
            'expiration_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
        }

# --- ADICIONE ESTA CLASSE PARA AS ANÁLISES ---
class AnalysisForm(forms.ModelForm):
    class Meta:
        model = Analysis
        # Aqui definimos explicitamente que queremos o campo PROJETO
        fields = ['title', 'project_name', 'description', 'status']
        
        labels = {
            'title': 'Título da Análise',
            'project_name': 'Nome do Projeto',
            'description': 'Metodologia / Descrição',
            'status': 'Situação Atual',
        }
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500', 'placeholder': 'Ex: Análise de pH da Amostra X'}),
            'project_name': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500', 'placeholder': 'Ex: Projeto Iniciação Científica 2026'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
            'status': forms.Select(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
        }