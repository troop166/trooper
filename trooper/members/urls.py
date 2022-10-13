from django.urls import path

from trooper.members.views import SignupView

app_name = "members"
urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
]
