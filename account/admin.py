from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Register your models here.




class UserAdmin(UserAdmin):
    
    list_display = ['email', 'first_name', 'last_name', 'is_staff','is_superuser',  'is_active', 'date_joined']
    list_filter = ['is_staff','email']
    list_display_links = ['email','first_name','last_name']
    
    readonly_fields = ['last_login', 'date_joined']
    
    ordering = ['-date_joined']
    filter_horizontal=[]
    fieldsets = []
    
    
admin.site.register(User, UserAdmin)
