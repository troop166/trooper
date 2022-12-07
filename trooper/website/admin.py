from django.contrib import admin

from trooper.core.admin.utils import image_preview
from trooper.website.models import Configuration, Content, Image, Page


class ContentInline(admin.StackedInline):
    model = Content
    extra = 0
    filter_horizontal = ["images"]
    # Affected by bug in Django < 4.1
    # https://code.djangoproject.com/ticket/28357
    prepopulated_fields = {"bookmark": ("heading",)}
    radio_fields = {"visibility": admin.HORIZONTAL}


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ("name", "domain")

    def get_actions(self, request):
        """Override Actions menu to remove `Delete` option."""
        return None

    def has_add_permission(self, request):
        """Do not display an `Add` button once one object exits."""
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("title", "file")
    list_display_links = ("title", "file")
    search_fields = ("title", "file")

    readonly_fields = ["preview"]

    @staticmethod
    def preview(obj):
        return image_preview(obj.file.url)


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    inlines = [ContentInline]
    list_display = ("title", "is_builtin", "slug", "in_navbar")
    list_display_links = ("title", "is_builtin", "slug")
    list_filter = ("is_builtin", "in_navbar")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ["title"]
