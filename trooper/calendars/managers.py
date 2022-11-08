import datetime

from django.db import models
from django.db.models import Q


class EventQuerySet(models.QuerySet):
    def on_date(self, date):
        return self.exclude(
            ends_at__date=date, ends_at__time=datetime.time(0, 0)
        ).filter(
            Q(begins_at__date=date)
            | Q(begins_at__date__lte=date, ends_at__date__gte=date)
        )

    def during_month(self, month):
        return self.filter(
            Q(begins_at__month=month)
            | Q(begins_at__month__lte=month, ends_at__month__gte=month)
        )
