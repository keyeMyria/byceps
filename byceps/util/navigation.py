"""
byceps.util.navigation
~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2017 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from collections import namedtuple
from enum import Enum
from typing import List

from flask import g


NavigationItem = namedtuple('NavigationItem', [
    'endpoint',
    'label',
    'id',
    'required_permission',
    'icon',
])


class Navigation(object):
    """A navigation list.

    The order of items is the order in which they are added.
    """

    def __init__(self, title: str) -> None:
        self.title = title
        self.items = []  # type: List[NavigationItem]

    def add_item(self, endpoint: str, label: str, *, id: str=None,
                 required_permission: Enum=None, icon: str=None) -> object:
        """Add an item to the navigation."""
        item = NavigationItem(
            endpoint=endpoint,
            label=label,
            id=id,
            required_permission=required_permission,
            icon=icon
            )

        self.items.append(item)
        return self

    def get_items(self) -> List[NavigationItem]:
        def current_user_has_permission(item: NavigationItem) -> bool:
            required_permission = item.required_permission
            if required_permission is None:
                return True

            return g.current_user.has_permission(required_permission)

        return list(filter(current_user_has_permission, self.items))
