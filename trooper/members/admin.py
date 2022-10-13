from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from trooper.members.forms import MemberChangeForm, MemberCreationForm
from trooper.members.models import Member


@admin.register(Member)
class MemberAdmin(UserAdmin):
    add_form = MemberCreationForm
    form = MemberChangeForm
