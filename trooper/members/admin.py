from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from trooper.address_book.admin import AddressInline, EmailInline, PhoneInline
from trooper.members.forms import MemberChangeForm, MemberCreationForm
from trooper.members.models import Member


@admin.register(Member)
class MemberAdmin(UserAdmin):
    add_form = MemberCreationForm
    form = MemberChangeForm

    inlines = [AddressInline, EmailInline, PhoneInline]
