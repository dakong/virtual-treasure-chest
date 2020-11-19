from app.model_views.model_view_base import ModelViewAuth


class StudentView(ModelViewAuth):
    column_editable_list = ('points',)
    column_filters = ('first_name', 'last_name')
    column_searchable_list = ('first_name', 'last_name')
    column_exclude_list = ('active',)
    export_types = ['csv', 'xlsx']
