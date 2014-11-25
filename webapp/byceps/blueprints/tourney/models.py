# -*- coding: utf-8 -*-

"""
byceps.blueprints.tourney.models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2014 Jochen Kupperschmidt
"""

from datetime import datetime

from flask import g

from ...database import BaseQuery, db, generate_uuid

from ..user.models import User


class Match(db.Model):
    """A match between two opponents."""
    __tablename__ = 'tourney_matches'

    id = db.Column(db.Uuid, default=generate_uuid, primary_key=True)


class MatchCommentQuery(BaseQuery):

    def for_match(self, match):
        return self.filter_by(match=match)


class MatchComment(db.Model):
    """An immutable comment on a match by one of the opponents."""
    __tablename__ = 'tourney_match_comments'
    query_class = MatchCommentQuery

    id = db.Column(db.Uuid, default=generate_uuid, primary_key=True)
    match_id = db.Column(db.Uuid, db.ForeignKey('tourney_matches.id'), index=True, nullable=False)
    match = db.relationship(Match)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    created_by_id = db.Column(db.Uuid, db.ForeignKey('users.id'), nullable=False)
    created_by = db.relationship(User)
    body = db.Column(db.UnicodeText, nullable=False)

    @classmethod
    def create(cls, match, body):
        comment = MatchComment(
            match=match,
            created_by=g.current_user,
            body=body)
        db.session.add(comment)
        db.session.commit()
        return comment