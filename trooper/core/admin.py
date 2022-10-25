from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.db import OperationalError, ProgrammingError
from django.utils.translation import gettext as _

from trooper.website.models import Configuration

try:
    name = Configuration.current().name
except (AttributeError, OperationalError, ProgrammingError):
    name = Configuration.name

admin.site.login = login_required(admin.site.login)
admin.site.site_header = _("%s Administration") % name
admin.site.site_title = _("%s") % name
