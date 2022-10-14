from django.urls import path
from django.views.generic import TemplateView

from trooper.website import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="website/index.html"), name="home"),
    path("favicon.ico", views.favicon),
    path(
        "about/", TemplateView.as_view(template_name="website/about.html"), name="about"
    ),
]
