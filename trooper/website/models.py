from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext as _


class Configuration(models.Model):
    name = models.CharField(_("display name"), max_length=20, default="Trooper")
    domain = models.URLField(
        _("domain name"), help_text=_("The domain name associated with this website")
    )
    description = models.CharField(
        _("description"),
        max_length=255,
        help_text=_("A brief description of this Troop"),
        blank=True,
    )
    logo = models.ImageField(
        _("logo"),
        upload_to="img",
        help_text=_("A recognizable icon to visually identify your Troop"),
        blank=True,
    )

    class Meta:
        verbose_name = _("Configuration")
        verbose_name_plural = _("Configuration")

    def __str__(self):
        return self.domain

    def save(self, **kwargs):
        if self.__class__.objects.exists():
            self.pk = self.__class__.objects.first().pk
        cache.set("configuration", self)
        super().save(**kwargs)

    @classmethod
    def current(cls):
        configuration = cache.get("configuration")
        if configuration:
            return configuration

        configuration = cls.objects.first()
        if configuration:
            cache.set("configuration", configuration)
        return configuration or cls()
