from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Register your models here.




class UserAdmin(admin.ModelAdmin):
    
    list_display = ['email', 'first_name', 'last_name', 'is_staff','is_superuser',  'is_active','credit_balance', 'is_eligible','date_joined']
    list_filter = ['is_staff','email']
    list_display_links = ['email','first_name','last_name']
    
    readonly_fields = ['last_login', 'date_joined']
    
    ordering = ['-date_joined']
    
    
admin.site.register(User, UserAdmin)
