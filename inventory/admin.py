from django.contrib import admin

# Register your models here.
from .models import InventoryRequest


class InventoryRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'total', 'unit', 'status']


admin.site.register(InventoryRequest, InventoryRequestAdmin)