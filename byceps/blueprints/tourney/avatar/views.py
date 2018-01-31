"""
byceps.blueprints.tourney.avatar.views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2018 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from flask import abort, g, request

from ....services.tourney.avatar import service as avatar_service
from ....util.framework.blueprint import create_blueprint
from ....util.image.models import ImageType
from ....util.views import respond_created

from .forms import CreateForm


blueprint = create_blueprint('avatar', __name__)


ALLOWED_IMAGE_TYPES = frozenset([
    ImageType.jpeg,
    ImageType.png,
])


@blueprint.route('', methods=['POST'])
@respond_created
def create():
    """Create an avatar image."""
    party_id = g.party_id
    user_id = _get_current_user_id_or_404()

    # Make `InputRequired` work on `FileField`.
    form_fields = request.form.copy()
    if request.files:
        form_fields.update(request.files)

    form = CreateForm(form_fields)

    if not form.validate():
        abort(400, 'Form validation failed.')

    image = request.files.get('image')

    avatar = _create(party_id, user_id, image)

    return avatar.url


def _create(party_id, creator_id, image):
    if not image or not image.filename:
        abort(400, 'No file to upload has been specified.')

    try:
        return avatar_service.create_avatar_image(
            party_id, creator_id, image.stream, ALLOWED_IMAGE_TYPES)
    except avatar_service.ImageTypeProhibited as e:
        abort(400, str(e))
    except FileExistsError:
        abort(409, 'File already exists, not overwriting.')


def _get_current_user_id_or_404():
    user = g.current_user

    if not user.is_active:
        abort(403)

    return user.id
