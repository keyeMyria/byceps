"""
:Copyright: 2006-2018 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

import pytest

from byceps.services.country import service as country_service

from tests.helpers import app_context


@pytest.mark.parametrize('name, alpha2, alpha3', [
    ('Deutschland', 'DE', 'DEU'),
    ('Österreich' , 'AT', 'AUT'),
])
def test_get_countries_contains_country(name, alpha2, alpha3):
    with app_context():
        countries = country_service.get_countries()

    country = find_by_name(countries, name)

    assert country is not None
    assert country.name == name
    assert country.alpha2 == alpha2
    assert country.alpha3 == alpha3


def test_get_country_names_contains_selected_items():
    with app_context():
        actual = country_service.get_country_names()

    some_expected = frozenset([
        'Belgien',
        'Dänemark',
        'Deutschland',
        'Vereinigtes Königreich Großbritannien und Nordirland',
        'Frankreich',
        'Niederlande',
        'Österreich',
        'Schweiz',
    ])

    assert frozenset(actual).issuperset(some_expected)


def test_get_country_names_contains_no_duplicates():
    with app_context():
        actual = country_service.get_country_names()

    assert len(actual) == len(set(actual))


# helpers


def find_by_name(countries, name):
    """Return the first country with that name, or `None` if none matches."""
    for country in countries:
        if country.name == name:
            return country
