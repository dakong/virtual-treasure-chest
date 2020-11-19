from flask import session, render_template
from flask_admin.contrib.sqla import ModelView


class ModelViewAuth(ModelView):
    def is_accessible(self):
        return 'userID' in session

    def inaccessible_callback(self, name, **kwargs):
        return render_template('404.html'), 404
