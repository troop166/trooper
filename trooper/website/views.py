from django.http import FileResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET

from trooper.website.models import Configuration


@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)
def favicon(request):
    icon = Configuration.current().logo.file
    return FileResponse(icon)
