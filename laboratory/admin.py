from django.contrib import admin
from .models import Analysis, Consumable, EquipmentBooking, MaterialUsage

# Configuração para mostrar os itens dentro da Análise (Inline)
class MaterialUsageInline(admin.TabularInline):
    model = MaterialUsage
    extra = 1

class EquipmentBookingInline(admin.TabularInline):
    model = EquipmentBooking
    extra = 1

@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ('title', 'researcher', 'status', 'created_at')
    list_filter = ('status', 'researcher')
    search_fields = ('title', 'project_name')
    # Isso permite adicionar reagentes e agendamentos direto na tela da Análise!
    inlines = [EquipmentBookingInline, MaterialUsageInline]

@admin.register(Consumable)
class ConsumableAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'current_stock', 'cost_per_unit')
    search_fields = ('name',)

# As outras tabelas também podem ser registradas se quiser ver separadamente
admin.site.register(EquipmentBooking)
admin.site.register(MaterialUsage)