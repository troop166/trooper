from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext as _
from django.utils.translation import ngettext

from trooper.address_book.admin import AddressInline, EmailInline, PhoneInline
from trooper.core.admin.utils import image_preview
from trooper.members.forms import MemberChangeForm, MemberCreationForm
from trooper.members.models import Family, FamilyMember, Member


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


class MemberFamiliesInline(admin.TabularInline):
    model = FamilyMember
    fields = ["role", "family"]
    autocomplete_fields = ("family",)
    extra = 0
    verbose_name = _("Family")
    verbose_name_plural = _("Families")


class FamilyMembersInline(admin.TabularInline):
    model = FamilyMember
    fields = ["role", "member"]
    autocomplete_fields = ("member",)
    extra = 0
    verbose_name = _("Member")
    verbose_name_plural = _("Members")


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ("__str__", "family_members")
    search_fields = ("members__first_name", "members__nickname", "members__last_name")
    inlines = [FamilyMembersInline]

    def get_queryset(self, request):
        return super().get_queryset(request)

    @admin.display(description=_("Members"))
    def family_members(self, instance):
        parents = instance.family_members.parents()
        children = instance.family_members.children()
        return format_html(
            "<ul>\n<li>{}</li>\n<li>{}</li>\n</ul>",
            format_html(
                "<strong>{}:</strong> {}",
                ngettext("Parent", "Parents", parents.count()),
                ", ".join(p.member.short_name for p in parents),
            ),
            format_html(
                "<strong>{} :</strong> {}",
                ngettext("Child", "Children", children.count()),
                ", ".join(c.member.short_name for c in children),
            ),
        )


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
    inlines = [MemberFamiliesInline, AddressInline, EmailInline, PhoneInline]
    readonly_fields = ("age", "last_login", "preview")
    search_fields = ("first_name", "last_name", "nickname")

    def get_inlines(self, request, obj):
        return super().get_inlines(request, obj) if obj else []

    @staticmethod
    @admin.display(description=_("current"))
    def preview(obj):
        return image_preview(obj.photo.url)
