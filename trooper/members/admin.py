from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

from trooper.address_book.admin import AddressInline, EmailInline, PhoneInline
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
    search_fields = ("members__first_name", "members__last_name")


@admin.register(Member)
class MemberAdmin(UserAdmin):
    add_form = MemberCreationForm
    form = MemberChangeForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "email", "avatar")},
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
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    inlines = [FamilyMemberInline, AddressInline, EmailInline, PhoneInline]
