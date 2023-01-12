import datetime

from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.validators import ValidationError
from django.utils import timezone
from django.utils.translation import gettext as _

from trooper.members.utils import calculate_age


def date_of_birth_validator(value: datetime.date):
    """
    Given a datetime.date()

    params: value
    returns:
    """

    # The scouting movement is widely recognized to have begun with the publication of
    # Scouting for Boys: A Handbook for instruction in good citizenship by Robert
    # Baden-Powell on January 24, 1908.
    #
    # ref: https://www.history.com/this-day-in-history/boy-scouts-movement-begins
    ORIGIN_DATE = datetime.date(year=1908, month=1, day=24)
    today = timezone.now().date()

    if today <= value:
        raise ValidationError(
            _("A person cannot be born in the future."), code="future_date_of_birth"
        )
    elif value <= ORIGIN_DATE.replace(year=ORIGIN_DATE.year - 111):
        age_on_origin_date = calculate_age(value, on_date=ORIGIN_DATE)
        raise ValidationError(
            _(
                "The date provided would make them %(age)s years old "
                "when scouting first began in %(year)d",
            )
            % {
                "age": intcomma(age_on_origin_date),
                "year": ORIGIN_DATE.year,
            },
            code="early_date_of_birth",
        )
    else:
        return value


def date_of_death_validator(value: datetime):
    today = timezone.now().date()
    if today <= value:
        raise ValidationError(
            _("We should not be able to know when a person will pass in the future."),
            code="future_date_of_death",
        )
    return value
