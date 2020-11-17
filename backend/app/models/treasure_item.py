from app import db


class TreasureItem(db.Model):
    __tablename__ = 'treasure_item'

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean)
    cost = db.Column(db.Integer)
    description = db.Column(db.String(50))
    image_path = db.Column(db.String(50))
    name = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
