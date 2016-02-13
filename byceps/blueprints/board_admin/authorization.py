# -*- coding: utf-8 -*-

"""
byceps.blueprints.board_admin.authorization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2016 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from byceps.util.authorization import create_permission_enum


BoardCategoryPermission = create_permission_enum('board_category', [
    'create',
    'update',
    'list',
])