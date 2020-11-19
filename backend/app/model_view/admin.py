from flask import session
from flask_admin import AdminIndexView


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return 'userID' in session
