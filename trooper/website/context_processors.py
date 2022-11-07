from trooper.website.models import Configuration, Page


def website(request):
    return {
        "navbar": {
            "links": Page.objects.filter(in_navbar=True).values(
                "title", "slug", "is_builtin"
            )
        },
        "website": Configuration.current(),
    }
