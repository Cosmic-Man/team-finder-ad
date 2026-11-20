import json
from http import HTTPStatus
from urllib.parse import urlencode

from django.contrib.auth import get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from team_finder.utils import json_error, paginate
from .forms import LoginForm, ProfileForm, RegisterForm
from .models import SKILL_NAME_MAX_LENGTH, Skill

User = get_user_model()

SKILLS_LIMIT = 10


def register(request):
    form = RegisterForm(request.POST or None)
    if not form.is_valid():
        return render(request, "users/register.html", {"form": form})
    user = form.save()
    login(request, user)
    return redirect("projects:list")


def login_view(request):
    form = LoginForm(request.POST or None)
    if not form.is_valid():
        return render(request, "users/login.html", {"form": form})
    login(request, form.user)
    return redirect("projects:list")


def logout_view(request):
    logout(request)
    return redirect("projects:list")


def user_list(request):
    participants = User.objects.all()
    active_skill = request.GET.get("skill", "")
    query_prefix = ""
    if active_skill:
        participants = participants.filter(skills__name=active_skill)
        query_prefix = urlencode({"skill": active_skill}) + "&"

    page_obj = paginate(request, participants)
    context = {
        "participants": page_obj.object_list,
        "page_obj": page_obj,
        "all_skills": Skill.objects.values_list("name", flat=True),
        "active_skill": active_skill,
        "query_prefix": query_prefix,
    }
    return render(request, "users/participants.html", context)


def user_detail(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    return render(request, "users/user-details.html", {"user": user})


@login_required
def edit_profile(request):
    form = ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user,
    )
    if not form.is_valid():
        return render(request, "users/edit_profile.html", {"form": form})
    form.save()
    return redirect("users:detail", user_pk=request.user.pk)


@login_required
def change_password(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if not form.is_valid():
        return render(request, "users/change_password.html", {"form": form})
    user = form.save()
    update_session_auth_hash(request, user)
    return redirect("users:detail", user_pk=user.pk)


def skill_search(request):
    search_query = request.GET.get("q", "").strip()
    matching_skills = Skill.objects.filter(
        name__istartswith=search_query
    ).values("id", "name")
    return JsonResponse(list(matching_skills[:SKILLS_LIMIT]), safe=False)


@login_required
@require_POST
def add_skill(request, user_pk):
    if request.user.pk != user_pk:
        return json_error("Нет доступа", HTTPStatus.FORBIDDEN)
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return json_error("Некорректный запрос", HTTPStatus.BAD_REQUEST)
    if not isinstance(payload, dict):
        return json_error("Некорректный запрос", HTTPStatus.BAD_REQUEST)

    created = False
    if payload.get("skill_id"):
        skill = Skill.objects.filter(pk=payload["skill_id"]).first()
        if skill is None:
            return json_error("Навык не найден", HTTPStatus.NOT_FOUND)
    else:
        skill_name = payload.get("name", "")
        if not isinstance(skill_name, str):
            return json_error("Некорректное название", HTTPStatus.BAD_REQUEST)
        skill_name = skill_name.strip()
        if not skill_name or len(skill_name) > SKILL_NAME_MAX_LENGTH:
            return json_error("Некорректное название", HTTPStatus.BAD_REQUEST)
        skill, created = Skill.objects.get_or_create(name=skill_name)

    added = not request.user.skills.filter(pk=skill.pk).exists()
    if added:
        request.user.skills.add(skill)
    return JsonResponse(
        {
            "skill_id": skill.pk,
            "created": created,
            "added": added,
            "id": skill.pk,
            "name": skill.name,
        }
    )


@login_required
@require_POST
def remove_skill(request, user_pk, skill_id):
    if request.user.pk != user_pk:
        return json_error("Нет доступа", HTTPStatus.FORBIDDEN)
    skill = request.user.skills.filter(pk=skill_id).first()
    if skill is None:
        return json_error("Навык не найден", HTTPStatus.NOT_FOUND)
    request.user.skills.remove(skill)
    return JsonResponse({"status": "ok"})
