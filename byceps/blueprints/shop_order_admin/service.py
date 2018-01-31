"""
byceps.blueprints.shop_order_admin.service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2018 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from collections import namedtuple

from typing import Dict, Iterator, Sequence

from ...services.shop.article.models.article import Article, ArticleNumber
from ...services.shop.article import service as article_service
from ...services.shop.order.models.order import OrderID, OrderTuple
from ...services.shop.order.models.order_event import OrderEvent, OrderEventData
from ...services.shop.order import event_service as order_event_service
from ...services.shop.order import service as order_service
from ...services.ticketing import category_service as ticket_category_service
from ...services.user.models.user import User, UserTuple
from ...services.user import service as user_service
from ...services.user_badge import service as user_badge_service
from ...typing import UserID


OrderTupleWithOrderer = namedtuple('OrderTupleWithOrderer',
                                   OrderTuple._fields + ('placed_by',))


def extend_order_tuples_with_orderer(orders: Sequence[OrderTuple]
                                    ) -> Iterator[OrderTupleWithOrderer]:
    orderer_ids = {order.placed_by_id for order in orders}
    orderers = user_service.find_users(orderer_ids)
    orderers_by_id = user_service.index_users_by_id(orderers)

    for order in orders:
        orderer = orderers_by_id[order.placed_by_id]
        fields = order + (orderer,)
        yield OrderTupleWithOrderer(*fields)


def get_articles_by_item_number(order: OrderTuple
                               ) -> Dict[ArticleNumber, Article]:
    numbers = {item.article_number for item in order.items}

    articles = article_service.get_articles_by_numbers(numbers)

    return {article.item_number: article for article in articles}


def get_events(order_id: OrderID) -> Iterator[OrderEventData]:
    events = order_event_service.get_events_for_order(order_id)
    events.insert(0, _fake_order_placement_event(order_id))

    user_ids = {event.data['initiator_id']
                for event in events
                if 'initiator_id' in event.data}
    users = user_service.find_users(user_ids)
    users_by_id = {str(user.id): user for user in users}

    for event in events:
        data = {
            'event': event.event_type,
            'occurred_at': event.occurred_at,
            'data': event.data,
        }

        additional_data = _get_additional_data(event, users_by_id)
        data.update(additional_data)

        yield data


def _fake_order_placement_event(order_id: OrderID) -> OrderEvent:
    order = order_service.find_order_with_details(order_id)
    if order is None:
        raise ValueError('Unknown order ID')

    data = {
        'initiator_id': str(order.placed_by_id),
    }

    return OrderEvent(order.created_at, 'order-placed', order.id, data)


def _get_additional_data(event: OrderEvent, users_by_id: Dict[UserID, UserTuple]
                        ) -> OrderEventData:
    if event.event_type == 'badge-awarded':
        return _get_additional_data_for_badge_awarded(event)
    elif event.event_type == 'ticket-bundle-created':
        return _get_additional_data_for_ticket_bundle_created(event)
    elif event.event_type == 'ticket-created':
        return _get_additional_data_for_ticket_created(event)
    elif event.event_type == 'ticket-revoked':
        return _get_additional_data_for_ticket_revoked(event)
    else:
        return _get_additional_data_for_standard_event(event, users_by_id)


def _get_additional_data_for_standard_event(event: OrderEvent,
                                            users_by_id: Dict[UserID, UserTuple]
                                           ) -> OrderEventData:
    initiator_id = event.data['initiator_id']

    return {
        'initiator': users_by_id[initiator_id],
    }


def _get_additional_data_for_badge_awarded(event: OrderEvent) -> OrderEventData:
    badge_id = event.data['badge_id']
    badge = user_badge_service.find_badge(badge_id)

    recipient_id = event.data['recipient_id']
    recipient = user_service.find_user(recipient_id)
    recipient = _to_user_tuple(recipient)

    return {
        'badge_label': badge.label,
        'recipient': recipient,
    }


def _get_additional_data_for_ticket_bundle_created(event: OrderEvent
                                                  ) -> OrderEventData:
    bundle_id = event.data['ticket_bundle_id']
    category_id = event.data['ticket_bundle_category_id']
    ticket_quantity = event.data['ticket_bundle_ticket_quantity']
    owner_id = event.data['ticket_bundle_owner_id']

    category = ticket_category_service.find_category(category_id)
    category_title = category.title if (category is not None) else None

    return {
        'bundle_id': bundle_id,
        'ticket_category_title': category_title,
        'ticket_quantity': ticket_quantity,
    }


def _get_additional_data_for_ticket_created(event: OrderEvent
                                           ) -> OrderEventData:
    ticket_id = event.data['ticket_id']
    ticket_code = event.data['ticket_code']
    category_id = event.data['ticket_category_id']
    owner_id = event.data['ticket_owner_id']

    return {
        'ticket_code': ticket_code,
    }


def _get_additional_data_for_ticket_revoked(event: OrderEvent
                                           ) -> OrderEventData:
    ticket_id = event.data['ticket_id']
    ticket_code = event.data['ticket_code']

    return {
        'ticket_code': ticket_code,
    }


def _to_user_tuple(user: User) -> UserTuple:
    """Create an immutable tuple with selected values from user entity."""
    avatar_url = user.avatar.url if user.avatar else None
    is_orga = False

    return UserTuple(
        user.id,
        user.screen_name,
        user.deleted,
        avatar_url,
        is_orga,
    )
