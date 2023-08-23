from datetime import date

from django.utils import timezone
from django.utils.translation import gettext as _

import vobject


def eighteen_years_from(day: date) -> date:
    """Given a day, returns the date eighteen years earlier. If no starting
    date is provided, will calculate eighteen years before today.

    Parameters
    ----------
    day : date, optional
        The starting day to calculate from (default is today)

    Returns
    -------
    date
        The original date minus eighteen years
    """
    if not day:
        day = timezone.now()
    return day.replace(year=day.year - 18)


def calculate_age(date_of_birth: date, on_date: date) -> int:
    """Calculate a Member's age on given date. If no date is provided,
    defaults to today.

    Parameters
    ----------
    date_of_birth : date
        The date a person was born.
    on_date : date, optional
        Calculate the person's age on a specific date. If no date is
        provided, calculate for the current date.

    Returns
    -------
    age : int
        The person's age for the specified date.
    """
    if not on_date:
        on_date = timezone.now().date()

    # Determine whether the member's birthday has passed the year
    birthday_upcoming = (on_date.month, on_date.day) < (
        date_of_birth.month,
        date_of_birth.day,
    )
    return on_date.year - date_of_birth.year - birthday_upcoming


def get_member_photo_upload_to(instance, filename: str) -> str:
    """Sort member photos into folders based on their username."""
    return _("members/%(username)s/%(filename)s") % {
        "username": instance.username,
        "filename": filename,
    }


def member_vcard(member) -> vobject.vCard:
    """Craft an object, compliant with vCard 3.0 standard using
    the published details of a Member
    """
    vcard = vobject.vCard()

    vcard.add("fn")
    vcard.fn.value = member.get_full_name()

    vcard.add("n")
    vcard.n.value = vobject.vcard.Name(
        family=member.last_name,
        given=member.first_name,
        additional=member.middle_name,
        suffix=member.suffix,
    )

    if member.nickname:
        vcard.add("nickname")
        vcard.nickname.value = member.nickname

    if member.age < 18:
        vcard.add("bday")
        vcard.bday.value = str(member.date_of_birth)

    for address in member.addresses.published():
        a = vcard.add("adr")
        a.value = vobject.vcard.Address(
            street=address.street,
            extended=address.street2,
            city=address.city,
            region=address.state,
            code=address.zip_code,
        )
        if address.label:
            a.type_param = address.label.lower()

    for email in member.email_addresses.published():
        e = vcard.add("email")
        e.value = email.address
        if email.label:
            e.type_param = email.label.lower()

    for phone in member.phone_numbers.published():
        p = vcard.add("tel")
        p.value = phone.number.as_national
        if phone.label:
            p.type_param = phone.label.lower()

    if member.photo:
        photo = vcard.add("photo")
        photo.encoding_param = "b"
        with member.photo.open() as p:
            photo.value = p.read()
    return vcard
