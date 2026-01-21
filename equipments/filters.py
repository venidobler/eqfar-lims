# equipments/filters.py
import django_filters
from .models import Equipment

class EquipmentFilter(django_filters.FilterSet):
    # Busca por texto no nome, marca ou modelo
    search = django_filters.CharFilter(
        method='filter_search', 
        label='Buscar (Nome, Marca ou Modelo)'
    )
    
    # Filtro exato de status (Dropdown)
    status = django_filters.ChoiceFilter(
        choices=Equipment.Status.choices,
        label='Status Atual'
    )

    class Meta:
        model = Equipment
        fields = ['search', 'status']

    # Método personalizado para buscar em vários campos ao mesmo tempo
    def filter_search(self, queryset, name, value):
        from django.db.models import Q
        return queryset.filter(
            Q(name__icontains=value) | 
            Q(brand__icontains=value) | 
            Q(model__icontains=value)
        )