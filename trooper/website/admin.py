from django.contrib import admin

from trooper.website.models import Configuration


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    def get_actions(self, request):
        """Override Actions menu to remove `Delete` option."""
        return None

    def has_add_permission(self, request):
        """Do not display an `Add` button once one object exits."""
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
