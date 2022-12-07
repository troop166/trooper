from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from trooper.address_book.admin import AddressInline, EmailInline, PhoneInline
from trooper.core.admin.utils import image_preview
from trooper.members.forms import MemberChangeForm, MemberCreationForm
from trooper.members.models import Family, FamilyMember, Member


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
    search_fields = ("members__first_name", "members__last_name")
    readonly_fields = ("family_members",)

    def get_queryset(self, request):
        return super().get_queryset(request).count_members()

    @admin.display(description=_("Family Members"))
    def family_members(self, instance):
        return format_html_join(
            mark_safe("<br>"),  # nosec: B308
            "<a href={}>{}</a>",
            (
                (
                    reverse(
                        f"admin:{member._meta.app_label}_{member._meta.model_name}_change",  # noqa: E501
                        args=(member.pk,),
                    ),
                    member,
                )
                for member in instance.members.all()
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
                    "last_name",
                    "suffix",
                    "nickname",
                    "email",
                    ("avatar", "preview"),
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
            },
        ),
        (
            _("Important dates"),
            {"fields": ("date_of_birth", "age", "last_login", "date_joined")},
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
                    "date_of_birth",
                    ("password1", "password2"),
                ),
            },
        ),
    )
    list_display = ("short_name", "last_name", "suffix", "is_staff")
    list_display_links = ("short_name", "last_name")
    inlines = [FamilyMemberInline, AddressInline, EmailInline, PhoneInline]
    readonly_fields = ("age", "last_login", "preview")

    def get_queryset(self, request):
        return super().get_queryset(request).with_name()

    def get_inlines(self, request, obj):
        if obj:
            inlines = super().get_inlines(request, obj)
        else:
            inlines = []
        return inlines

    @admin.display(description=_("name"), ordering="short_name")
    def short_name(self, obj):
        return obj.short_name

    @staticmethod
    @admin.display(description=_("current"))
    def preview(obj):
        return image_preview(obj.avatar.url)
