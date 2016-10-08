# -*- coding: utf-8 -*-

"""
byceps.blueprints.board_admin.views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2016 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from flask import abort, request, url_for

from ...services.board import service as board_service
from ...services.brand import service as brand_service
from ...util.framework import create_blueprint, flash_error, flash_success
from ...util.templating import templated
from ...util.views import redirect_to, respond_no_content_with_location

from ..authorization.decorators import permission_required
from ..authorization.registry import permission_registry

from .authorization import BoardCategoryPermission
from .forms import CategoryCreateForm, CategoryUpdateForm


blueprint = create_blueprint('board_admin', __name__)


permission_registry.register_enum(BoardCategoryPermission)


@blueprint.route('/brands/<brand_id>')
@permission_required(BoardCategoryPermission.list)
@templated
def index_for_brand(brand_id):
    """List categories for that brand."""
    brand = get_brand_or_404(brand_id)

    categories = board_service.get_categories(brand.id)

    return {
        'brand': brand,
        'categories': categories,
    }


@blueprint.route('/for_brand/<brand_id>/create')
@permission_required(BoardCategoryPermission.create)
@templated
def category_create_form(brand_id, erroneous_form=None):
    """Show form to create a category."""
    brand = get_brand_or_404(brand_id)

    form = erroneous_form if erroneous_form else CategoryCreateForm()

    return {
        'brand': brand,
        'form': form,
    }


@blueprint.route('/for_brand/<brand_id>', methods=['POST'])
@permission_required(BoardCategoryPermission.create)
def category_create(brand_id):
    """Create a category."""
    brand = get_brand_or_404(brand_id)

    form = CategoryCreateForm(request.form)
    if not form.validate():
        return category_create_form(brand_id, form)

    slug = form.slug.data.strip().lower()
    title = form.title.data.strip()
    description = form.description.data.strip()

    category = board_service.create_category(brand, slug, title, description)

    flash_success('Die Kategorie "{}" wurde angelegt.', category.title)
    return redirect_to('.index_for_brand', brand_id=brand.id)


@blueprint.route('/categories/<uuid:category_id>/update')
@permission_required(BoardCategoryPermission.update)
@templated
def category_update_form(category_id, erroneous_form=None):
    """Show form to update a category."""
    category = get_category_or_404(category_id)

    form = erroneous_form if erroneous_form \
           else CategoryUpdateForm(obj=category)

    return {
        'category': category,
        'form': form,
    }


@blueprint.route('/categories/<uuid:category_id>', methods=['POST'])
@permission_required(BoardCategoryPermission.update)
def category_update(category_id):
    """Update a category."""
    category = get_category_or_404(category_id)

    form = CategoryUpdateForm(request.form)
    if not form.validate():
        return category_update_form(category_id, form)

    slug = form.slug.data
    title = form.title.data
    description = form.description.data

    category = board_service.update_category(category, slug, title, description)

    flash_success('Die Kategorie "{}" wurde aktualisiert.', category.title)
    return redirect_to('.index_for_brand', brand_id=category.brand.id)


@blueprint.route('/categories/<uuid:category_id>/up', methods=['POST'])
@permission_required(BoardCategoryPermission.update)
@respond_no_content_with_location
def category_move_up(category_id):
    """Move a category upwards by one position."""
    category = get_category_or_404(category_id)

    try:
        board_service.move_category_up(category)
    except ValueError:
        flash_error('Die Kategorie "{}" befindet sich bereits ganz oben.', category.title)
    else:
        flash_success('Die Kategorie "{}" wurde eine Position nach oben verschoben.', category.title)

    return url_for('.index_for_brand', brand_id=category.brand.id)


@blueprint.route('/categories/<uuid:category_id>/down', methods=['POST'])
@permission_required(BoardCategoryPermission.update)
@respond_no_content_with_location
def category_move_down(category_id):
    """Move a category downwards by one position."""
    category = get_category_or_404(category_id)

    try:
        board_service.move_category_down(category)
    except ValueError:
        flash_error('Die Kategorie "{}" befindet sich bereits ganz unten.', category.title)
    else:
        flash_success('Die Kategorie "{}" wurde eine Position nach unten verschoben.', category.title)

    return url_for('.index_for_brand', brand_id=category.brand.id)


def get_brand_or_404(brand_id):
    brand = brand_service.find_brand(brand_id)

    if brand is None:
        abort(404)

    return brand


def get_category_or_404(category_id):
    category = board_service.find_category_by_id(category_id)

    if category is None:
        abort(404)

    return category
