"""
byceps.blueprints.shop_order.forms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2017 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from wtforms import SelectField, StringField
from wtforms.validators import InputRequired, Length

from ...services.shop.cart.models import Cart
from ...services.shop.order.models.order import Orderer
from ...util.l10n import LocalizedForm


class OrderForm(LocalizedForm):
    first_names = StringField('Vorname(n)', validators=[Length(min=2)])
    last_name = StringField('Nachname', validators=[Length(min=2)])
    country = StringField('Land', validators=[Length(min=2, max=60)])
    zip_code = StringField('PLZ', validators=[Length(min=5, max=5)])
    city = StringField('Stadt', validators=[Length(min=2)])
    street = StringField('Straße', validators=[Length(min=2)])

    def get_orderer(self, user):
        return Orderer(
            user,
            self.first_names.data.strip(),
            self.last_name.data.strip(),
            self.country.data.strip(),
            self.zip_code.data.strip(),
            self.city.data.strip(),
            self.street.data.strip(),
        )


def assemble_articles_order_form(article_compilation):
    """Dynamically extend the order form with one field per article."""

    class ArticlesOrderForm(OrderForm):

        def get_field_for_article(self, article):
            name = _generate_field_name(article)
            return getattr(self, name)

        def get_cart(self, article_compilation):
            cart = Cart()
            for article, quantity in self.get_cart_items(article_compilation):
                cart.add_item(article, quantity)
            return cart

        def get_cart_items(self, article_compilation):
            for item in article_compilation:
                quantity = self.get_field_for_article(item.article).data
                if quantity > 0:
                    yield item.article, quantity


    validators = [InputRequired()]
    for item in article_compilation:
        field_name = _generate_field_name(item.article)
        choices = _create_choices(item.article)
        field = SelectField('Anzahl', validators, coerce=int, choices=choices)
        setattr(ArticlesOrderForm, field_name, field)

    return ArticlesOrderForm


def _generate_field_name(article):
    return 'article_{}'.format(article.id)


def _create_choices(article):
    max_orderable_quantity = _get_max_orderable_quantity(article)
    quantities = list(range(max_orderable_quantity + 1))
    return [(quantity, str(quantity)) for quantity in quantities]


def _get_max_orderable_quantity(article):
    if article.max_quantity_per_order is None:
        return article.quantity

    return min(article.quantity, article.max_quantity_per_order)
