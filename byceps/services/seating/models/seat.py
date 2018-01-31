"""
byceps.services.seating.models.seat
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2018 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from collections import namedtuple
from typing import NewType, Optional
from uuid import UUID

from sqlalchemy.ext.hybrid import hybrid_property

from ....database import db, generate_uuid
from ....util.instances import ReprBuilder

from ...ticketing.models.category import Category, CategoryID
from ...user.models.user import User

from .area import Area


Point = namedtuple('Point', ['x', 'y'])


SeatID = NewType('SeatID', UUID)


class Seat(db.Model):
    """A seat."""
    __tablename__ = 'seats'

    id = db.Column(db.Uuid, default=generate_uuid, primary_key=True)
    area_id = db.Column(db.Uuid, db.ForeignKey('seating_areas.id'), index=True, nullable=False)
    area = db.relationship(Area, backref='seats')
    coord_x = db.Column(db.Integer, nullable=False)
    coord_y = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Uuid, db.ForeignKey('ticket_categories.id'), index=True, nullable=False)
    category = db.relationship(Category)
    label = db.Column(db.Unicode(40), nullable=True)

    def __init__(self, area: Area, category_id: CategoryID, *, coord_x: int=0,
                 coord_y: int=0) -> None:
        self.area = area
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.category_id = category_id

    @hybrid_property
    def coords(self) -> Point:
        return Point(x=self.coord_x, y=self.coord_y)

    @coords.setter
    def coords(self, point: Point) -> None:
        self.coord_x = point.x
        self.coord_y = point.y

    @property
    def is_occupied(self) -> bool:
        """Return `True` if the seat is occupied by a ticket."""
        return self.occupied_by_ticket is not None

    @property
    def has_user(self) -> bool:
        """Return `True` if the seat is occupied by a ticket, and that
        ticket is assigned to a user.
        """
        return self.is_occupied and \
            (self.occupied_by_ticket.used_by_id is not None)

    @property
    def user(self) -> Optional[User]:
        """Return the user to which the ticket that occupies this seat
        is assigned, or `None` if this seat is not occupied by a ticket
        or the ticket is not assigned to a user.
        """
        if not self.has_user:
            return None

        return self.occupied_by_ticket.used_by

    def __repr__(self) -> str:
        return ReprBuilder(self) \
            .add('id', str(self.id)) \
            .add_with_lookup('area') \
            .add_with_lookup('category') \
            .add_with_lookup('label') \
            .build()
