import django_filters
from .models import Consumable
from django import forms

class ConsumableFilter(django_filters.FilterSet):
    # Busca por texto no nome (icontains = case insensitive)
    name = django_filters.CharFilter(
        lookup_expr='icontains', 
        label='Nome do Insumo'
    )
    
    # Filtro de Data de Validade (Range = De... Até...)
    expiration_date = django_filters.DateFromToRangeFilter(
        label='Validade (Período)',
        widget=django_filters.widgets.RangeWidget(attrs={'type': 'date', 'class': 'form-input'})
    )

    # Filtro para mostrar/esconder Arquivados
    # Note que usamos BooleanFilter para mapear o True/False do banco
    is_active = django_filters.BooleanFilter(
        label='Apenas Ativos',
        field_name='is_active',
        widget=forms.CheckboxInput,
        initial=True # Começa filtrando só os ativos por padrão
    )

    class Meta:
        model = Consumable
        fields = ['name', 'is_active', 'expiration_date']