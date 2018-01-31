"""
byceps.blueprints.authorization_admin.views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2018 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from flask import abort

from ...services.authorization import service as authorization_service
from ...services.user import service as user_service
from ...util.framework.blueprint import create_blueprint
from ...util.framework.templating import templated

from ..authorization.decorators import permission_required
from ..authorization.registry import permission_registry

from .authorization import RolePermission


blueprint = create_blueprint('authorization_admin', __name__)


permission_registry.register_enum(RolePermission)


@blueprint.route('/permissions')
@permission_required(RolePermission.list)
@templated
def permission_index():
    """List permissions."""
    permissions = authorization_service.get_all_permissions_with_titles()

    return {'permissions': permissions}


@blueprint.route('/roles')
@permission_required(RolePermission.list)
@templated
def role_index():
    """List roles."""
    roles = authorization_service.get_all_roles_with_titles()

    return {'roles': roles}


@blueprint.route('/roles/<role_id>')
@permission_required(RolePermission.list)
@templated
def role_view(role_id):
    """View role details."""
    role = authorization_service.find_role(role_id)

    if role is None:
        abort(404)

    permissions = authorization_service \
        .get_permissions_with_title_for_role(role.id)

    user_ids = authorization_service.find_user_ids_for_role(role.id)
    users = user_service.find_users(user_ids)

    return {
        'role': role,
        'permissions': permissions,
        'users': users,
    }
