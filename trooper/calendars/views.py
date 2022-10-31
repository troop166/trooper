from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import (
    CreateView,
    DayArchiveView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from trooper.calendars.models import Event


class EventCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Event
    permission_required = "calendars.add_event"
    success_message = _("<strong>%(title)s</strong> has been added to the calendar.")


class EventListView(LoginRequiredMixin, ListView):
    model = Event


class EventDetailView(LoginRequiredMixin, ListView):
    model = Event


class EventUpdateView(PermissionRequiredMixin, SuccessMessageMixin, DetailView):
    model = Event
    permission_required = "calendars.change_event"
    success_message = _("<strong>%(title)s</strong> has been updated.")


class EventDeleteView(PermissionRequiredMixin, DeleteView):
    model = Event
    permission_required = "calendars.delete_event"
    success_url = reverse_lazy("calendars:list")

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        success_message = _(
            "<strong>%(title)s</strong> has been permanently removed from the database."
        )
        messages.warning(request, success_message, "danger")
