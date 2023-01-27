from django import template

from trooper.website.models import Page

register = template.Library()


@register.inclusion_tag("website/partials/navbar.html", takes_context=True)
def navbar(context):
    user = context["user"]
    pages = Page.objects.in_navbar_for(user)
    context["navbar"] = {"links": []}

    for page in pages:
        context["navbar"]["links"].append(
            {
                "title": page.title,
                "url": page.get_absolute_url(),
                "is_current": context["request"].path == page.get_absolute_url(),
            }
        )

    return context
