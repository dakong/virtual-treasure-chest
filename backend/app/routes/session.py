import bcrypt
from flask import current_app as app, request, session, url_for, render_template, redirect

from app.utils.response_generator import generateSuccessResponse, generateFailResponse, generateErrorResponse
from app.model.student import Student
from app.model.teacher import Teacher
from app.model_view.login_form import login_form


@app.route('/boba')
def loginForm():
    return render_template('login.html', form=login_form)


@app.route('/login', methods=['POST'])
def login():
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


@ app.route('/verify', methods=['POST'])
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


@ app.route('/logout')
def logout():
    session.pop('userID', None)
    return redirect(url_for('loginForm'))
