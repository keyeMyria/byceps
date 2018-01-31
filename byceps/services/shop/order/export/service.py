"""
byceps.services.shop.order.export.service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2018 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from datetime import datetime
from decimal import Decimal
from typing import Any, Dict

from flask import current_app

from .....services.user import service as user_service
from .....util.money import to_two_places
from .....util.templating import load_template

from .. import service as order_service
from ..models.order import OrderID, OrderTuple


def export_order_as_xml(order_id: OrderID) -> Dict[str, str]:
    """Export the order as an XML document."""
    order = order_service.find_order_with_details(order_id)

    if order is None:
        return None

    context = _assemble_context(order)
    xml = _render_template(context)

    return {
        'content': xml,
        'content_type': 'application/xml; charset=iso-8859-1',
    }


def _assemble_context(order: OrderTuple) -> Dict[str, Any]:
    """Assemble template context."""
    placed_by = user_service.find_user(order.placed_by_id)
    email_address = placed_by.email_address

    now = datetime.now()

    return {
        'order': order,
        'email_address': email_address,
        'order_items': order.items,
        'now': now,
        'format_export_amount': _format_export_amount,
        'format_export_datetime': _format_export_datetime,
    }


def _format_export_amount(amount: Decimal) -> str:
    """Format the monetary amount as required by the export format
    specification.
    """
    quantized = to_two_places(amount)
    return '{:.2f}'.format(quantized)


def _format_export_datetime(dt: datetime) -> str:
    """Format date and time as required by the export format specification."""
    timezone = current_app.config['SHOP_ORDER_EXPORT_TIMEZONE']
    localized_dt = timezone.localize(dt)

    date_time, utc_offset = localized_dt.strftime('%Y-%m-%dT%H:%M:%S|%z') \
                                        .split('|', 1)

    if len(utc_offset) == 5:
        # Insert colon between hours and minutes.
        utc_offset = utc_offset[:3] + ':' + utc_offset[3:]

    return date_time + utc_offset


def _render_template(context: Dict[str, Any]) -> str:
    """Load and render export template."""
    path = 'services/shop/order/export/templates/export.xml'
    with current_app.open_resource(path, 'r') as f:
        source = f.read()

    template = load_template(source)
    return template.render(**context)
