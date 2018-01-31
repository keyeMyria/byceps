"""
byceps.blueprints.shop_order_admin.forms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2018 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from wtforms import RadioField, TextAreaField
from wtforms.validators import InputRequired, Length

from ...services.shop.order.models.payment import PaymentMethod
from ...util.l10n import LocalizedForm


class CancelForm(LocalizedForm):
    reason = TextAreaField('Begründung', validators=[InputRequired(), Length(max=200)])


PAYMENT_METHOD_CHOICES = [
    (PaymentMethod.bank_transfer.name, 'Überweisung'),
    (PaymentMethod.cash.name, 'Barzahlung'),
    (PaymentMethod.direct_debit.name, 'Lastschrift'),
]


class MarkAsPaidForm(LocalizedForm):
    payment_method = RadioField('Zahlungsart',
        choices=PAYMENT_METHOD_CHOICES,
        default=PAYMENT_METHOD_CHOICES[0][0],
        validators=[InputRequired()])
