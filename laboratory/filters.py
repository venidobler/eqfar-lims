import django_filters
from .models import Consumable, Analysis
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

class AnalysisFilter(django_filters.FilterSet):
    # Busca inteligente: Procura no Título, Descrição E Projeto ao mesmo tempo
    search = django_filters.CharFilter(
        method='filter_search',
        label='Buscar (Título, Projeto ou Descrição)'
    )
    
    # Filtro de Status (Dropdown com as opções do Model)
    status = django_filters.ChoiceFilter(
        choices=Analysis.STATUS_CHOICES,
        label='Status'
    )

    # Filtro de Data de Criação (De... Até...)
    created_at = django_filters.DateFromToRangeFilter(
        label='Data de Criação',
        widget=django_filters.widgets.RangeWidget(attrs={'type': 'date', 'class': 'form-input'})
    )

    class Meta:
        model = Analysis
        fields = ['search', 'status', 'created_at']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | 
            Q(description__icontains=value) |
            Q(project_name__icontains=value)
        )