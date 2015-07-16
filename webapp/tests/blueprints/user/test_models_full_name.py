# -*- coding: utf-8 -*-

from unittest import TestCase

from nose2.tools import params

from testfixtures.user import create_user_with_detail


class FullNameTestCas(TestCase):

    @params(
        (None,          None    , None                ),
        ('Giesbert Z.', None    , 'Giesbert Z.'       ),
        (None,          'Blümli', 'Blümli'            ),
        ('Giesbert Z.', 'Blümli', 'Giesbert Z. Blümli'),
    )
    def test_full_name(self, first_names, last_name, expected):
        user = create_user_with_detail(123,
                                       first_names=first_names,
                                       last_name=last_name)

        self.assertEquals(user.detail.full_name, expected)