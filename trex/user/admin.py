from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()
# from .models import User
# Register your models here.


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "role",
        "first_name",
        "last_name",
    )
    list_filter = (
        "role",
        "is_staff",
        "is_superuser",
        "is_active",
    )
    fieldsets = (
        ('Auth', {"fields": ("username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "avatar",
                    "gender",
                    "role",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                )
            },
        ),
    )
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

