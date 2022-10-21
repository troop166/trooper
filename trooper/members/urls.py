from django.urls import path

from trooper.members import views

app_name = "members"
urlpatterns = [
    path("", views.MemberListView.as_view(), name="list"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("<slug:username>/", views.MemberDetailView.as_view(), name="detail"),
    path("<slug:username>/edit/", views.MemberUpdateView.as_view(), name="update"),
    path("<slug:username>/delete/", views.MemberDeleteView.as_view(), name="delete"),
]
