"""
byceps.services.seating.models.seat_group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2017 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from typing import NewType
from uuid import UUID

from sqlalchemy.ext.associationproxy import association_proxy

from ....database import db, generate_uuid
from ....typing import PartyID
from ....util.instances import ReprBuilder

from ...ticketing.models.ticket_bundle import TicketBundle, TicketBundleID

from .category import Category
from .seat import Seat


SeatGroupID = NewType('SeatGroupID', UUID)


class SeatGroup(db.Model):
    """A group of seats."""
    __tablename__ = 'seat_groups'
    __table_args__ = (
        db.UniqueConstraint('party_id', 'title'),
    )

    id = db.Column(db.Uuid, default=generate_uuid, primary_key=True)
    party_id = db.Column(db.Unicode(40), db.ForeignKey('parties.id'), index=True, nullable=False)
    seat_category_id = db.Column(db.Uuid, db.ForeignKey('seat_categories.id'), nullable=False)
    seat_category = db.relationship(Category)
    seat_quantity = db.Column(db.Integer, nullable=False)
    title = db.Column(db.Unicode(40), nullable=False)

    seats = association_proxy('assignments', 'seat')

    def __init__(self, party_id: PartyID, seat_category: Category,
                 seat_quantity: int, title: str) -> None:
        self.party_id = party_id
        self.seat_category = seat_category
        self.seat_quantity = seat_quantity
        self.title = title

    def is_occupied(self) -> bool:
        return self.occupancy is not None

    def __repr__(self) -> str:
        return ReprBuilder(self) \
            .add('id', str(self.id)) \
            .add('party', self.party_id) \
            .add('seat_category', self.seat_category.title) \
            .add_with_lookup('seat_quantity') \
            .add_with_lookup('title') \
            .add_with_lookup('is_occupied') \
            .build()


class SeatGroupAssignment(db.Model):
    """The assignment of a seat to a seat group."""
    __tablename__ = 'seat_group_assignments'

    id = db.Column(db.Uuid, default=generate_uuid, primary_key=True)
    group_id = db.Column(db.Uuid, db.ForeignKey('seat_groups.id'), index=True, nullable=False)
    group = db.relationship(SeatGroup, collection_class=set, backref='assignments')
    seat_id = db.Column(db.Uuid, db.ForeignKey('seats.id'), unique=True, index=True, nullable=False)
    seat = db.relationship(Seat)

    def __init__(self, group: SeatGroup, seat: Seat) -> None:
        self.group = group
        self.seat = seat

    def __repr__(self) -> str:
        return ReprBuilder(self) \
            .add('id', str(self.id)) \
            .add('group', self.group.title) \
            .add_with_lookup('seat_id') \
            .build()


class Occupancy(db.Model):
    """The occupancy of a seat group."""
    __tablename__ = 'seat_group_occupancies'

    id = db.Column(db.Uuid, default=generate_uuid, primary_key=True)
    seat_group_id = db.Column(db.Uuid, db.ForeignKey('seat_groups.id'), unique=True, index=True, nullable=False)
    seat_group = db.relationship(SeatGroup, backref=db.backref('occupancy', uselist=False))
    ticket_bundle_id = db.Column(db.Uuid, db.ForeignKey('ticket_bundles.id'), unique=True, index=True, nullable=False)
    ticket_bundle = db.relationship(TicketBundle, backref=db.backref('occupied_seat_group', uselist=False))

    def __init__(self, seat_group_id: SeatGroup,
                 ticket_bundle_id: TicketBundleID) -> None:
        self.seat_group_id = seat_group_id
        self.ticket_bundle_id = ticket_bundle_id

    def __repr__(self) -> str:
        return ReprBuilder(self) \
            .add('seat_group_id', str(self.seat_group_id)) \
            .add('ticket_bundle_id', str(self.ticket_bundle_id)) \
            .build()
