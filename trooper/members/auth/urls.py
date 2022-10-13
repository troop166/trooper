from django.urls import path

from trooper.members.auth.views import (
    MemberLoginView,
    MemberLogoutView,
    MemberPasswordChangeView,
    MemberPasswordResetConfirmView,
    MemberPasswordResetView,
)

app_name = "auth"
urlpatterns = [
    path(
        "login/",
        MemberLoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        MemberLogoutView.as_view(),
        name="logout",
    ),
    path(
        "password/change/",
        MemberPasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password/reset/",
        MemberPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password/reset/<uidb64>/<token>/",
        MemberPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
