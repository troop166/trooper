import logging

from django.contrib.staticfiles import finders
from django.http import FileResponse, Http404
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET
from django.views.generic import DetailView, TemplateView

from trooper.website.models import Page

logger = logging.getLogger(__name__)


@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)
def favicon(request):
    file = finders.find("img/favicon.ico")
    return FileResponse(open(file, "rb"))


@require_GET
@cache_control(max_age=60 * 68 * 24, immutable=True, public=True)
def color_css(request):

    return render(request, "website/css/colors.txt", content_type="text/css")


class HomePageView(TemplateView):
    template_name = "website/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            page = Page.objects.get(is_builtin=Page.BuiltIn.HOME)
        except Page.DoesNotExist:
            page = Page()
            page.title = _("Home")
            logger.warning(
                _("Home page was requested but does not exist in the database!")
            )

        context["page"] = page
        return context


class AboutPageView(TemplateView):
    template_name = "website/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["page"] = Page.objects.get(is_builtin=Page.BuiltIn.ABOUT)
            return context
        except Page.DoesNotExist as e:
            raise Http404 from e


class ContactPageView(TemplateView):
    template_name = "website/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["page"] = Page.objects.get(is_builtin=Page.BuiltIn.CONTACT)
            return context
        except Page.DoesNotExist as e:
            raise Http404 from e


class SignUpPageView(TemplateView):
    template_name = "website/signup.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["page"] = Page.objects.get(is_builtin=Page.BuiltIn.SIGNUP)
            return context
        except Page.DoesNotExist as e:
            raise Http404 from e


class PageDetailView(DetailView):
    model = Page
    template_name = "website/detail.html"

    def get_queryset(self):
        return super().get_queryset().with_visible_content_for(self.request.user)
