from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from team_finder.utils import json_error, paginate
from .forms import ProjectForm
from .models import Project


def project_list(request):
    project_queryset = Project.objects.select_related("owner").prefetch_related(
        "participants"
    )
    page_obj = paginate(request, project_queryset)
    context = {"projects": page_obj.object_list, "page_obj": page_obj}
    return render(request, "projects/project_list.html", context)


def project_detail(request, project_pk):
    project = get_object_or_404(
        Project.objects.select_related("owner").prefetch_related("participants"),
        pk=project_pk,
    )
    return render(request, "projects/project-details.html", {"project": project})


@login_required
def create_project(request):
    form = ProjectForm(request.POST or None)
    if not form.is_valid():
        return render(
            request, "projects/create-project.html", {"form": form, "is_edit": False}
        )
    project = form.save(commit=False)
    project.owner = request.user
    project.save()
    project.participants.add(request.user)
    return redirect("projects:detail", project_pk=project.pk)


@login_required
def edit_project(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if project.owner != request.user:
        return redirect("projects:detail", project_pk=project_pk)
    form = ProjectForm(request.POST or None, instance=project)
    if not form.is_valid():
        return render(
            request, "projects/create-project.html", {"form": form, "is_edit": True}
        )
    form.save()
    return redirect("projects:detail", project_pk=project_pk)


@login_required
@require_POST
def complete_project(request, project_pk):
    project = Project.objects.filter(pk=project_pk).first()
    if project is None:
        return json_error("Проект не найден", HTTPStatus.NOT_FOUND)
    if project.owner != request.user:
        return json_error(
            "Завершить проект может только его автор", HTTPStatus.FORBIDDEN
        )
    if project.status != Project.OPEN:
        return json_error("Проект уже закрыт", HTTPStatus.FORBIDDEN)
    project.status = Project.CLOSED
    project.save(update_fields=["status"])
    return JsonResponse({"status": "ok", "project_status": project.status})


@login_required
@require_POST
def toggle_participate(request, project_pk):
    project = Project.objects.filter(pk=project_pk).first()
    if project is None:
        return json_error("Проект не найден", HTTPStatus.NOT_FOUND)
    is_participant = project.participants.filter(pk=request.user.pk).exists()
    if project.status != Project.OPEN and not is_participant:
        return json_error(
            "Нельзя присоединиться к закрытому проекту", HTTPStatus.CONFLICT
        )
    if is_participant:
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)
    return JsonResponse({"status": "ok", "participant": not is_participant})
