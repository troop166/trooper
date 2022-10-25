from django.contrib.staticfiles import finders
from django.http import FileResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView


@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)
def favicon(request):
    file = finders.find("img/favicon.ico")
    return FileResponse(open(file, "rb"))


class HomePageView(TemplateView):
    template_name = "website/index.html"


class AboutPageView(TemplateView):
    template_name = "website/about.html"
