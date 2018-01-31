"""
byceps.services.authentication.password.models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2018 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from datetime import datetime

from ....database import db
from ....typing import UserID


class Credential(db.Model):
    """A user's login credential."""
    __tablename__ = 'authn_credentials'

    user_id = db.Column(db.Uuid, db.ForeignKey('users.id'), primary_key=True)
    password_hash = db.Column(db.Unicode(100), nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id: UserID, password_hash: str, updated_at: datetime) -> None:
        self.user_id = user_id
        self.password_hash = password_hash
        self.updated_at = updated_at
