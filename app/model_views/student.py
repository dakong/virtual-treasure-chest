from flask_admin import form
from flask import url_for
from jinja2 import Markup

from app import file_path
from app.model_views.model_view_base import ModelViewAuth


class StudentView(ModelViewAuth):
    def _list_thumbnail(view, context, model, name):
        if not model.image_path:
            return ''

        thumbnail_path = 'images/profile/' + \
            form.thumbgen_filename(model.image_path)

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=thumbnail_path))

    column_editable_list = ('points',)
    column_filters = ('first_name', 'last_name')
    column_formatters = {
        'image_path': _list_thumbnail
    }
    column_searchable_list = ('first_name', 'last_name')
    column_exclude_list = ('active',)
    export_types = ['csv', 'xlsx']

    form_extra_fields = {
        'profile_image': form.ImageUploadField('Image',
                                               base_path=file_path + '/profile/',
                                               url_relative_path='images/profile/',
                                               thumbnail_size=(100, 100, True))
    }
