from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, UserRole


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'full_name', 'user_password', 'role', 'job_category_id', 'organization_id', 'image_url', 'fcm_id', 'os_type', 'device_unique_id', 'notification_status', 'created_date', 'updated_date', 'status')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'full_name', 'role', 'job_category_id', 'organization_id', 'image_url', 'fcm_id', 'os_type', 'device_unique_id', 'notification_status', 'created_date', 'updated_date', 'status')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserRole)