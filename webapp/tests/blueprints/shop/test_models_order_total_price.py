# -*- coding: utf-8 -*-

from unittest import TestCase

from nose2.tools import params

from byceps.blueprints.shop.models import Order
from byceps.util.money import EuroAmount

from testfixtures.shop import create_article, create_order
from testfixtures.user import create_user


class OrderTotalPriceTestCase(TestCase):

    def test_without_any_items(self):
        order = self.create_order_with_items([])

        self.assertEquals(order.calculate_total_price(), 0)

    def test_with_single_item(self):
        order = self.create_order_with_items([
            (EuroAmount(49, 95), 1),
        ])

        self.assertEquals(order.calculate_total_price(), EuroAmount(49, 95))

    def test_with_multiple_items(self):
        order = self.create_order_with_items([
            (EuroAmount(49, 95), 3),
            (EuroAmount( 6, 20), 1),
            (EuroAmount(12, 53), 4),
        ])

        self.assertEquals(order.calculate_total_price(), EuroAmount(206, 17))

    def create_order_with_items(self, price_quantity_pairs):
        user = create_user(42)
        order = create_order(placed_by=user)

        for price, quantity in price_quantity_pairs:
            article = create_article(price=price, quantity=quantity)
            order.add_item(article, quantity)

        return order