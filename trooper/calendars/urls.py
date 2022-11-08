from django.urls import path, register_converter

from trooper.calendars.converters import MonthConverter, YearConverter
from trooper.calendars.feeds import EventFeed
from trooper.calendars.views import (
    EventCreateView,
    EventDeleteView,
    EventDetailView,
    EventListView,
    EventUpdateView,
)

register_converter(MonthConverter, "mm")
register_converter(YearConverter, "yyyy")

app_name = "calendars"
urlpatterns = [
    path("", EventListView.as_view(), name="list"),
    path("<yyyy:year>/<mm:month>/", EventListView.as_view(), name="month"),
    path("create/", EventCreateView.as_view(), name="create"),
    path("ical/", EventFeed(), name="ical"),
    path("<uuid:pk>/", EventDetailView.as_view(), name="detail"),
    path("<uuid:pk>/edit/", EventUpdateView.as_view(), name="update"),
    path("<uuid:pk>/delete/", EventDeleteView.as_view(), name="delete"),
]
