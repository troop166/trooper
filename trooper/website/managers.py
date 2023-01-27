from django.apps import apps
from django.db import models
from django.db.models import Prefetch, Q


class ContentQuerySet(models.QuerySet):
    def public(self):
        return self.filter(
            visibility__in=[
                self.model.Visibility.ANONYMOUS,
                self.model.Visibility.PUBLIC,
            ]
        )

    def private(self):
        return self.filter(visibility=self.model.Visibility.PUBLIC)

    def members(self):
        return self.filter(
            visibility__in=[self.model.Visibility.PUBLIC, self.model.Visibility.MEMBERS]
        )


class ContentManager(models.Manager):
    def get_queryset(self):
        return ContentQuerySet(self.model, using=self._db)

    def visible_to(self, user):
        if user.is_anonymous:
            return self.get_queryset().public()
        # TODO: Add another check for active members
        elif user.is_staff:
            return self.get_queryset().members()
        else:
            return self.get_queryset().private()


def _content_model():
    # Lookup the real model class from the global app registry so this
    # manager method can be used in migrations. This is fine because
    # managers are by definition working on the real model.
    return apps.get_model("website", "content")


class PageQuerySet(models.QuerySet):
    def with_visible_content_for(self, user):
        return self.prefetch_related(
            Prefetch(
                "content",
                queryset=_content_model().objects.visible_to(user),
                to_attr="visible_content",
            ),
            "visible_content__images",
        )

    def visible_to(self, user):
        content = _content_model().objects.visible_to(user).values("pk")
        return self.filter(content__in=content)

    def in_navbar_for(self, user):
        builtin_pages = self.filter(is_builtin__isnull=False, in_navbar=True)
        custom_pages = self.visible_to(user).filter(in_navbar=True).distinct()
        return builtin_pages.union(custom_pages).order_by("navbar_order")
