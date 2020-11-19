from flask import current_app as app, request, session
from app import db
from app.utils.response_generator import generateSuccessResponse, generateFailResponse, generateErrorResponse
from app.model.teacher import Teacher


@ app.route('/api/teacher', methods=['POST'])
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
