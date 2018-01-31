"""
byceps.services.user_avatar.service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2018 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from typing import BinaryIO, Dict, List, Set

from ...database import db
from ...typing import UserID
from ...util.image import create_thumbnail
from ...util.image.models import Dimensions, ImageType
from ...util import upload

from ..image import service as image_service
from ..image.service import ImageTypeProhibited  # Provide to view functions.
from ..user.models.user import User

from .models import Avatar, AvatarCreationTuple, AvatarSelection


MAXIMUM_DIMENSIONS = Dimensions(512, 512)


def update_avatar_image(user: User, stream: BinaryIO,
                        allowed_types: Set[ImageType],
                        *, maximum_dimensions: Dimensions=MAXIMUM_DIMENSIONS
                       ) -> None:
    """Set a new avatar image for the user.

    Raise `ImageTypeProhibited` if the stream data is not of one the
    allowed types.
    """
    image_type = image_service.determine_image_type(stream, allowed_types)
    image_dimensions = image_service.determine_dimensions(stream)

    image_too_large = image_dimensions > maximum_dimensions
    if image_too_large or not image_dimensions.is_square:
        stream = create_thumbnail(stream, image_type.name, maximum_dimensions,
                                  force_square=True)

    avatar = Avatar(user.id, image_type)
    db.session.add(avatar)
    db.session.commit()

    # Might raise `FileExistsError`.
    upload.store(stream, avatar.path)

    user.avatar = avatar
    db.session.commit()


def remove_avatar_image(user: User) -> None:
    """Remove the user's avatar image.

    The avatar will be unlinked from the user, but the database record
    as well as the image file itself won't be removed, though.
    """
    db.session.delete(user.avatar_selection)
    db.session.commit()


def get_avatars_uploaded_by_user(user_id: UserID) -> List[AvatarCreationTuple]:
    """Return the avatars uploaded by the user."""
    avatars = Avatar.query \
        .filter_by(creator_id=user_id) \
        .all()

    return [AvatarCreationTuple(avatar.created_at, avatar.url)
            for avatar in avatars]


def get_avatar_url_for_user(user_id: UserID) -> str:
    """Return the URL of the user's current avatar, or `None` if not set."""
    avatar_urls_by_user_id = get_avatar_urls_for_users({user_id})
    return avatar_urls_by_user_id.get(user_id)


def get_avatar_urls_for_users(user_ids: Set[UserID]) -> Dict[UserID, str]:
    """Return the URLs of those users' current avatars."""
    if not user_ids:
        return {}

    user_ids_and_avatars = db.session.query(AvatarSelection.user_id, Avatar) \
        .join(Avatar) \
        .filter(AvatarSelection.user_id.in_(user_ids)) \
        .all()

    urls_by_user_id = {user_id: avatar.url
                       for user_id, avatar in user_ids_and_avatars}

    # Include all user IDs in result.
    return {user_id: urls_by_user_id.get(user_id) for user_id in user_ids}
