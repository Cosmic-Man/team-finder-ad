from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from team_finder.validators import validate_github_url
from .constants import (
    ABOUT_MAX_LENGTH,
    NAME_MAX_LENGTH,
    PHONE_MAX_LENGTH,
    SKILL_NAME_MAX_LENGTH,
)
from .managers import UserManager
from .utils import generate_avatar


class Skill(models.Model):
    name = models.CharField("Название", max_length=SKILL_NAME_MAX_LENGTH, unique=True)

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"
        ordering = ["name"]

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Email", unique=True)
    name = models.CharField("Имя", max_length=NAME_MAX_LENGTH)
    surname = models.CharField("Фамилия", max_length=NAME_MAX_LENGTH)
    avatar = models.ImageField("Аватар", upload_to="avatars/")
    phone = models.CharField(
        "Телефон", max_length=PHONE_MAX_LENGTH, unique=True, blank=True, null=True
    )
    github_url = models.URLField(
        "Ссылка на GitHub", blank=True, validators=[validate_github_url]
    )
    about = models.TextField("О себе", max_length=ABOUT_MAX_LENGTH, blank=True)
    skills = models.ManyToManyField(
        Skill, verbose_name="Навыки", related_name="users", blank=True
    )
    is_active = models.BooleanField("Активен", default=True)
    is_staff = models.BooleanField("Администратор", default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["name", "surname"]

    def __str__(self):
        return f"{self.name} {self.surname}"

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = generate_avatar(self.name)
        super().save(*args, **kwargs)
