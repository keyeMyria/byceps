# -*- coding: utf-8 -*-

"""
testfixtures.verification_token
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2016 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from byceps.services.verification_token.models import Purpose, Token


def create_verification_token(user_id, purpose):
    return Token(user_id, purpose)


def create_verification_token_for_email_address_confirmation(user_id):
    purpose = Purpose.email_address_confirmation
    return create_verification_token(user_id, purpose)