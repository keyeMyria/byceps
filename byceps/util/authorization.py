# -*- coding: utf-8 -*-

"""
byceps.util.authorization
~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2017 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from enum import Enum


def create_permission_enum(key, member_names):
    """Create a permission enum."""
    name = derive_name(key)
    permission_enum = Enum(name, list(member_names))
    permission_enum.__key__ = key
    permission_enum.__repr__ = lambda self: '<{}>'.format(self)
    return permission_enum


def derive_name(key: str) -> str:
    """Derive a `CamelCase` name from the `underscore_separated_key`."""
    words = key.split('_')
    words.append('permission')

    return ''.join(word.title() for word in words)
