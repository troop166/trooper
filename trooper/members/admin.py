from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

from trooper.core.admin.utils import change_list, image_preview
from trooper.members.forms import MemberChangeForm, MemberCreationForm
from trooper.members.models import (
    Address,
    EmailAddress,
    Family,
    FamilyMember,
    Member,
    PhoneNumber,
)


class MemberAgeRangeFilter(admin.SimpleListFilter):
    title = _("Age Range")
    parameter_name = "range"

    def lookups(self, request, model_admin):
        return (
            ("adults", _("Adults")),
            ("youths", _("Youths")),
        )

    def queryset(self, request, queryset):
        if self.value() == "adults":
            return queryset.adults()
        if self.value() == "youths":
            return queryset.youths()


class AddressInline(admin.StackedInline):
    model = Address
    extra = 0
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "label",
                    ("street", "street2"),
                    ("city", "state", "zip_code"),
                    "is_published",
                )
            },
        ),
    )


class EmailAddressInline(admin.TabularInline):
    model = EmailAddress
    extra = 0


class PhoneNumberInline(admin.TabularInline):
    model = PhoneNumber
    extra = 0


class FamilyMemberInline(admin.TabularInline):
    model = FamilyMember
    fields = ["role", "family"]
    autocomplete_fields = ("family",)
    extra = 0
    verbose_name = _("Family")
    verbose_name_plural = _("Families")


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ("__str__", "member_count")
    search_fields = ("members__first_name", "members__nickname", "members__last_name")
    readonly_fields = ("family_members",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.with_member_count()

    @admin.display(description=_("Family Members"))
    def family_members(self, obj):
        members = obj.members.all()
        return change_list(members) if members else self.get_empty_value_display()

    @admin.display(description=_("Members"), ordering="member_count")
    def member_count(self, obj):
        return obj.member_count


@admin.register(Member)
class MemberAdmin(UserAdmin):
    add_form = MemberCreationForm
    form = MemberChangeForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "middle_name",
                    "last_name",
                    "suffix",
                    "nickname",
                    "gender",
                    ("photo", "preview"),
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Important dates"),
            {
                "fields": (
                    "date_of_birth",
                    "date_of_death",
                    "age",
                    "last_login",
                    "date_joined",
                ),
                "classes": ("collapse",),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    ("first_name", "last_name", "suffix"),
                    "nickname",
                    "gender",
                    "date_of_birth",
                    ("password1", "password2"),
                ),
            },
        ),
    )
    list_display = ("first_name", "middle_name", "last_name", "suffix", "is_staff")
    list_display_links = ("first_name", "last_name")
    list_filter = (MemberAgeRangeFilter, "is_staff", "is_superuser", "is_active")
    inlines = [
        FamilyMemberInline,
        AddressInline,
        EmailAddressInline,
        PhoneNumberInline,
    ]
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    readonly_fields = ("age", "last_login", "preview")
    search_fields = ("first_name", "last_name", "nickname")

    def get_inlines(self, request, obj):
        return super().get_inlines(request, obj) if obj else []

    @staticmethod
    @admin.display(description=_("current photo"))
    def preview(obj):
        return image_preview(obj.photo.url)
