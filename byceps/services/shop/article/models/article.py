"""
byceps.services.shop.article.models.article
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2017 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from datetime import datetime
from decimal import Decimal
from typing import Any, NewType, Optional
from uuid import UUID

from Ranger import Range
from Ranger.src.Range.Cut import Cut

from .....database import BaseQuery, db, generate_uuid
from .....typing import PartyID
from .....util.instances import ReprBuilder

from ....party.models import Party


ArticleID = NewType('ArticleID', UUID)


ArticleNumber = NewType('ArticleNumber', str)


class ArticleQuery(BaseQuery):

    def for_party_id(self, party_id: PartyID) -> BaseQuery:
        return self.filter_by(party_id=party_id)

    def currently_available(self) -> BaseQuery:
        """Select only articles that are available in between the
        temporal boundaries for this article, if specified.
        """
        now = datetime.now()

        return self \
            .filter(db.or_(
                Article.available_from == None,
                now >= Article.available_from
            )) \
            .filter(db.or_(
                Article.available_until == None,
                now < Article.available_until
            ))


class Article(db.Model):
    """An article that can be bought."""
    __tablename__ = 'shop_articles'
    __table_args__ = (
        db.UniqueConstraint('party_id', 'description'),
        db.CheckConstraint('available_from < available_until'),
    )
    query_class = ArticleQuery

    id = db.Column(db.Uuid, default=generate_uuid, primary_key=True)
    party_id = db.Column(db.Unicode(40), db.ForeignKey('parties.id'), index=True, nullable=False)
    party = db.relationship(Party)
    item_number = db.Column(db.Unicode(20), unique=True, nullable=False)
    description = db.Column(db.Unicode(80), nullable=False)
    price = db.Column(db.Numeric(6, 2), nullable=False)
    tax_rate = db.Column(db.Numeric(3, 3), nullable=False)
    available_from = db.Column(db.DateTime, nullable=True)
    available_until = db.Column(db.DateTime, nullable=True)
    quantity = db.Column(db.Integer, db.CheckConstraint('quantity >= 0'), nullable=False)
    max_quantity_per_order = db.Column(db.Integer, nullable=True)
    not_directly_orderable = db.Column(db.Boolean, default=False, nullable=False)
    requires_separate_order = db.Column(db.Boolean, default=False, nullable=False)
    shipping_required = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, party_id: PartyID, item_number: ArticleNumber,
                 description: str, price: Decimal, tax_rate: Decimal,
                 quantity: int, *, available_from: Optional[datetime]=None,
                 available_until: Optional[datetime]=None) -> None:
        self.party_id = party_id
        self.item_number = item_number
        self.description = description
        self.price = price
        self.tax_rate = tax_rate
        self.available_from = available_from
        self.available_until = available_until
        self.quantity = quantity

    @property
    def tax_rate_as_percentage(self) -> str:
        # Keep a digit after the decimal point in case
        # the tax rate is a fractional number.
        percentage = (self.tax_rate * 100).quantize(Decimal('.0'))
        return str(percentage).replace('.', ',')

    @property
    def availability_range(self) -> Range:
        """Assemble the date/time range of the articles availability."""
        start = self.available_from
        end = self.available_until

        if start:
            if end:
                return Range.closedOpen(start, end)
            else:
                return Range.atLeast(start)
        else:
            if end:
                return Range.lessThan(end)
            else:
                return range_all(datetime)

    @property
    def is_available(self) -> bool:
        """Return `True` if the article is available at this moment in time."""
        now = datetime.now()
        return self.availability_range.contains(now)

    def __repr__(self) -> str:
        return ReprBuilder(self) \
            .add_with_lookup('id') \
            .add('party', self.party_id) \
            .add_with_lookup('item_number') \
            .add_with_lookup('description') \
            .add_with_lookup('quantity') \
            .build()


def range_all(theType: Any) -> Range:
    """Create a range than contains every value of the given type."""
    return Range(
        Cut.belowAll(theType=theType),
        Cut.aboveAll(theType=theType))
