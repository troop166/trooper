from django.contrib import admin

from .models import Outing, OutingLeader


class OutingLeaderInline(admin.TabularInline):
    model = OutingLeader
    extra = 0


@admin.register(Outing)
class OutingAdmin(admin.ModelAdmin):
    inlines = [OutingLeaderInline]
