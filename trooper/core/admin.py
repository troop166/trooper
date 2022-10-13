from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _

admin.site.login = login_required(admin.site.login)
admin.site.site_header = _("Trooper Administration")
admin.site.site_title = _("Trooper")
