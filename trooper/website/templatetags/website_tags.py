from django import template

from trooper.website.models import Page

register = template.Library()


@register.inclusion_tag("website/partials/navbar.html", takes_context=True)
def navbar(context):
    user = context["user"]
    links = Page.objects.in_navbar_for(user)

    context["navbar"] = {"links": links}
    return context
