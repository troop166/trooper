from django.urls import path

from trooper.address_book.views import (
    AddressCreateView,
    AddressDeleteView,
    AddressDetailView,
    AddressUpdateView,
    address_delete_view,
    address_form_view,
)

app_name = "address_book"
urlpatterns = [
    path(
        "<slug:username>/address/add/",
        AddressCreateView.as_view(),
        name="address_create",
    ),
    path(
        "<slug:username>/address/<int:pk>/",
        AddressDetailView.as_view(),
        name="address_form",
    ),
    path(
        "<slug:username>/address/<int:pk>/edit",
        AddressUpdateView.as_view(),
        name="address_update",
    ),
    path(
        "<slug:username>/address/<int:pk>/delete/",
        AddressDeleteView.as_view(),
        name="address_delete",
    ),
]
