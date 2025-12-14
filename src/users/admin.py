from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.forms import UserChangeForm, UserCreationForm
from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['email', 'is_staff', 'is_active', 'is_superuser', 'date_joined']
    list_filter = ['is_staff', 'is_active', 'is_superuser']

    fieldsets = [
        (None, {'fields': ['email', 'password']}),
        ('Permissions', {'fields': ['is_staff', 'is_superuser', 'is_active']}),
        ('Permission Groups', {'fields': ['groups', 'user_permissions']}),
        ('Important dates', {'fields': ['date_joined',]}),
    ]
    
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "password1", "password2"],
            },
        ),
    ]
    
    search_fields = ['email']
    ordering = ['email']
    readonly_fields = ['date_joined']