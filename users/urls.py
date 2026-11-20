from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("list/", views.user_list, name="list"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("change-password/", views.change_password, name="change_password"),
    path("skills/", views.skill_search, name="skill_search"),
    path("<int:user_pk>/", views.user_detail, name="detail"),
    path("<int:user_pk>/skills/add/", views.add_skill, name="add_skill"),
    path(
        "<int:user_pk>/skills/<int:skill_id>/remove/",
        views.remove_skill,
        name="remove_skill",
    ),
]
