from django.contrib import admin, messages
from django.utils.translation import gettext as _
from django.utils.translation import ngettext

from trooper.calendars.models import Attachment, Category, Event, Invite


class InviteInline(admin.TabularInline):
    """
    Inline admin class for managing invites.

    Attributes:
        model (Model): The model associated with the inline admin.
        autocomplete_fields (tuple): Fields to enable autocomplete for.
        extra (int): Number of extra forms to display.
        readonly_fields (tuple): Fields that are read-only.

    """

    model = Invite
    autocomplete_fields = ("attendee",)
    extra = 0
    readonly_fields = ("status",)


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    """
    Model admin class for managing attachments.

    Attributes:
        search_fields (list): Fields to enable search functionality.

    """

    search_fields = ["title", "file"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    Model admin class for managing categories.

    Attributes:
        search_fields (list): Fields to enable search functionality.

    """

    actions = ("cancel_selected", "confirm_selected", "mark_tentative_selected")
    autocomplete_fields = ["categories", "organizer"]
    date_hierarchy = "begins_at"
    filter_horizontal = ["attachments"]
    inlines = [InviteInline]
    list_display = ("title", "begins_at", "ends_at", "status", "duration")
    list_filter = ("categories", "status", "begins_at")
    readonly_fields = ("duration",)
    radio_fields = {"status": admin.HORIZONTAL}
    search_fields = ("name",)

    def get_changeform_initial_data(self, request):
        """
        Get the initial data for the change form.

        Args:
            self: The instance of the class.
            request (HttpRequest): The HTTP request object.

        Returns:
            dict: The initial data for the change form.

        """
        return {"organizer": request.user}

    @admin.action(description=_("Cancel selected Events"), permissions=["change"])
    def cancel_selected(self, request, queryset):
        """
        Action method to cancel selected events.

        Args:
            self: The instance of the class.
            request (HttpRequest): The HTTP request object.
            queryset (QuerySet): The queryset containing the selected events.

        Returns:
            None

        """
        events = queryset.update(status=Event.Status.CANCELLED)
        self.message_user(
            request,
            ngettext(
                "%d event was successfully canceled.",
                "%d events were successfully canceled.",
                events,
            )
            % events,
            messages.WARNING,
        )

    @admin.action(description=_("Confirm selected Events"), permissions=["change"])
    def confirm_selected(self, request, queryset):
        """
        Action method to confirm selected events.

        Args:
            self: The instance of the class.
            request (HttpRequest): The HTTP request object.
            queryset (QuerySet): The queryset containing the selected events.

        Returns:
            None

        """
        events = queryset.update(status=Event.Status.CONFIRMED)
        self.message_user(
            request,
            ngettext(
                "%d event was successfully confirmed.",
                "%d events were successfully confirmed.",
                events,
            )
            % events,
            messages.SUCCESS,
        )

    @admin.action(
        description=_("Mark selected Events as tentative"), permissions=["change"]
    )
    def mark_tentative_selected(self, request, queryset):
        """
        Action method to mark selected events as tentative.

        Args:
            self: The instance of the class.
            request (HttpRequest): The HTTP request object.
            queryset (QuerySet): The queryset containing the selected events.

        Returns:
            None

        """
        events = queryset.update(status=Event.Status.TENTATIVE)
        self.message_user(
            request,
            ngettext(
                "%d event was successfully marked tentative.",
                "%d events were successfully marked tentative.",
                events,
            )
            % events,
            messages.INFO,
        )
