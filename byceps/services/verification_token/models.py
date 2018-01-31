"""
byceps.services.verification_token.models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2018 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from datetime import datetime, timedelta
from enum import Enum

from sqlalchemy.ext.hybrid import hybrid_property

from ...database import BaseQuery, db, generate_uuid
from ...typing import UserID
from ...util.instances import ReprBuilder

from ..user.models.user import User


Purpose = Enum('Purpose',
    ['email_address_confirmation', 'password_reset', 'terms_consent'])


class TokenQuery(BaseQuery):

    def for_purpose(self, purpose) -> BaseQuery:
        return self.filter_by(_purpose=purpose.name)


class Token(db.Model):
    """A private token to authenticate as a certain user for a certain
    action.
    """
    __tablename__ = 'verification_tokens'
    query_class = TokenQuery

    token = db.Column(db.Uuid, default=generate_uuid, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    user_id = db.Column(db.Uuid, db.ForeignKey('users.id'), index=True, nullable=False)
    user = db.relationship(User)
    _purpose = db.Column('purpose', db.Unicode(40), index=True, nullable=False)

    def __init__(self, user_id: UserID, purpose: Purpose) -> None:
        self.user_id = user_id
        self.purpose = purpose

    @hybrid_property
    def purpose(self) -> Purpose:
        return Purpose[self._purpose]

    @purpose.setter
    def purpose(self, purpose: Purpose) -> None:
        assert purpose is not None
        self._purpose = purpose.name

    @property
    def is_expired(self) -> bool:
        """Return `True` if expired, i.e. it is no longer valid."""
        if self.purpose == Purpose.password_reset:
            now = datetime.now()
            expires_after = timedelta(hours=24)
            return now >= (self.created_at + expires_after)
        else:
            return False

    def __repr__(self) -> str:
        return ReprBuilder(self) \
            .add_with_lookup('token') \
            .add('user', self.user.screen_name) \
            .add('purpose', self.purpose.name) \
            .build()
