from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from users.models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('email','username', 'first_name', 'last_name', 'is_staff', 'is_client','is_verified','created_by','modified_by')
    list_filter = ('is_client','is_staff','created','modified')


admin.site.register(User, CustomUserAdmin)
