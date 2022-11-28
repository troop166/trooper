from django.urls.converters import IntConverter


class MonthConverter(IntConverter):
    # Matches MM from 1-12 with optional leading zero
    regex = "(1[0-2]|0?[1-9])"


class YearConverter(IntConverter):
    # Matches YYYY from 1900-2999
    regex = "(19|2[0-9])[0-9]{2}"
