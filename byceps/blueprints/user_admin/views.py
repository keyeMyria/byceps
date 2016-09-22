# -*- coding: utf-8 -*-

"""
byceps.blueprints.user_admin.views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2016 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from flask import abort, request

from ...services.user_badge import service as badge_service
from ...util.framework import create_blueprint
from ...util.templating import templated

from ..authorization.decorators import permission_required
from ..authorization.registry import permission_registry
from ..authorization_admin import service as authorization_admin_service
from ..shop import order_service
from ..ticket import service as ticket_service
from ..user import service as user_service

from .authorization import UserPermission
from . import service
from .service import UserEnabledFilter


blueprint = create_blueprint('user_admin', __name__)


permission_registry.register_enum(UserPermission)


@blueprint.route('/', defaults={'page': 1})
@blueprint.route('/pages/<int:page>')
@permission_required(UserPermission.list)
@templated
def index(page):
    """List users."""
    per_page = request.args.get('per_page', type=int, default=20)
    search_term = request.args.get('search_term', default='').strip()

    if search_term:
        # Enabled filter argument is ignored if search term is given.
        only = None
        enabled_filter = None
    else:
        only = request.args.get('only')
        enabled_filter = UserEnabledFilter.__members__.get(only)

    users = service.get_users_paginated(page, per_page,
                                        search_term=search_term,
                                        enabled_filter=enabled_filter)

    total_enabled = user_service.count_enabled_users()
    total_disabled = user_service.count_disabled_users()
    total_overall = total_enabled + total_disabled

    return {
        'users': users,
        'total_enabled': total_enabled,
        'total_disabled': total_disabled,
        'total_overall': total_overall,
        'search_term': search_term,
        'only': only,
    }


@blueprint.route('/<uuid:id>')
@permission_required(UserPermission.view)
@templated
def view(id):
    """Show a user's interal profile."""
    user = user_service.find_user(id)
    if user is None:
        abort(404)

    permissions_by_role = authorization_admin_service \
        .get_permissions_by_roles_for_user_with_titles(user)

    badges = badge_service.get_badges_for_user(user.id)

    orders = order_service.get_orders_placed_by_user(user)

    tickets = ticket_service.find_tickets_related_to_user(user)

    return {
        'user': user,
        'permissions_by_role': permissions_by_role,
        'badges': badges,
        'orders': orders,
        'tickets': tickets,
    }
