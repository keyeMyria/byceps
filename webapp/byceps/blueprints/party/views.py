# -*- coding: utf-8 -*-

"""
byceps.blueprints.party.views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2015 Jochen Kupperschmidt
"""

from flask import g

from ...config import get_current_party_id
from ...database import db
from ...util.framework import create_blueprint
from ...util.templating import templated

from .models import Party


blueprint = create_blueprint('party', __name__)


@blueprint.before_app_request
def before_request():
    id = get_current_party_id()
    party = get_party(id)
    if party is None:
        raise Exception('Unknown party ID "{}".'.format(id))

    g.party = party


def get_party(id):
    return Party.query \
        .options(db.joinedload('brand')) \
        .get(id)


@blueprint.route('/info')
@templated
def info():
    """Show information about the current party."""
