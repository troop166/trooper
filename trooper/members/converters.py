from django.urls.converters import StringConverter

from trooper.members.models import Member


class FilterConverter(StringConverter):
    VALID_FILTERS = Member.objects.FILTERS_AVAILABLE
    regex = f"({'|'.join(VALID_FILTERS)})"
