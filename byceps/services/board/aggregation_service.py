"""
byceps.services.board.aggregation_service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2017 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from ...database import db

from .models.category import Category
from .models.posting import Posting
from .models.topic import Topic


def aggregate_category(category: Category) -> None:
    """Update the category's count and latest fields."""
    topic_count = Topic.query.for_category(category.id).without_hidden().count()

    posting_query = Posting.query \
        .without_hidden() \
        .join(Topic) \
            .filter_by(category=category)

    posting_count = posting_query.count()

    latest_posting = posting_query \
        .filter(Topic.hidden == False) \
        .latest_to_earliest() \
        .first()

    category.topic_count = topic_count
    category.posting_count = posting_count
    category.last_posting_updated_at = latest_posting.created_at \
                                        if latest_posting else None
    category.last_posting_updated_by_id = latest_posting.creator_id \
                                        if latest_posting else None

    db.session.commit()


def aggregate_topic(topic: Topic) -> None:
    """Update the topic's count and latest fields."""
    posting_query = Posting.query.for_topic(topic.id).without_hidden()

    posting_count = posting_query.count()

    latest_posting = posting_query.latest_to_earliest().first()

    topic.posting_count = posting_count
    if latest_posting:
        topic.last_updated_at = latest_posting.created_at
        topic.last_updated_by_id = latest_posting.creator_id

    db.session.commit()

    aggregate_category(topic.category)
