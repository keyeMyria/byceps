"""
byceps.blueprints.authorization.views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2018 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from ...util.framework.blueprint import create_blueprint

from .registry import permission_registry


blueprint = create_blueprint('authorization', __name__)


@blueprint.app_context_processor
def add_permission_enums_to_template_context():
    return {e.__name__: e for e in permission_registry.get_enums()}
