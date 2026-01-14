from django.contrib import admin
from .models import Scheduling

@admin.register(Scheduling)
class SchedulingAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'user', 'start_time', 'end_time', 'status', 'estimated_cost_display')
    list_filter = ('status', 'start_time', 'equipment')
    
    def estimated_cost_display(self, obj):
        return f"R$ {obj.estimated_cost:.2f}"
    estimated_cost_display.short_description = "Custo Estimado"