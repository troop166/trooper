from pathlib import Path

from django.core.cache import cache
from django.db import models
from django.db.utils import OperationalError, ProgrammingError
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.text import Truncator, slugify
from django.utils.translation import gettext as _

from colorfield.fields import ColorField

from trooper.website.managers import ContentManager, PageQuerySet


class Configuration(models.Model):

    PRIMARY_PALETTE = [
        ("#ce1126", _("Scouting Red")),
        ("#003f87", _("Scouting Blue")),
        ("#d6cebd", _("Scouting Tan")),
        ("#515354", _("Warm Gray")),
        ("#243e2c", _("Olive")),
        ("#fdc116", _("Gold")),
        ("#ffffff", _("White")),
    ]
    SECONDARY_PALETTE = [
        ("#c54250", _("Light Red")),
        ("#860d1a", _("Dark Red")),
        ("#9ab3d5", _("Pale Blue")),
        ("#003366", _("Dark Blue")),
        ("#e9e9e4", _("Light Tan")),
        ("#ad9d7b", _("Dark Tan")),
        ("#858787", _("Pale Gray")),
        ("#232528", _("Dark Gray")),
    ]
    FULL_PALETTE = PRIMARY_PALETTE + SECONDARY_PALETTE

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
    footer_text = models.TextField(_("footer"), blank=True)

    # Colors
    primary = ColorField(_("Primary Color"), samples=FULL_PALETTE, default="#003f87")
    secondary = ColorField(
        _("Secondary Color"), samples=FULL_PALETTE, default="#515354"
    )
    body_bg = ColorField(
        _("Body Background Color"), samples=FULL_PALETTE, default="#d6cebd"
    )
    navbar_bg = ColorField(
        _("Navbar Background Color"), samples=FULL_PALETTE, default="#243e2c"
    )

    class Meta:
        verbose_name = _("Configuration")
        verbose_name_plural = _("Configuration")

    def __str__(self):
        return self.domain

    def save(self, **kwargs):
        # Ensure only one Configuration exists
        if self.__class__.objects.exists():
            self.pk = self.__class__.objects.first().pk
        # Update the cached version
        cache.set("configuration", self)
        super().save(**kwargs)

    def delete(self, **kwargs):
        super().delete(**kwargs)
        # Delete the cached version
        cache.delete("configuration")

    @classmethod
    def current(cls):
        try:
            configuration = cache.get_or_set("configuration", cls.objects.first())
            return configuration or cls()
        except (OperationalError, ProgrammingError):
            return cls()


class Page(models.Model):
    class BuiltIn(models.TextChoices):
        HOME = "HOME", _("Home Page")
        ABOUT = "ABOUT", _("About Us")
        CONTACT = "CONTACT", _("Contact Form")
        SIGNUP = "SIGNUP", _("Sign Up Form")
        __empty__ = _("custom webpage")

    title = models.CharField(
        _("title"),
        max_length=100,
        help_text=_(
            "The title of this page. Will be shown at the top of the page, "
            "in navigation, and in the browser's title bar."
        ),
    )
    slug = models.SlugField(
        _("slug"),
        unique=True,
        blank=True,
        help_text=_(
            "The part of the page's URL that comes after the slash. Useful "
            "in providing meaningful links."
        ),
    )
    is_builtin = models.CharField(
        _("page"),
        max_length=7,
        choices=BuiltIn.choices,
        unique=True,
        blank=True,
        null=True,
        help_text=_(
            "Some pages, such as the home page, require special treatment. "
            "If this is to be one of those special pages, you can specify "
            "it here."
        ),
    )
    in_navbar = models.BooleanField(
        _("include in navigation"),
        default=True,
        help_text=_(
            "Determines whether this page should appear in the site's "
            "navigation bar."
        ),
    )
    navbar_order = models.PositiveSmallIntegerField(
        _("navigation order"),
        unique=True,
        blank=True,
        null=True,
        help_text=_(
            "Specify the order this page should appear on the site's navigation bar."
        ),
    )
    created_at = models.DateTimeField(
        _("created"),
        auto_now_add=True,
        help_text=_("The date and time this page was first added to the database."),
    )
    last_modified = models.DateTimeField(
        _("modified"),
        auto_now=True,
        help_text=_("The date and time this page was last saved to the database."),
    )

    objects = PageQuerySet.as_manager()

    class Meta:
        ordering = ("navbar_order",)
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")

    def __str__(self):
        return self.title

    def clean(self):
        if self.is_builtin == self.BuiltIn.HOME:
            self.slug = ""
        if not self.slug:
            self.slug = slugify(self.title)

    def get_absolute_url(self):
        if self.is_builtin:
            return reverse(f"{self.is_builtin.lower()}_page")
        else:
            return reverse("detail", kwargs={"slug": self.slug})


class Image(models.Model):
    file = models.ImageField(_("file"), upload_to="website")
    title = models.CharField(_("title"), max_length=150, blank=True)
    description = models.TextField(_("description"), blank=True)

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __str__(self):
        return self.title

    def clean(self):
        if not self.title:
            self.title = Path(self.file.name).stem


class Content(models.Model):
    class Visibility(models.TextChoices):
        ANONYMOUS = "ANONYMOUS", _("Anonymous/Guests")
        PUBLIC = "PUBLIC", _("Everyone")
        MEMBERS = "MEMBERS", _("Members Only")

    class GalleryVariant(models.TextChoices):
        DARK = "carousel-dark", _("Dark")
        __empty__ = _("Light")

    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="content")
    visibility = models.CharField(
        _("visibility"),
        max_length=9,
        choices=Visibility.choices,
        default=Visibility.MEMBERS,
        help_text=_("Controls who will be allowed to view this content."),
    )
    heading = models.CharField(_("heading"), max_length=100, blank=True)
    bookmark = models.SlugField(
        _("bookmark"),
        blank=True,
        help_text=_("Can be used to link directly to this content block on a webpage."),
    )

    body = models.TextField(
        _("body"), help_text=_("The main body of this content block")
    )
    images = models.ManyToManyField(Image, related_name="content", blank=True)
    gallery_controls = models.CharField(
        _("gallery controls"),
        max_length=13,
        choices=GalleryVariant.choices,
        blank=True,
        help_text=_(
            "Choose whether the controls, indicators, and captions are "
            "white or dark. Light controls work best when the images in "
            "the gallery are darker and dark controls appear better "
            "over light colors."
        ),
    )

    objects = ContentManager()

    class Meta:
        order_with_respect_to = "page"
        verbose_name = _("Content Block")
        verbose_name_plural = _("Content Blocks")

    def __str__(self):
        description = self.heading or Truncator(strip_tags(self.body)).words(15)
        return _("%s: %s") % (self.page, description)
