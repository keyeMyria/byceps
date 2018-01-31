"""
byceps.services.board.models.last_category_view
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2018 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from datetime import datetime

from ....database import db
from ....typing import UserID
from ....util.instances import ReprBuilder

from .category import Category, CategoryID


class LastCategoryView(db.Model):
    """The last time a user looked into specific category."""
    __tablename__ = 'board_categories_lastviews'

    user_id = db.Column(db.Uuid, db.ForeignKey('users.id'), primary_key=True)
    category_id = db.Column(db.Uuid, db.ForeignKey('board_categories.id'), primary_key=True)
    category = db.relationship(Category)
    occurred_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id: UserID, category_id: CategoryID,
                 occurred_at: datetime) -> None:
        self.user_id = user_id
        self.category_id = category_id
        self.occurred_at = occurred_at

    def __repr__(self) -> str:
        return ReprBuilder(self) \
            .add_with_lookup('user_id') \
            .add('category', self.category.title) \
            .add_with_lookup('occurred_at') \
            .build()
