from django.urls.converters import IntConverter


class MonthConverter(IntConverter):
    regex = "(1[0-2]|0?[1-9])"


class YearConverter(IntConverter):
    regex = "(19|2[0-9])[0-9]{2}"
