from trooper.website.models import Configuration, Page


def website(request):
    navbar = {"links": Page.objects.in_navbar_for(request.user)}

    return {
        "navbar": navbar,
        "website": Configuration.current(),
    }
