from app import db


class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    student = db.relationship('Student')

    treasure_item_id = db.Column(db.Integer, db.ForeignKey('treasure_item.id'))
    treasure_item = db.relationship('TreasureItem')
