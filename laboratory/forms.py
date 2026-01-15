from django import forms
from .models import EquipmentBooking, MaterialUsage

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