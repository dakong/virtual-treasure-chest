import bcrypt
from flask import current_app as app, request, session
from app.database import db

from app.utils.auth import login_required
from app.utils.response_generator import generateSuccessResponse, generateFailResponse, generateErrorResponse
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.transaction import Transaction
from app.models.treasure_item import TreasureItem


def student():
    if request.method == 'POST':
        studentData = request.get_json()
        # need to hash the passwords when we save
        passcode = studentData['passcode']
        first_name = studentData['first_name']
        last_name = studentData['last_name']

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


def teacher():
    # Create a way where only I can create teachers
    teacherData = request.get_json()
    password = teacherData['password']
    first_name = teacherData['first_name']
    last_name = teacherData['last_name']
    username = teacherData['username']

    hashed_password = bcrypt.hashpw(
        bytes(password, encoding='utf-8'), bcrypt.gensalt())

    teacher = Teacher(
        active=True,
        first_name=first_name,
        last_name=last_name,
        password=hashed_password,
        username=username
    )

    db.session.add(teacher)
    db.session.commit()

    return generateSuccessResponse({
        'teacher': {
            'id': teacher.id,
            'name': teacher.username
        }
    })


def transaction():
    transaction = request.get_json()

    transaction = Transaction(
        active=True,
        student_id=transaction['student_id'],
        treasure_item_id=transaction['treasure_item_id'])

    db.session.add(transaction)
    db.session.commit()

    return generateSuccessResponse({
        'transaction': {
            'id': transaction.id,
            'student_id': transaction.student_id,
            'treasure_item_id': transaction.treasure_item_id
        }
    })


@ login_required
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


def purchase():
    purchase_details = request.get_json()
    student_id = purchase_details['student_id']
    treasure_item_id = purchase_details['treasure_item_id']

    # first check if student has sufficient funds, and if quantity of treasure item is enough
    treasure_item = TreasureItem.query.get(treasure_item_id)
    student = Student.query.get(student_id)

    if treasure_item.cost > student.points:
        return generateFailResponse({'message': 'Student has insufficient funds'})

    if treasure_item.quantity <= 0:
        return generateFailResponse({'message': 'Item is out of stock'})

    # If it does than subract cost of item from the total number of points the student has
    # and decrement quantity of items
    student.points = student.points - treasure_item.cost
    treasure_item.quantity = treasure_item.quantity - 1

    # Create a transaction log to record this purchase
    txn = Transaction(active=True, student_id=student_id,
                      treasure_item_id=treasure_item_id)
    db.session.add(txn)
    db.session.commit()

    return generateSuccessResponse({
        'student': {
            'id': student.id,
            'points': student.points
        },
        'treasure_item': {
            'id': treasure_item.id,
            'quantity': treasure_item.quantity
        }
    })