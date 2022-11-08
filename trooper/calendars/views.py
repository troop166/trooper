from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from trooper.calendars.forms import EventForm
from trooper.calendars.models import Event
from trooper.calendars.utils import get_next_month, get_previous_month


class EventCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Event
    form_class = EventForm
    permission_required = "calendars.add_event"
    success_message = _("<strong>%(title)s</strong> has been added to the calendar.")


class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = "calendars/event_list.html"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.year = None
        self.month = None
        self.today = timezone.now()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["month"] = datetime(year=self.year, month=self.month, day=1).date()
        context["curr_month"] = self.today.date().replace(day=1)
        context["prev_month"] = get_previous_month(self.year, self.month)
        context["next_month"] = get_next_month(self.year, self.month)
        return context

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        try:
            self.month = self.kwargs["month"]
            self.year = self.kwargs["year"]
        except KeyError:
            self.month = self.today.month
            self.year = self.today.year


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event


class EventUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
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
