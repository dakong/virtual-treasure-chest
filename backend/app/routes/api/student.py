from flask import current_app as app, request, session
from app import db
from app.utils.response_generator import generateSuccessResponse, generateFailResponse, generateErrorResponse
from app.model.student import Student


@ app.route('/api/student', methods=['GET', 'POST'])
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
