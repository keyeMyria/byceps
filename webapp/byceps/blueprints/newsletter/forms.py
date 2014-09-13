# -*- coding: utf-8 -*-

"""
byceps.blueprints.newsletter.forms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2014 Jochen Kupperschmidt
"""

from wtforms import RadioField
from wtforms.validators import DataRequired

from ...util.l10n import LocalizedForm

from ..newsletter.models import SubscriptionState


class SubscriptionForm(LocalizedForm):
    state = RadioField(
        'Abonnement',
        choices=[
            (SubscriptionState.requested.name, 'ja, bitte'),
            (SubscriptionState.declined.name, 'nein, danke'),
        ],
        validators=[DataRequired()])
