import bcrypt
from flask import current_app as app, request, session, url_for, render_template, redirect

from app.utils.response_generator import generateSuccessResponse, generateFailResponse, generateErrorResponse
from app.models.student import Student
from app.models.teacher import Teacher
from app.model_views.login_form import login_form


def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        teacher = Teacher.query.filter_by(username=username).first()

        if teacher == None:
            return render_template('login.html', form=login_form, fail=True)

        if bcrypt.checkpw(bytes(password, encoding='utf-8'), teacher.password):
            # password match. Let's store user session
            session['userID'] = teacher.id
            return redirect(url_for('admin.index'))

        return render_template('login.html', form=login_form, fail=True)

    if request.method == 'GET':
        return render_template('login.html', form=login_form, fail=False)


def verify():
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


def logout():
    session.pop('userID', None)
    return redirect(url_for('login'))
