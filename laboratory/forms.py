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

    # AQUI ESTÁ A MÁGICA 🎩
    def __init__(self, *args, **kwargs):
        # Extrai o usuário que passaremos pela View
        self.user = kwargs.pop('user', None) 
        super(AnalysisForm, self).__init__(*args, **kwargs)

        # Regra 1: CRIAÇÃO
        # Se não tem ID (instance.pk é None), é uma criação nova.
        if not self.instance.pk:
            # Remove o campo status do formulário visualmente
            # O usuário não escolhe status ao criar, nasce sempre 'planned'
            if 'status' in self.fields:
                self.fields['status'].widget = forms.HiddenInput()
                self.fields['status'].initial = 'planned'
        
        # Regra 2: EDIÇÃO
        else:
            # Se for STAFF (Gestor), vê todas as opções (não fazemos nada)
            # Se for PESQUISADOR (Comum), aplicamos o filtro
            if self.user and not self.user.is_staff:
                allowed_choices = [
                    ('planned', 'Planejada'),
                    ('ongoing', 'Em Andamento'),
                ]
                
                # Mas atenção: Se a análise JÁ estiver aprovada/rejeitada, 
                # o pesquisador deve ver o status atual (mas não pode mudar).
                current_status = self.instance.status
                if current_status in ['approved', 'rejected']:
                    # Se já está finalizada, tornamos o campo somente leitura ou desabilitado
                    self.fields['status'].disabled = True
                else:
                    # Se ainda está aberta, limita as opções
                    self.fields['status'].choices = allowed_choices