from django.urls import path

from trooper.website import views

urlpatterns = [
    path("favicon.ico", views.favicon),
]
