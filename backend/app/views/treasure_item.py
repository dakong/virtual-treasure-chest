from flask import url_for
from flask_admin import form
from flask_admin.contrib.sqla import ModelView
from jinja2 import Markup

from app import file_path


class TreasureItemView(ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.image_path:
            return ''

        thumbnail_path = 'treasure_items/' + \
            form.thumbgen_filename(model.image_path)

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=thumbnail_path))

    column_formatters = {
        'image_path': _list_thumbnail
    }
    column_list = ('image_path', 'name', 'description', 'cost', 'quantity')
    form_extra_fields = {
        'image_path': form.ImageUploadField('Image',
                                            base_path=file_path,
                                            thumbnail_size=(100, 100, True))
    }
