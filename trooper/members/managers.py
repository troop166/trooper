from django.contrib.auth.models import UserManager
from django.db import models
from django.db.models import Count, Prefetch, Q


class FamilyQuerySet(models.QuerySet):
    def count_members(self):
        return self.annotate(Count("members"))


class MemberQuerySet(models.QuerySet):
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


class MemberManager(UserManager):
    def get_queryset(self):
        return MemberQuerySet(self.model, using=self._db)

    def with_published_contact_info(self):
        return self.get_queryset().with_published_contact_info()

    def get_by_natural_key(self, username):
        return self.get(
            Q(**{f"{self.model.USERNAME_FIELD}__iexact": username})
            | Q(**{f"{self.model.EMAIL_FIELD}__iexact": username})
        )
