"""
byceps.blueprints.authorization.registry
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2017 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from flask import current_app


class PermissionRegistry:

    def __init__(self):
        self.enums = {}

    def register_enum(self, permission_enum):
        """Add an enum to the registry."""
        self.enums[permission_enum.__key__] = permission_enum

    def get_enums(self):
        """Return the registered enums."""
        return frozenset(self.enums.values())

    def get_enum_member(self, permission_id):
        """Return the enum that is registered for the given permission
        ID, or `None` if none is.
        """
        enum_key, permission_name = permission_id.split('.', 1)

        enum = self.enums.get(enum_key)
        if enum is None:
            # No enum found for that key. This happens if the blueprint
            # which contains the authorization enum is not registered in
            # the current site mode (public/admin).
            return None

        try:
            return enum[permission_name]
        except KeyError:
            current_app.logger.warn(
                'Ignoring unknown permission name "%s" configured '
                'in database for "%s" enum (permission ID: "%s").',
                permission_name, enum_key, permission_id)
            return None

    def get_enum_members(self, permission_ids):
        """Return the nums that are registered for the permission IDs.

        If no enum is found for a permission ID, it is silently ignored.
        """
        enums = (self.get_enum_member(p_id) for p_id in permission_ids)
        enums_without_none = (enum for enum in enums if enum is not None)
        return frozenset(enums_without_none)


permission_registry = PermissionRegistry()
