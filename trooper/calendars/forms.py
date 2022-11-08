from django import forms

from trooper.calendars.models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("title", "begins_at", "ends_at", "location", "description")
        widgets = {
            "begins_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "ends_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        self.event.organizer = self.user
        if commit:
            self.event.save()
        return self.event
