"""
:Copyright: 2006-2018 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

import pytest

from byceps.util.image.models import Dimensions


@pytest.mark.parametrize('width, height, expected', [
    ( 1,  1, True ),
    (12, 16, False),
    (16, 12, False),
    (16, 16, True ),
])
def test_is_square(width, height, expected):
    dimensions = Dimensions(width, height)

    assert dimensions.is_square == expected
