from django.urls import path

from trooper.calendars.feeds import EventFeed
from trooper.calendars.views import (
    EventCreateView,
    EventDeleteView,
    EventDetailView,
    EventListView,
    EventUpdateView,
)

app_name = "calendars"
urlpatterns = [
    path("", EventListView.as_view(), name="list"),
    path("create/", EventCreateView.as_view(), name="create"),
    path("ical/", EventFeed(), name="ical"),
    path("<uuid:uuid>/", EventDetailView.as_view(), name="detail"),
    path("<uuid:uuid>/edit/", EventUpdateView.as_view(), name="update"),
    path("<uuid:uuid>/delete/", EventDeleteView.as_view(), name="delete"),
]
