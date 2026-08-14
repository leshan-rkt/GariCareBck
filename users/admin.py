from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Fields to show in the LIST view
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'phone', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_superuser']
    
    # Fields when EDITING a user
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'sacco_name', 'sacco_registration')}),
    )
    
    # Fields when CREATING a user
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'sacco_name', 'sacco_registration')}),
    )