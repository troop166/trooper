from django.urls import path

from trooper.website import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home_page"),
    path("about/", views.AboutPageView.as_view(), name="about_page"),
    path("contact/", views.ContactPageView.as_view(), name="contact_page"),
    path("<slug:slug>/", views.PageDetailView.as_view(), name="detail"),
]
