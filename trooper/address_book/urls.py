from django.urls import path

from trooper.address_book.views import address_delete_view, address_form_view

app_name = "address_book"
urlpatterns = [
    path("address/", address_form_view, name="address_create_form"),
    path("address/<int:pk>/", address_form_view, name="address_form"),
    path("address/<int:pk>/delete/", address_delete_view, name="address_delete"),
]
