"""
Trooper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/stable/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from django.views import defaults


def ping(*args):
    return JsonResponse({"ping": "pong"})


urlpatterns = [
    # Ping test endpoint
    path("ping/", ping, name="ping"),
    # Django admin
    path("admindocs/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    # Trooper
    path("", include("trooper.members.auth.urls")),
    path("members/", include("trooper.members.urls")),
    path("", include("trooper.website.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns = [
        # Debug error webpages
        path(
            "400/", defaults.bad_request, kwargs={"exception": Exception("Bad Request")}
        ),
        path(
            "403/",
            defaults.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            defaults.page_not_found,
            kwargs={"exception": Exception("Page Not Found")},
        ),
        path("500/", defaults.server_error),
    ] + urlpatterns

    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
