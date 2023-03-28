import operator
from functools import reduce

from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.db import models
from django.db.models import Count, Prefetch, Q
from django.utils import timezone

from trooper.members.utils import eighteen_years_from


class FamilyQuerySet(models.QuerySet):
    def count_members(self):
        return self.annotate(Count("members"))


class FamilyMemberQuerySet(models.QuerySet):
    def children(self):
        return self.filter(role=self.model.Role.CHILD)

    def parents(self):
        return self.filter(role=self.model.Role.PARENT)


class MemberQuerySet(models.QuerySet):
    FILTERS_AVAILABLE = ("adults", "youths")

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
        return self.filter(reduce(operator.or_, lookups)).distinct()

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
        return self.filter(date_of_birth__lte=eighteen_years_from(timezone.now()))

    def youths(self):
        return self.filter(date_of_birth__gt=eighteen_years_from(timezone.now()))


class MemberManager(UserManager):
    FILTERS_AVAILABLE = MemberQuerySet.FILTERS_AVAILABLE

    def get_queryset(self):
        return MemberQuerySet(self.model, using=self._db)

    def _create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given username and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, password, **extra_fields)

    def search(self, query):
        return self.get_queryset().search(query)

    def with_published_contact_info(self):
        return self.get_queryset().with_published_contact_info()

    def get_by_natural_key(self, username):
        fields = ["email_addresses__address", "username"]
        lookups = [Q(**{f"{field}__iexact": username}) for field in fields]
        return (
            self.get_queryset().filter(reduce(operator.or_, lookups)).distinct().get()
        )

    def adults(self):
        return self.get_queryset().adults()

    def youths(self):
        return self.get_queryset().youths()
