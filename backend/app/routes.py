import bcrypt
from datetime import timedelta
from functools import wraps
from flask import current_app as app, request, session, url_for

from app.utils.response_generator import generateSuccessResponse, generateFailResponse, generateErrorResponse
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.treasure_item import TreasureItem


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwds):
        if 'userID' in session:
            return fn(*args, **kwds)
        else:
            return (generateFailResponse({'message': 'Unauthorized'}), 401)

    return wrapper


@app.before_request
def make_session_permanent():
    session.permanent = False
    session.permanent_session_lifetime = timedelta(days=7)


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

    if student.passcode == pascode:
        # password match. Let's store user session
        session['userID'] = userID
        return generateSuccessResponse({'message': 'Succesfully created session'})

    return generateFailResponse({'message': 'Invalid passcode'})


@ app.route('/logout', methods=['POST'])
def logout():
    session.pop('userID', None)
    return generateSuccessResponse({'message': 'Succesfully ended session'})


@app.route('/api/treasureitem', methods=['GET', 'POST'])
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


@app.route('/api/student', methods=['GET', 'POST'])
def student():
    if request.method == 'POST':
        studentData = request.get_json()
        # need to hash the passwords when we save
        passcode = studentData['passcode']
        first_name = studentData['first_name']
        last_name = studentData['last_name']

        # TODO: Commented out for now for reference. We want to remove this and only has admin pw.
        # Student Passcode is okay to store. We want jennifer to be able to read and update passcodes.
        # Cannot update passcode if we hash pw. No way to consistently reverse the hash.
        #  Security threat is low that a student gets hacked.

        # hashed_passcode = bcrypt.hashpw(
        # bytes(passcode, encoding='utf-8'), bcrypt.gensalt())

        student = Student(
            first_name=first_name,
            last_name=last_name,
            passcode=passcode,
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
