from django.db import models
from django.db.models import Count, Q
from django.utils import timezone


class CommitteeQuerySet(models.QuerySet):
    def count_members(self):
        today = timezone.now()
        return self.annotate(
            member_count=Count(
                "committee_member",
                filter=Q(
                    Q(committee_member__start__lte=today),
                    Q(committee_member__end__gte=today)
                    | Q(committee_member__end__isnull=True),
                ),
            )
        )


class PatrolQuerySet(models.QuerySet):
    def count_members(self):
        today = timezone.now()
        return self.annotate(
            member_count=Count(
                "patrol_member",
                filter=Q(
                    Q(patrol_member__start__lte=today),
                    Q(patrol_member__end__gte=today)
                    | Q(patrol_member__end__isnull=True),
                ),
            )
        )
