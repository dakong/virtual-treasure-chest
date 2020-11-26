from flask import url_for
from flask_admin import form
from app.model_views.model_view_base import ModelViewAuth
from jinja2 import Markup

from app import file_path


class TreasureItemView(ModelViewAuth):
    def _list_thumbnail(view, context, model, name):
        if not model.image_path:
            return ''

        thumbnail_path = 'images/treasure_items/' + \
            form.thumbgen_filename(model.image_path)

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=thumbnail_path))

    def create_form(self):
        form = super(ModelViewAuth, self).create_form()
        form.active.data = True
        return form

    column_formatters = {
        'image_path': _list_thumbnail
    }
    column_list = ('image_path', 'name', 'description', 'cost', 'quantity')
    form_extra_fields = {
        'image_path': form.ImageUploadField('Image',
                                            base_path=file_path + '/treasure_items/',
                                            url_relative_path='images/treasure_items/',
                                            thumbnail_size=(100, 100, True))
    }
