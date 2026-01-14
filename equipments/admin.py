from django.contrib import admin
from .models import Equipment

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'asset_tag', 'status', 'updated_at')
    list_filter = ('status', 'brand')
    search_fields = ('name', 'asset_tag')