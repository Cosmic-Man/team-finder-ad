from django.conf import settings
from django.db import models

from team_finder.validators import validate_github_url

NAME_MAX_LENGTH = 200


class Project(models.Model):
    OPEN = "open"
    CLOSED = "closed"
    STATUS_CHOICES = [
        (OPEN, "Открыт"),
        (CLOSED, "Закрыт"),
    ]
    STATUS_MAX_LENGTH = max(len(value) for value, _ in STATUS_CHOICES)

    name = models.CharField("Название", max_length=NAME_MAX_LENGTH)
    description = models.TextField("Описание", blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        related_name="owned_projects",
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    github_url = models.URLField(
        "Ссылка на GitHub", blank=True, validators=[validate_github_url]
    )
    status = models.CharField(
        "Статус", max_length=STATUS_MAX_LENGTH, choices=STATUS_CHOICES, default=OPEN
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="Участники",
        related_name="participated_projects",
        blank=True,
    )

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
