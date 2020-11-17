import bcrypt
from datetime import timedelta
from functools import wraps
from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.utils.response_generator import generateSuccessResponse, generateFailResponse, generateErrorResponse

from app.config import config

# Initialize our flask app
app = Flask(__name__)

# Initialize our database and ORM
app.config['SQLALCHEMY_DATABASE_URI'] = config['DB']
app.secret_key = config['SECRET_KEY']
db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)


@app.before_request
def make_session_permanent():
    session.permanent = False
    session.permanent_session_lifetime = timedelta(days=7)

# Declare our ORM mapping


class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    points = db.Column(db.Integer)
    passcode = db.Column(db.String(100))

    def fullname(self):
        return self.first_name + ' ' + self.last_name


class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    password = db.Column(db.String(100))


class TreasureItem(db.Model):
    __tablename__ = 'treasure_item'

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean)
    cost = db.Column(db.Integer)
    description = db.Column(db.String(50))
    image_path = db.Column(db.String(50))
    name = db.Column(db.String(50))
    quantity = db.Column(db.Integer)


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwds):
        if 'userID' in session:
            return fn(*args, **kwds)
        else:
            return (generateFailResponse({'message': 'Unauthorized'}), 401)

    return wrapper

# Declare routes


@app.route('/student', methods=['GET', 'POST'])
def student():
    if request.method == 'POST':
        studentData = request.get_json()
        # need to hash the passwords when we save
        passcode = studentData['passcode']
        first_name = studentData['first_name']
        last_name = studentData['last_name']
        salt = bcrypt.gensalt()
        hashed_passcode = bcrypt.hashpw(
            bytes(passcode, encoding='utf-8'), salt)

        student = Student(
            first_name=first_name,
            last_name=last_name,
            passcode=hashed_passcode,
            active=True,
            points=0)

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
@login_required
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
                'description': treasureItem.descriptdaion,
                'quantity': treasureItem.quantity
            })

        return generateSuccessResponse({'treasureItems': result})


@app.route('/', methods=['GET'])
def index():
    if 'userID' in session:
        return generateSuccessResponse({
            'isLoggedIn': True
        })
    return generateSuccessResponse({
        'isLoggedIn': False
    })


@app.route('/login', methods=['POST'])
def login():
    # authenticate using authorization header
    # base64 decode
    userID = request.authorization.username
    passcode = request.authorization.password

    student = Student.query.get(userID)

    if student == None:
        return generateFailResponse({'message': 'User not found'})

    if bcrypt.checkpw(bytes(passcode, encoding='utf-8'), student.passcode):
        # password match. Let's store user session
        session['userID'] = userID
        return generateSuccessResponse({'message': 'Succesfully created session'})

    return generateFailResponse({'message': 'Invalid passcode'})


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('userID', None)
    return generateSuccessResponse({'message': 'Succesfully ended session'})
