from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

from .models import Skill

User = get_user_model()


class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "name", "surname")


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = AdminUserCreationForm
    list_display = ("id", "email", "name", "surname", "is_active", "is_staff")
    list_filter = ("is_active", "is_staff")
    search_fields = ("email", "name", "surname")
    ordering = ("id",)
    filter_horizontal = ("skills",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Профиль",
            {"fields": ("name", "surname", "avatar", "about", "phone", "github_url")},
        ),
        ("Навыки", {"fields": ("skills",)}),
        ("Права", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (None, {"fields": ("email", "name", "surname", "password1", "password2")}),
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    search_fields = ("name",)
