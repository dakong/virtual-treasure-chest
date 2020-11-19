from flask import session, render_template
from flask_admin import AdminIndexView


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return 'userID' in session

    def inaccessible_callback(self, name, **kwargs):
        return render_template('404.html'), 404
