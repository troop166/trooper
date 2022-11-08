from calendar import HTMLCalendar

from django.urls import reverse


class EventCalendar(HTMLCalendar):
    cssclass_date = "date"
    cssclass_month = "table table-light calendar month"
    cssclass_month_head = "table-primary"
    cssclass_noday = "table-secondary"
    cssclasses = [
        "mon",
        "tue",
        "wed",
        "thu",
        "fri",
        "sat table-secondary",
        "sun table-secondary",
    ]
    cssclasses_weekday_head = ["table-secondary" for _ in range(7)]
    cssclass_event = "list-entry mb-2"
    cssclass_event_link = "text-decoration-none"
    cssclass_event_list = "list-unstyled"

    def __init__(self, firstweekday=0, events=None):
        super().__init__(firstweekday)
        self.events = events

    def formatevents(self, day):
        """
        Return a list of Events that correspond with a day.
        """
        events_on_day = self.events.filter(begins_at__day=day)
        if events_on_day:
            e = '<ul class="%s">' % self.cssclass_event_list
            for event in events_on_day:
                event_display = (
                    f'{event.begins_at.time().strftime("%I%p")}: {event.title}'
                )
                event_link = '<a href="{}" class="{}">{}</a>'.format(
                    event.get_absolute_url(),
                    self.cssclass_event_link,
                    event_display,
                )
                e += f'<li class="{self.cssclass_event}">{event_link}</li>'
                e += "\n"
            e += "</ul>"
            return e

    def formatday(self, day, weekday):
        """
        Return a day as a table cell.
        """
        if day == 0:
            # day outside month
            return '<td class="%s"></td>' % self.cssclass_noday

        smore = self.formatevents(day)
        s = '<span class="%s">%d</span>' % (self.cssclass_date, day)
        s += smore or ""
        return f'<td class="{self.cssclasses[weekday]}">{s}</td>'


def _prevmonth(year, month):
    if month == 1:
        return year - 1, 12
    else:
        return year, month - 1


def _nextmonth(year, month):
    if month == 12:
        return year + 1, 1
    else:
        return year, month + 1


def get_next_month(year=None, month=None):
    """
    Given a month and a year, return a link to the following month.
    """
    next_year, next_month = _nextmonth(year, month)
    return reverse("calendars:month", kwargs={"month": next_month, "year": next_year})


def get_previous_month(year=None, month=None):
    """
    Given a month and a year, return a link to the prior month.
    """
    previous_year, previous_month = _prevmonth(year, month)
    return reverse(
        "calendars:month",
        kwargs={"month": previous_month, "year": previous_year},
    )
