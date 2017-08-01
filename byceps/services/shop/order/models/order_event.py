"""
byceps.services.shop.order.models.order_event
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2017 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from datetime import datetime

from .....database import db, generate_uuid
from .....util.instances import ReprBuilder

from .order import OrderID


class OrderEvent(db.Model):
    """An event that refers to an order."""
    __tablename__ = 'shop_order_events'

    id = db.Column(db.Uuid, default=generate_uuid, primary_key=True)
    occured_at = db.Column(db.DateTime, nullable=False)
    event_type = db.Column(db.Unicode(40), index=True, nullable=False)
    order_id = db.Column(db.Uuid, db.ForeignKey('shop_orders.id'), index=True, nullable=False)
    data = db.Column(db.JSONB)

    def __init__(self, occured_at: datetime, event_type: str, order_id: OrderID,
                 **data) -> None:
        self.occured_at = occured_at
        self.event_type = event_type
        self.order_id = order_id
        self.data = data

    def __repr__(self) -> str:
        return ReprBuilder(self) \
            .add_custom(repr(self.event_type)) \
            .add_with_lookup('order_id') \
            .add_with_lookup('data') \
            .build()
