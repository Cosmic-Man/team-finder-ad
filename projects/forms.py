from django import forms

from .models import Project

STATUS_LABELS = ((Project.OPEN, "Открыт"), (Project.CLOSED, "Закрыт"))


class ProjectForm(forms.ModelForm):
    status = forms.ChoiceField(label="Статус", choices=STATUS_LABELS)

    class Meta:
        model = Project
        fields = ("name", "description", "github_url", "status")
