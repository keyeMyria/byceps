"""
byceps.blueprints.seating_admin.views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2018 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from flask import abort, request

from ...services.party import service as party_service
from ...services.seating import \
    area_service as seating_area_service, \
    seat_group_service, seat_service
from ...services.ticketing import category_service as ticketing_category_service
from ...util.framework.blueprint import create_blueprint
from ...util.framework.templating import templated

from ..authorization.decorators import permission_required
from ..authorization.registry import permission_registry

from .authorization import SeatingPermission


blueprint = create_blueprint('seating_admin', __name__)


permission_registry.register_enum(SeatingPermission)


@blueprint.route('/<party_id>')
@permission_required(SeatingPermission.view)
@templated
def index_for_party(party_id):
    """List seating areas for that party."""
    party = _get_party_or_404(party_id)

    seat_count = seat_service.count_seats_for_party(party.id)
    area_count = seating_area_service.count_areas_for_party(party.id)
    category_count = ticketing_category_service.count_categories_for_party(
        party.id)
    group_count = seat_group_service.count_seat_groups_for_party(party.id)

    return {
        'party': party,
        'seat_count': seat_count,
        'area_count': area_count,
        'category_count': category_count,
        'group_count': group_count,
    }


@blueprint.route('/parties/<party_id>/areas', defaults={'page': 1})
@blueprint.route('/parties/<party_id>/areas/pages/<int:page>')
@permission_required(SeatingPermission.view)
@templated
def area_index(party_id, page):
    """List seating areas for that party."""
    party = _get_party_or_404(party_id)

    per_page = request.args.get('per_page', type=int, default=15)
    areas = seating_area_service.get_areas_for_party_paginated(party.id, page,
                                                               per_page)

    seat_total_per_area = seat_service.get_seat_total_per_area(party.id)

    return {
        'party': party,
        'areas': areas,
        'seat_total_per_area': seat_total_per_area,
    }


@blueprint.route('/parties/<party_id>/seat_categories')
@permission_required(SeatingPermission.view)
@templated
def seat_category_index(party_id):
    """List seat categories for that party."""
    party = _get_party_or_404(party_id)

    categories = ticketing_category_service.get_categories_for_party(party.id)

    return {
        'party': party,
        'categories': categories,
    }


@blueprint.route('/parties/<party_id>/seat_groups')
@permission_required(SeatingPermission.view)
@templated
def seat_group_index(party_id):
    """List seat groups for that party."""
    party = _get_party_or_404(party_id)

    groups = seat_group_service.get_all_seat_groups_for_party(party.id)

    return {
        'party': party,
        'groups': groups,
    }


def _get_party_or_404(party_id):
    party = party_service.find_party(party_id)

    if party is None:
        abort(404)

    return party
