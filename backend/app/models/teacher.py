from app import db


class Teacher(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    password = db.Column(db.String(100))
