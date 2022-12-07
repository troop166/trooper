from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _

from trooper.website.models import Configuration

site_name = Configuration.current().name

admin.site.login = login_required(admin.site.login)
admin.site.site_header = _("%s Administration") % site_name
admin.site.site_title = _("%s") % site_name
