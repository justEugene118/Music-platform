from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active', 'is_creator')
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'creator_name', 'creator_descr')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_creator')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active', 'creator_name', 'creator_descr')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

    def __str__(self):
        return self.username


admin.site.register(CustomUser, CustomUserAdmin)