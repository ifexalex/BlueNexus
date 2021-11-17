from django.contrib import admin
from .models import Vendor
# Register your models here.

class VendorAdmin(admin.ModelAdmin):
        
    list_display = ['store_name', 'created_date', 'modified_date', 'is_active']
    search_fields = ['store_name', 'is_active',] 
    
    
admin.site.register(Vendor,VendorAdmin)