# -*- coding: utf-8 -*-

from datetime import date
from functools import partial
from unittest import TestCase

from nose2.tools import params

from byceps.blueprints.user.models import User
from byceps.blueprints.orga_admin.models import Birthday, sort_birthdays


class BirthdayTestCase(TestCase):

    def setUp(self):
        self.date_of_birth = date(1994, 3, 18)

    @params(
        (date(2014, 3, 17), 19),
        (date(2014, 3, 18), 20),
        (date(2014, 3, 19), 20),
        (date(2015, 3, 17), 20),
        (date(2015, 3, 18), 21),
        (date(2015, 3, 19), 21),
    )
    def test_age(self, today, expected):
        birthday = create_birthday(self.date_of_birth, today)

        self.assertEquals(birthday.age, expected)

    @params(
        (date(2014, 3, 16), 2),
        (date(2014, 3, 17), 1),
        (date(2014, 3, 18), 0),
        (date(2014, 3, 19), 364),
    )
    def test_days_until(self, today, expected):
        birthday = create_birthday(self.date_of_birth, today)

        self.assertEquals(birthday.days_until, expected)

    @params(
        (date(1994, 3, 17), False),
        (date(1994, 3, 18), True),
        (date(1994, 3, 19), False),
        (date(2014, 3, 17), False),
        (date(2014, 3, 18), True),
        (date(2014, 3, 19), False),
    )
    def test_is_today(self, today, expected):
        birthday = create_birthday(self.date_of_birth, today)

        self.assertEquals(birthday.is_today, expected)


class BirthdayListTestCase(TestCase):

    def test_sort(self):
        today = date(1994, 9, 30)

        to_birthday = partial(create_birthday, today=today)

        birthday1985 = to_birthday(date(1985,  9, 29))
        birthday1987 = to_birthday(date(1987, 10,  1))
        birthday1991 = to_birthday(date(1991, 11, 14))
        birthday1992 = to_birthday(date(1992, 11, 14))
        birthday1994 = to_birthday(date(1994,  9, 30))

        birthdays = set([
            birthday1985,
            birthday1987,
            birthday1991,
            birthday1992,
            birthday1994,
        ])

        expected = [
            birthday1994,
            birthday1987,
            birthday1991,
            birthday1992,
            birthday1985,
        ]

        actual = list(sort_birthdays(birthdays))
        self.assertEquals(actual, expected)


def create_birthday(date_of_birth, today):
    return Birthday.of(None, date_of_birth, today)