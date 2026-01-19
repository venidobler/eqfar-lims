from django import forms
from .models import Equipment

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        # Lista exata dos campos que existem no seu models.py
        fields = [
            'name', 
            'asset_tag', 
            'brand', 
            'model', 
            'status', 
            'photo', 
            'analysis_time_minutes', 
            'cost_per_hour'
        ]
        
        labels = {
            'name': 'Nome do Equipamento',
            'asset_tag': 'Patrimônio (Tag)',
            'brand': 'Marca',
            'model': 'Modelo',
            'status': 'Status Atual',
            'photo': 'Foto do Equipamento',
            'analysis_time_minutes': 'Tempo de Análise (min)',
            'cost_per_hour': 'Custo Hora (R$)',
        }
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
            'asset_tag': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
            'brand': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
            'model': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
            
            # Select com estilo para o Status
            'status': forms.Select(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
            
            # Input de arquivo estilizado
            'photo': forms.FileInput(attrs={'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'}),
            
            # Campos numéricos
            'analysis_time_minutes': forms.NumberInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
            'cost_per_hour': forms.NumberInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500', 'step': '0.01'}),
        }