from django.contrib import admin

from trooper.website.models import Configuration, Content, Page


class ContentInline(admin.StackedInline):
    model = Content
    extra = 0
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


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    inlines = [ContentInline]
    list_display = ("is_builtin", "title", "slug", "in_navbar")
    list_display_links = ("is_builtin", "title")
    list_filter = ("in_navbar",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ["title"]
