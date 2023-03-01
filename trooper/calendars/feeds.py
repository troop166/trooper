from django.conf import settings
from django.utils.translation import gettext as _

from django_ical.utils import build_rrule_from_recurrences_rrule
from django_ical.views import ICalFeed

from trooper.calendars.models import Event
from trooper.website.models import Configuration


class EventFeed(ICalFeed):
    website = Configuration.current()

    product_id = f"-//{website.name}/ical/{settings.LANGUAGE_CODE}"
    timezone = settings.TIME_ZONE
    title = website.name
    description = _("A calendar of events crafted specifically for you")

    def get_object(self, request, *args, **kwargs):
        self.website = request.headers["host"]
        return super().get_object(request, *args, **kwargs)

    def items(self):
        return Event.objects.all().order_by("-begins_at")

    def item_guid(self, item):
        return f"{item.uuid}@{self.website}"

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_location(self, item):
        return item.location

    def item_link(self, item):
        return item.get_absolute_url()

    def item_start_datetime(self, item):
        return item.begins_at

    def item_end_datetime(self, item):
        return item.ends_at

    def item_organizer(self, item):
        return "YES"

    def item_rrule(self, item):
        if item.recurrences:
            rules = []
            for rule in item.recurrences.rrules:
                rules.append(build_rrule_from_recurrences_rrule(rule))
            return rules

    def item_exrule(self, item):
        if item.recurrences:
            rules = []
            for rule in item.recurrences.exrules:
                rules.append(build_rrule_from_recurrences_rrule(rule))
            return rules

    def item_rdate(self, item):
        if item.recurrences:
            return item.recurrences.rdates

    def item_exdate(self, item):
        if item.recurrences:
            return item.recurrences.exdates

    def item_created(self, item):
        return item.created_at

    def item_updateddate(self, item):
        return item.last_modified

    def item_categories(self, item):
        return item.categories.values_list("name", flat=True)

    def item_status(self, item):
        return item.status
