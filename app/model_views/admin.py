import os.path as op
from flask import session, render_template
from flask_admin import AdminIndexView, expose
from app.models.student import Student


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def home(self):
        students = Student.query.with_entities(
            Student.id, Student.first_name, Student.last_name, Student.profile_image, Student.points).filter_by(active=True).all()

        students_object = []

        for row in students:
            profile_image = 'default-profile.png'
            s = dict()
            s['id'] = row.id
            s['name'] = row.first_name + ' ' + row.last_name
            s['points'] = row.points

            if row.profile_image is not None:
                profile_image = row.profile_image

            s['image'] = op.join('/static', 'images',
                                 'profile', profile_image)
            students_object.append(s)

        return self.render('home.html', students=students_object, environment='development')

    def is_accessible(self):
        return 'userID' in session

    def inaccessible_callback(self, name, **kwargs):
        return render_template('404.html'), 404
