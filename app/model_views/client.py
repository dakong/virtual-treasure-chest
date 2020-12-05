import os.path as op
from flask import url_for, render_template, redirect, session as app_session

from app.models.student import Student
from app.models.treasure_item import TreasureItem


def get_students():
    students = Student.query.with_entities(
        Student.id, Student.first_name, Student.last_name, Student.profile_image).filter_by(active=True).all()
    students_object = []

    for row in students:
        profile_image = 'default-profile.png'
        s = dict()
        s['id'] = row.id
        s['name'] = row.first_name + ' ' + row.last_name

        if row.profile_image is not None:
            profile_image = row.profile_image

        s['image'] = op.join('/static', 'images',
                             'profile', profile_image)
        students_object.append(s)

    return students_object


def get_treasure_items():
    treasure_items = TreasureItem.query.with_entities(
        TreasureItem.id,
        TreasureItem.cost,
        TreasureItem.name,
        TreasureItem.description,
        TreasureItem.quantity,
        TreasureItem.image_path
    ).filter_by(active=True).all()
    treasure_items_object = []

    for row in treasure_items:
        treasure_items_object.append({
            'id': row.id,
            'cost': row.cost,
            'name': row.name,
            'description': row.description,
            'quantity': row.quantity,
            'image_path': row.image_path,
        })

    return treasure_items_object


def get_current_student(id):
    student = Student.query.get(id)

    return {
        'id': student.id,
        'name': student.first_name + ' ' + student.last_name,
        'profile_image': student.profile_image,
        'points': student.points
    }


def student_home_view():
    authenticated = False
    if 'studentID' in app_session:
        authenticated = True

    if authenticated is True:
        return redirect(url_for('shop'))

    students = get_students()

    return render_template(
        'index.html',
        students=students,
        current_student={},
        treasure_items=[],
        authenticated=authenticated,
        environment='development'
    )


def authenticated_shop_view():
    authenticated = False
    if 'studentID' in app_session:
        authenticated = True

    if authenticated is False:
        return redirect(url_for('index'))

    students = get_students()
    treasure_items = get_treasure_items()
    print(app_session['studentID'])
    current_student = get_current_student(app_session['studentID'])

    return render_template(
        'index.html',
        students=students,
        current_student=current_student,
        treasure_items=treasure_items,
        authenticated=authenticated,
        environment='development'
    )
