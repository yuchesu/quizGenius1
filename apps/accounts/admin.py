from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'firstname', 'lastname', 'is_active', 'is_staff', 'phone', ]
    fieldsets = UserAdmin.fieldsets + (
        ('Profile', {'fields': ('firstname',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Profile', {'fields': ('firstname',)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)