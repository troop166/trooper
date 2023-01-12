import calendar

from django import template

register = template.Library()


@register.inclusion_tag("calendars/partials/month.html", takes_context=True)
def calendar_month(context, month):
    c = calendar.Calendar(firstweekday=calendar.SUNDAY)
    context["calendar"] = {
        "days_of_the_week": (
            {"name": calendar.day_name[d], "abbr": calendar.day_abbr[d]}
            for d in c.iterweekdays()
        ),
        "month": month.month,
        "name": calendar.month_name[month.month],
        "weeks": c.monthdatescalendar(year=month.year, month=month.month),
        "year": month.year,
    }
    return context


@register.inclusion_tag("calendars/partials/event_list.html", takes_context=True)
def events_on(context, date):
    qs = context["event_list"]
    context["events"] = qs.on_date(date)
    context["date"] = date
    return context
