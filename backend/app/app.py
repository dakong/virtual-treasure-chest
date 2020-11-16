from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.utils.response_generator import generateSuccessResponse, generateFailResponse, generateErrorResponse

# Initialize our flask app
app = Flask(__name__)

# Initialize our database and ORM
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///virtual_treasure_chest.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Declare our ORM mapping


class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    points = db.Column(db.Integer)

    def fullname(self):
        return self.first_name + ' ' + self.last_name


class TreasureItem(db.Model):
    __tablename__ = 'treasure_item'

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean)
    cost = db.Column(db.Integer)
    description = db.Column(db.String(50))
    image_path = db.Column(db.String(50))
    name = db.Column(db.String(50))
    quantity = db.Column(db.Integer)

# Declare routes


@app.route('/student', methods=['GET', 'POST'])
def student():
    if request.method == 'POST':
        studentData = request.get_json()
        student = Student(
            first_name=studentData['first_name'], last_name=studentData['last_name'], active=True, points=0)
        db.session.add(student)
        db.session.commit()

        return generateSuccessResponse({
            'student': {
                'id': student.id,
                'name': student.fullname()
            }
        })

    if request.method == 'GET':
        allStudents = Student.query.all()
        result = []
        for student in allStudents:
            result.append({'id': student.id, 'name': student.fullname()})

        return generateSuccessResponse({'students': result})


@app.route('/treasureitem', methods=['GET', 'POST'])
def treasure_item():
    if request.method == 'POST':
        treasureItemData = request.get_json()
        cost = treasureItemData['cost']
        description = treasureItemData['description']
        name = treasureItemData['name']
        quantity = treasureItemData['quantity']

        treasureItem = TreasureItem(
            cost=cost, name=name, description=description, quantity=quantity)
        db.session.add(treasureItem)
        db.session.commit()

        return generateSuccessResponse({
            'treasureItem': {
                'id': treasureItem.id,
                'name': treasureItem.name,
                'cost': treasureItem.cost,
                'description': treasureItem.description,
                'quantity': treasureItem.quantity
            }
        })

    if request.method == 'GET':
        treasureItems = TreasureItem.query.all()
        result = []
        for treasureItem in treasureItems:
            result.append({
                'id': treasureItem.id,
                'name': treasureItem.name,
                'cost': treasureItem.cost,
                'description': treasureItem.description,
                'quantity': treasureItem.quantity
            })

        return generateSuccessResponse({'treasureItems': result})
