"""
byceps.blueprints.orga_admin.views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2018 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from operator import attrgetter

from flask import abort, request

from ...services.brand import service as brand_service
from ...services.orga import service as orga_service
from ...services.orga import birthday_service as orga_birthday_service
from ...services.user import service as user_service
from ...util.export import serialize_to_csv
from ...util.framework.blueprint import create_blueprint
from ...util.framework.flash import flash_success
from ...util.framework.templating import templated
from ...util.views import redirect_to, respond_no_content, textified

from ..authorization.decorators import permission_required
from ..authorization.registry import permission_registry
from ..orga_team_admin.authorization import OrgaTeamPermission

from .authorization import OrgaBirthdayPermission, OrgaDetailPermission
from .forms import OrgaFlagCreateForm


blueprint = create_blueprint('orga_admin', __name__)


permission_registry.register_enum(OrgaBirthdayPermission)
permission_registry.register_enum(OrgaDetailPermission)
permission_registry.register_enum(OrgaTeamPermission)


@blueprint.route('/persons')
@permission_required(OrgaDetailPermission.view)
@templated
def persons():
    """List brands to choose from."""
    brands_with_person_counts = orga_service.get_brands_with_person_counts()

    return {
        'brands_with_person_counts': brands_with_person_counts,
    }


@blueprint.route('/persons/<brand_id>')
@permission_required(OrgaDetailPermission.view)
@templated
def persons_for_brand(brand_id):
    """List organizers for the brand with details."""
    brand = _get_brand_or_404(brand_id)

    orgas = orga_service.get_orgas_for_brand(brand.id)

    return {
        'brand': brand,
        'orgas': orgas,
    }


@blueprint.route('/persons/<brand_id>/create')
@permission_required(OrgaTeamPermission.administrate_memberships)
@templated
def create_orgaflag_form(brand_id, erroneous_form=None):
    """Show form to give the organizer flag to a user."""
    brand = _get_brand_or_404(brand_id)

    form = erroneous_form if erroneous_form else OrgaFlagCreateForm()

    return {
        'brand': brand,
        'form': form,
    }


@blueprint.route('/persons/<brand_id>', methods=['POST'])
@permission_required(OrgaTeamPermission.administrate_memberships)
def create_orgaflag(brand_id):
    """Give the organizer flag to a user."""
    brand = _get_brand_or_404(brand_id)

    form = OrgaFlagCreateForm(request.form)
    if not form.validate():
        return create_orgaflag_form(brand.id, form)

    user = form.user.data

    orga_flag = orga_service.create_orga_flag(brand.id, user.id)

    flash_success('{} wurde das Orga-Flag für die Marke {} gegeben.',
                  orga_flag.user.screen_name, orga_flag.brand.title)
    return redirect_to('.persons_for_brand', brand_id=orga_flag.brand.id)


@blueprint.route('/persons/<brand_id>/<uuid:user_id>', methods=['DELETE'])
@permission_required(OrgaTeamPermission.administrate_memberships)
@respond_no_content
def remove_orgaflag(brand_id, user_id):
    """Remove the organizer flag for a brand from a person."""
    orga_flag = orga_service.find_orga_flag(brand_id, user_id)

    if orga_flag is None:
        abort(404)

    brand = orga_flag.brand
    user = orga_flag.user

    orga_service.delete_orga_flag(orga_flag)

    flash_success('{} wurde das Orga-Flag für die Marke {} entzogen.',
                  user.screen_name, brand.title)


@blueprint.route('/persons/<brand_id>/export')
@permission_required(OrgaDetailPermission.view)
@textified
def export_persons(brand_id):
    """Export the list of organizers for the brand as a CSV document in
    Microsoft Excel dialect.
    """
    brand = _get_brand_or_404(brand_id)

    field_names = [
        'Benutzername',
        'Vorname',
        'Nachname',
        'Geburtstag',
        'Straße',
        'PLZ',
        'Ort',
        'Land',
        'E-Mail-Adresse',
        'Telefonnummer',
    ]

    def to_dict(user):
        date_of_birth = user.detail.date_of_birth.strftime('%d.%m.%Y') \
                        if user.detail.date_of_birth else None

        return {
            'Benutzername': user.screen_name,
            'Vorname': user.detail.first_names,
            'Nachname': user.detail.last_name,
            'Geburtstag': date_of_birth,
            'Straße': user.detail.street,
            'PLZ': user.detail.zip_code,
            'Ort': user.detail.city,
            'Land': user.detail.country,
            'E-Mail-Adresse': user.email_address,
            'Telefonnummer': user.detail.phone_number,
        }

    orgas = orga_service.get_orgas_for_brand(brand.id)
    orgas.sort(key=attrgetter('screen_name'))
    rows = map(to_dict, orgas)
    return serialize_to_csv(field_names, rows)


@blueprint.route('/birthdays')
@permission_required(OrgaBirthdayPermission.list)
@templated
def birthdays():
    orgas = list(
        orga_birthday_service.collect_orgas_with_next_birthdays(limit=5))

    return {
        'orgas': orgas,
    }


def _get_brand_or_404(brand_id):
    brand = brand_service.find_brand(brand_id)

    if brand is None:
        abort(404)

    return brand


def _get_user_or_404(user_id):
    user = user_service.find_user(user_id)

    if user is None:
        abort(404)

    return user
