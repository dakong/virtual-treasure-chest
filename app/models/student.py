from app.database import db


class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    points = db.Column(db.Integer)
    passcode = db.Column(db.String(100))
    profile_image = db.Column(db.String(50))

    def fullname(self):
        return self.first_name + ' ' + self.last_name

    def __repr__(self):
        return self.fullname()
