# -*- coding: utf-8 -*-

"""
:Copyright: 2006-2015 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from decimal import Decimal
from unittest import TestCase

from nose2.tools import params

from byceps.util.money import EuroAmount


class EuroAmountTestCase(TestCase):

    @params(
        (
            EuroAmount( 0,  0),
            EuroAmount( 0,  0),
            EuroAmount( 0,  0),
        ),
        (
            EuroAmount( 0, 99),
            EuroAmount( 0,  2),
            EuroAmount( 1,  1),
        ),
        (
            EuroAmount(24, 90),
            EuroAmount(17, 10),
            EuroAmount(42,  0),
        ),
    )
    def test_addition(self, a, b, expected):
        self.assertEquals(a + b, expected)

    @params(
        (
            EuroAmount( 0,  0),
            EuroAmount( 0,  0),
            EuroAmount( 0,  0),
        ),
        (
            EuroAmount( 0, 99),
            EuroAmount( 0,  2),
            EuroAmount( 1,  1),
        ),
        (
            EuroAmount(24, 90),
            EuroAmount(17, 10),
            EuroAmount(42,  0),
        ),
    )
    def test_sum(self, a, b, expected):
        # Using the `sum` function requires `__radd__` to be implemented.
        self.assertEquals(sum([a, b]), expected)

    @params(
        (
            EuroAmount( 0,  0),
            3,
            EuroAmount( 0,  0),
        ),
        (
            EuroAmount( 0, 99),
            3,
            EuroAmount( 2, 97),
        ),
    )
    def test_multiplication(self, a, b, expected):
        self.assertEquals(a * b, expected)

    def test_multiplication_with_another_euro_amount_is_denied(self):
        with self.assertRaises(TypeError):
            EuroAmount(12, 99) * EuroAmount(4, 55)

    @params(
        (  '0'   , EuroAmount(  0,  0)),
        (  '0.00', EuroAmount(  0,  0)),
        (  '0.01', EuroAmount(  0,  1)),
        (  '0.05', EuroAmount(  0,  5)),
        (  '0.09', EuroAmount(  0,  9)),
        (  '0.10', EuroAmount(  0, 10)),
        (  '0.99', EuroAmount(  0, 99)),
        (  '1'   , EuroAmount(  1,  0)),
        (  '1.00', EuroAmount(  1,  0)),
        (  '1.01', EuroAmount(  1,  1)),
        (  '1.11', EuroAmount(  1, 11)),
        (  '1.99', EuroAmount(  1, 99)),
        (  '2.00', EuroAmount(  2,  0)),
        ( '12.34', EuroAmount( 12, 34)),
        ('123.45', EuroAmount(123, 45)),
    )
    def test_from_decimal(self, value_text, expected):
        value = Decimal(value_text)
        actual = EuroAmount.from_decimal(value)
        self.assertEquals(actual, expected)

    @params(
        (  '-1'),
        ( '-99'),
        ('-100'),
        ('-101'),
    )
    def test_from_decimal_raises_exception_on_negative_value(self, value_text):
        value = Decimal(value_text)
        with self.assertRaises(ValueError):
            EuroAmount.from_decimal(value)

    @params(
        (    0, EuroAmount(  0,  0)),
        (    1, EuroAmount(  0,  1)),
        (    5, EuroAmount(  0,  5)),
        (    9, EuroAmount(  0,  9)),
        (   10, EuroAmount(  0, 10)),
        (   99, EuroAmount(  0, 99)),
        (  100, EuroAmount(  1,  0)),
        (  101, EuroAmount(  1,  1)),
        (  111, EuroAmount(  1, 11)),
        (  199, EuroAmount(  1, 99)),
        (  200, EuroAmount(  2,  0)),
        ( 1234, EuroAmount( 12, 34)),
        (12345, EuroAmount(123, 45)),
    )
    def test_from_int(self, value, expected):
        actual = EuroAmount.from_int(value)
        self.assertEquals(actual, expected)

    @params(
        (  -1),
        ( -99),
        (-100),
        (-101),
    )
    def test_from_int_raises_exception_on_negative_value(self, value):
        with self.assertRaises(ValueError):
            EuroAmount.from_int(value)

    @params(
        (EuroAmount(  0,  0),   '0.00'),
        (EuroAmount(  0,  1),   '0.01'),
        (EuroAmount(  0,  5),   '0.05'),
        (EuroAmount(  0,  9),   '0.09'),
        (EuroAmount(  0, 10),   '0.10'),
        (EuroAmount(  0, 99),   '0.99'),
        (EuroAmount(  1,  0),   '1.00'),
        (EuroAmount(  1,  1),   '1.01'),
        (EuroAmount(  1, 11),   '1.11'),
        (EuroAmount(  1, 99),   '1.99'),
        (EuroAmount(  2,  0),   '2.00'),
        (EuroAmount( 12, 34),  '12.34'),
        (EuroAmount(123, 45), '123.45'),
    )
    def test_to_decimal(self, euro_amount, expected_text):
        expected = Decimal(expected_text)
        actual = euro_amount.to_decimal()
        self.assertEquals(actual, expected)

    @params(
        (EuroAmount(  0,  0),     0),
        (EuroAmount(  0,  1),     1),
        (EuroAmount(  0,  5),     5),
        (EuroAmount(  0,  9),     9),
        (EuroAmount(  0, 10),    10),
        (EuroAmount(  0, 99),    99),
        (EuroAmount(  1,  0),   100),
        (EuroAmount(  1,  1),   101),
        (EuroAmount(  1, 11),   111),
        (EuroAmount(  1, 99),   199),
        (EuroAmount(  2,  0),   200),
        (EuroAmount( 12, 34),  1234),
        (EuroAmount(123, 45), 12345),
    )
    def test_to_int(self, euro_amount, expected):
        actual = euro_amount.to_int()
        self.assertEquals(actual, expected)