from flask_admin import form
from flask import url_for
from jinja2 import Markup

from app.utils import pokedex
from app import file_path
from app.model_views.model_view_base import ModelViewAuth

pokemon_to_image_dict = pokedex.create_pokemon_dict()


class StudentView(ModelViewAuth):
    # TODO Generate thumbnail images for pokemon. Right now since we only have ~30 students it doesn't really matter
    def _list_thumbnail(view, context, model, name):
        if not model.profile_image:
            return ''

        return Markup('<img src="%s" style="width: 50px; height: 50px;">' % model.profile_image)

    column_editable_list = ('points',)
    column_filters = ('first_name', 'last_name')
    column_formatters = {
        'profile_image': _list_thumbnail
    }
    column_searchable_list = ('first_name', 'last_name')
    column_exclude_list = ('active',)
    export_types = ['csv', 'xlsx']

    pokemon_choices = []

    for name in pokemon_to_image_dict:
        pokemon_choices.append((pokemon_to_image_dict[name], name))

    form_choices = {'profile_image': pokemon_choices}
