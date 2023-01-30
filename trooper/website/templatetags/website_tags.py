from django import template
from django.urls import reverse
from django.utils.translation import gettext as _

from trooper.website.models import Page

register = template.Library()


@register.inclusion_tag("website/partials/navbar.html", takes_context=True)
def navbar(context):
    request = context["request"]
    user = context["user"]
    links = []
    pages = Page.objects.in_navbar_for(user)

    if user.is_authenticated:
        links.extend(
            (
                {
                    "title": _("Members"),
                    "url": reverse("members:list"),
                    "is_current": request.resolver_match.app_name == "members",
                },
                {
                    "title": _("Calendar"),
                    "url": reverse("calendars:list"),
                    "is_current": request.resolver_match.app_name == "calendars",
                },
            )
        )
    for page in pages:
        url = page.get_absolute_url()
        link = {
            "title": page.title,
            "url": url,
            "is_current": request.path == url,
        }
        if page.is_builtin == Page.BuiltIn.HOME:
            links.insert(0, link)
        else:
            links.append(link)

    context["navbar"] = {"links": links}
    return context
