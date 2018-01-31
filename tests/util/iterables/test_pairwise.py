"""
:Copyright: 2006-2018 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

import pytest

from byceps.util.iterables import pairwise


@pytest.mark.parametrize('iterable, expected', [
    (
        [],
        [],
    ),
    (
        ['a', 'b', 'c'],
        [('a', 'b'), ('b', 'c')],
    ),
    (
        range(5),
        [(0, 1), (1, 2), (2, 3), (3, 4)],
    ),
])
def test_pairwise(iterable, expected):
    actual = pairwise(iterable)
    assert list(actual) == expected
