"""
byceps.util.datetime.calc
~~~~~~~~~~~~~~~~~~~~~~~~~

Date/time calculations.

:Copyright: 2006-2018 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from datetime import date

from .monthday import MonthDay


def calculate_age(date_of_birth: date, today: date) -> int:
    """Calculate the number of full years since the date of birth until
    today.
    """
    age = today.year - date_of_birth.year
    if MonthDay.of(date_of_birth) > MonthDay.of(today):
        age -= 1
    return age


def calculate_days_until(date: date, today: date) -> int:
    """Calculate the number of days from today until the given date."""
    date_this_year = date.replace(year=today.year)
    if date_this_year < today:
        date_this_year = date.replace(year=date_this_year.year + 1)

    delta = date_this_year - today
    return delta.days
