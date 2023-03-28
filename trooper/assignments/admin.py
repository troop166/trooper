from django.contrib import admin
from django.utils.translation import gettext as _

from trooper.assignments.models import (
    Committee,
    CommitteeMember,
    Leader,
    Patrol,
    PatrolMember,
)


class CommitteeMemberInline(admin.TabularInline):
    model = CommitteeMember
    extra = 0
    autocomplete_fields = ("member",)


class PatrolMemberInline(admin.TabularInline):
    model = PatrolMember
    extra = 0
    autocomplete_fields = ("member",)


@admin.register(Leader)
class LeadershipAdmin(admin.ModelAdmin):
    list_display = ("member", "role", "start", "end")
    autocomplete_fields = ("member",)
    list_filter = ("role",)


@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    inlines = [CommitteeMemberInline]


@admin.register(Patrol)
class PatrolAdmin(admin.ModelAdmin):
    inlines = [PatrolMemberInline]
    list_display = ["name", "_member_count"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.count_members()

    @admin.display(description=_("Member count"), ordering="member_count")
    def _member_count(self, obj):
        return obj.member_count
