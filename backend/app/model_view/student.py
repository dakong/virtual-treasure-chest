from flask import session
from flask_admin.contrib.sqla import ModelView


class StudentView(ModelView):
    def is_accessible(self):
        return 'userID' in session

    column_editable_list = ('points',)
    column_filters = ('first_name', 'last_name')
    column_searchable_list = ('first_name', 'last_name')
    column_exclude_list = ('active',)
    export_types = ['csv', 'xlsx']
