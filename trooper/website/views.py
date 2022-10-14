from django.contrib.staticfiles import finders
from django.http import FileResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET


@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)
def favicon(request):
    file = finders.find("img/favicon.ico")
    return FileResponse(open(file, "rb"))
