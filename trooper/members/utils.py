from django.utils import timezone
from django.utils.translation import gettext as _


def eighteen_years_from(date=None):
    if not date:
        date = timezone.now()
    return date.replace(year=date.year - 18)


def calculate_age(date_of_birth, on_date=None):
    """
    Calculate a Member's age on given date. If no date is provided,
    defaults to today.
    """
    if not on_date:
        on_date = timezone.now().date()

    # Determine whether the member's birthday has passed the year
    birthday_upcoming = (on_date.month, on_date.day) < (
        date_of_birth.month,
        date_of_birth.day,
    )
    return on_date.year - date_of_birth.year - birthday_upcoming


def get_member_photo_upload_to(instance, filename):
    """Sort member photos into folders based on their username."""
    return _("members/%(username)s/%(filename)s") % {
        "username": instance.username,
        "filename": filename,
    }
