import os
import os.path as op
from sqlalchemy.event import listens_for
from flask_admin import form

from app.database import db
from app import file_path


class TreasureItem(db.Model):
    __tablename__ = 'treasure_item'

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean)
    cost = db.Column(db.Integer)
    description = db.Column(db.String(50))
    image_path = db.Column(db.String(50))
    name = db.Column(db.String(50))
    quantity = db.Column(db.Integer)

    def __repr__(self):
        return self.name + ': ' + self.description


@listens_for(TreasureItem, 'after_delete')
def del_image(mapper, connection, target):
    if target.image_path:
        # Delete image
        try:
            os.remove(op.join(file_path, target.image_path))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(op.join(file_path,
                              form.thumbgen_filename(target.image_path)))
        except OSError:
            pass
