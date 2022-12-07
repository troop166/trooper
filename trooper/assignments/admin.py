from django.contrib import admin

from trooper.assignments.models import (
    Committee,
    CommitteeMember,
    Leadership,
    Patrol,
    PatrolMember,
)


class CommitteeMemberInline(admin.TabularInline):
    model = CommitteeMember
    extra = 0


class PatrolMemberInline(admin.TabularInline):
    model = PatrolMember
    extra = 0


@admin.register(Leadership)
class LeadershipAdmin(admin.ModelAdmin):
    pass


@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    inlines = [CommitteeMemberInline]


@admin.register(Patrol)
class PatrolAdmin(admin.ModelAdmin):
    inlines = [PatrolMemberInline]
