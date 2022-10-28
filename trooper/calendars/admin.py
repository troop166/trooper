from django.contrib import admin

from trooper.calendars.models import Attachment, Category, Event, Invite


class InviteInline(admin.TabularInline):
    model = Invite
    extra = 0


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    auto_complete_fields = ["attachements"]
    date_hierarchy = "begins_at"
    list_display = ("summary", "begins_at", "ends_at", "status")
    list_filter = ("categories", "status", "begins_at")
    search_fields = ("name",)
