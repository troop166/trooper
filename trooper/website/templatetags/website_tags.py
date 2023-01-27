from django import template

from trooper.website.models import Page

register = template.Library()


@register.inclusion_tag("website/partials/navbar.html", takes_context=True)
def navbar(context):
    user = context["user"]
    pages = Page.objects.in_navbar_for(user)
    context["navbar"] = {"links": []}

    for page in pages:
        url = page.get_absolute_url()
        link = {
            "title": page.title,
            "url": url,
            "is_current": context["request"].path == url,
        }
        if page.navbar_order:
            context["navbar"]["links"].insert(page.navbar_order, link)
        else:
            context["navbar"]["links"].append(link)

    return context
