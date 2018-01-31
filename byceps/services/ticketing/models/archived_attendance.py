"""
byceps.services.ticketing.models.archived_attendance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2018 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from datetime import datetime

from ....database import db
from ....typing import PartyID, UserID
from ....util.instances import ReprBuilder


class ArchivedAttendance(db.Model):
    """A user's attendance of a party.

    This is a link between a party and a user that attended it.

    While such a link is usually established through a ticket for a
    party that is assigned to a user, this entity was introduced for
    legacy data for which no information on tickets, orders, seating
    areas and so on exists anymore (or should not be migrated).

    The data for this entity is expected to be inserted from the
    outside. BYCEPS itself currently does not write any archived
    attendances (but incorporates them to be displayed on user
    profiles).
    """
    __tablename__ = 'user_archived_party_attendances'

    user_id = db.Column(db.Uuid, db.ForeignKey('users.id'), primary_key=True)
    party_id = db.Column(db.Unicode(40), db.ForeignKey('parties.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, user_id: UserID, party_id: PartyID) -> None:
        self.user_id = user_id
        self.party_id = party_id

    def __repr__(self) -> str:
        return ReprBuilder(self) \
            .add('user_id', str(self.user_id)) \
            .add('party_id', self.party_id) \
            .build()
