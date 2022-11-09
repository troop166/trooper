from django.apps import apps
from django.db import models
from django.db.models import Count, Exists, FilteredRelation, Prefetch


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

    def members_only(self):
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
        # elif user.is_active_member():
        #     pass
        else:
            return self.get_queryset().private()


class PageQuerySet(models.QuerySet):
    def with_visible_content_for(self, user):
        Content = apps.get_model("website", "content")
        return self.prefetch_related(
            Prefetch(
                "content",
                queryset=Content.objects.visible_to(user),
                to_attr="visible_content",
            ),
            "visible_content__images",
        )

    def visible_to(self, user):
        Content = apps.get_model("website", "content")
        content = Content.objects.visible_to(user).values("pk")
        return self.filter(Exists(content))

    def in_navbar_for(self, user):
        return self.visible_to(user).filter(in_navbar=True)
