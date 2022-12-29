from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from accounts.models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    Custom user class-based administration panel for managing custom users in
    the Django admin site.
    This class extends the built-in Django 'UserAdmin' class and is used to
    register a custom user model and custom forms for creating and editing user
    instances in the Django admin site.
    """
    # Custom form for creating new users in the Django Admin Panel
    add_form = CustomUserCreationForm
    # Custom form for changing a user's information in the Django Admin Panel
    form = CustomUserChangeForm
    # Custom user model used by Django
    model = CustomUser
    # Fields to display in the user list view of the Django Admin Panel
    list_display = [
        'email',
        'username',
        'age',
        'is_staff'
    ]
    # Fields to display on the user change form in the Django Admin Panel
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('age', )}),
    )
    # Fields to display on the user creation form in the Django Admin Panel
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('age', )}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
