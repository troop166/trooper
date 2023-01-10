import operator
from functools import reduce

from django.contrib.auth.models import UserManager
from django.db import models
from django.db.models import Case, Count, Prefetch, Q, When
from django.db.models.functions import Coalesce
from django.utils import timezone


def _eighteen_years_from(date=None):
    if not date:
        date = timezone.now()
    return date.replace(year=date.year - 18)


class FamilyQuerySet(models.QuerySet):
    def count_members(self):
        return self.annotate(Count("members"))


class MemberQuerySet(models.QuerySet):
    def search(self, query=None):
        if not query:
            return self.none()
        query_words = query.split()
        if not query_words:
            return self.none()
        fields = (
            "first_name",
            "last_name",
            "nickname",
            "email_addresses__address",
            "phone_numbers__number",
        )
        lookups = []
        for word in query_words:
            lookups.extend(Q(**{f"{field}__icontains": word}) for field in fields)
        return self.filter(reduce(operator.or_, lookups))

    def with_name(self):
        return self.annotate(
            short_name=Coalesce(
                Case(
                    When(nickname="", then=None),
                    default="nickname",
                    output_field=models.CharField(),
                ),
                "first_name",
            )
        )

    def with_published_contact_info(self):
        return self.prefetch_related(
            Prefetch(
                "addresses",
                queryset=self.model.addresses.rel.model.objects.published(),
                to_attr="published_addresses",
            ),
            Prefetch(
                "email_addresses",
                queryset=self.model.email_addresses.rel.model.objects.published(),
                to_attr="published_email_addresses",
            ),
            Prefetch(
                "phone_numbers",
                queryset=self.model.phone_numbers.rel.model.objects.published(),
                to_attr="published_phone_numbers",
            ),
        )

    def adults(self):
        return self.filter(date_of_birth__lte=_eighteen_years_from(timezone.now()))

    def youths(self):
        return self.filter(date_of_birth__gt=_eighteen_years_from(timezone.now()))


class MemberManager(UserManager):
    def get_queryset(self):
        return MemberQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)

    def with_name(self):
        return self.get_queryset().with_name()

    def with_published_contact_info(self):
        return self.get_queryset().with_published_contact_info()

    def get_by_natural_key(self, username):
        return self.get(
            Q(**{f"{self.model.USERNAME_FIELD}__iexact": username})
            | Q(email_addresses__address__iexact=username)
        )

    def adults(self):
        return self.get_queryset().adults()

    def youths(self):
        return self.get_queryset().youths()
