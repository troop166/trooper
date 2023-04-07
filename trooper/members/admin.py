from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html, format_html_join
from django.utils.translation import gettext as _

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


class MemberAddressInline(admin.StackedInline):
    model = Member.addresses.through
    extra = 0


class MemberEmailInline(admin.TabularInline):
    model = Member.email_addresses.through
    extra = 0


class MemberPhoneInline(admin.TabularInline):
    model = Member.phone_numbers.through
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
        return super().get_queryset(request).count_members()

    @admin.display(description=_("Family Members"))
    def family_members(self, instance):
        member_set = instance.family_members.all()
        return format_html(
            "<ul{}>\n{}\n</ul>",
            " style=margin-left:1.5em;",
            format_html_join(
                "\n",
                "<li><a href={}>{}</a></li>",
                (
                    (
                        reverse(
                            f"admin:{fm.member._meta.app_label}_{fm.member._meta.model_name}_change",  # noqa: E501
                            args=(fm.member_id,),
                        ),
                        fm.member.get_full_name(),
                    )
                    for fm in member_set
                ),
            ),
        )

    @admin.display(description=_("Members"), ordering="member__count")
    def member_count(self, obj):
        return obj.members__count


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
        MemberAddressInline,
        MemberEmailInline,
        MemberPhoneInline,
    ]
    filter_horizontal = (
        "groups",
        "user_permissions",
        "addresses",
    )
    readonly_fields = ("age", "last_login", "preview")
    search_fields = ("first_name", "last_name", "nickname")

    def get_inlines(self, request, obj):
        return super().get_inlines(request, obj) if obj else []

    @staticmethod
    @admin.display(description=_("current photo"))
    def preview(obj):
        return image_preview(obj.photo.url)
