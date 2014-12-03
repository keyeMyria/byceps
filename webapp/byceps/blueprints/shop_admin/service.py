# -*- coding: utf-8 -*-

"""
byceps.blueprints.shop_admin.service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2014 Jochen Kupperschmidt
"""

from collections import Counter


def count_ordered_articles(article):
    """Count how often the article has been ordered, grouped by the
    order's payment state.
    """
    counter = Counter()
    for order_item in article.order_items:
        counter[order_item.order.payment_state] += order_item.quantity
    return dict(counter)