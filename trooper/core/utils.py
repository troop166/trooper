from django.http import HttpRequest


def check_for_htmx(request: HttpRequest) -> bool:
    """
    Given a Django HTTP request, check for HTMX.org header.
    """

    return "HX-Request" in request.headers
