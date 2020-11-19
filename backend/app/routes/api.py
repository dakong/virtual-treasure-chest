import bcrypt
from flask import current_app as app, request, session
from app import db

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
