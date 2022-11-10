from django.contrib import admin
from django.utils.safestring import mark_safe

from trooper.website.models import Configuration, Content, Image, Page


class ContentInline(admin.StackedInline):
    model = Content
    extra = 0
    filter_horizontal = ["images"]
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

    def preview(self, obj):
        return mark_safe(  # nosec B308, B703
            '<img src="{url}" width="100%" height="auto" />'.format(
                url=obj.file.url,
            )
        )


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    inlines = [ContentInline]
    list_display = ("is_builtin", "title", "slug", "in_navbar")
    list_display_links = ("is_builtin", "title")
    list_filter = ("in_navbar",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ["title"]
