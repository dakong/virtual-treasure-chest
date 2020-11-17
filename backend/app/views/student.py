from flask_admin.contrib.sqla import ModelView


class StudentView(ModelView):
    can_export = True
    column_editable_list = ('points',)
    column_filters = ('first_name', 'last_name')
    column_searchable_list = ('first_name',)

    export_types = ['csv', 'xlsx']
