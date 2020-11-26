import os
import os.path as op
from flask import Flask, url_for, render_template, session as app_session
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_migrate import Migrate

from app.database import db

# Where we will store images for treasure_items
file_path = op.join(op.dirname(__file__), 'static', 'images')
static_path = file_path = op.join(op.dirname(__file__), 'static')


def create_app(config_object):
    """Construct the core application."""
    # Initialize our flask app and database
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_object)
    db.init_app(app)
    migrate = Migrate(app, db, compare_type=True, render_as_batch=True)

    # Create directory if it does not exist
    try:
        os.mkdir(file_path)
    except OSError:
        pass

    with app.app_context():
        from app.routes import session, api
        from app.models.student import Student
        from app.models.treasure_item import TreasureItem
        from app.models.transaction import Transaction
        from app.model_views.admin import MyAdminIndexView
        from app.model_views.student import StudentView
        from app.model_views.treasure_item import TreasureItemView
        from app.model_views.transaction import TransactionView

        # Create database tables for our data models
        db.create_all()

        # Initialize routes for the application
        app.add_url_rule('/login/', 'login', session.login,
                         methods=['POST', 'GET'])
        app.add_url_rule('/verify/', 'verify',
                         session.verify, methods=['POST'])
        app.add_url_rule('/logout/', 'logout', session.logout)
        app.add_url_rule('/api/student/', 'student',
                         api.student, methods=['GET', 'POST'])
        app.add_url_rule('/api/teacher/', 'teacher',
                         api.teacher, methods=['POST'])
        app.add_url_rule('/api/treasureitem/', 'treasure_item',
                         api.treasure_item, methods=['GET', 'POST'])
        app.add_url_rule('/api/transaction/', 'transaction',
                         api.transaction, methods=['POST'])
        app.add_url_rule('/api/purchase/', 'purchase',
                         api.purchase, methods=['POST'])

        def index_view():
            students = Student.query.with_entities(
                Student.id, Student.first_name, Student.last_name, Student.profile_image).filter_by(active=True).all()

            students_object = []
            authenticated = False
            if 'userID' in app_session:
                authenticated = True
            for row in students:
                profile_image = 'default-profile.png'
                s = dict()
                s['id'] = row.id
                s['name'] = row.first_name + ' ' + row.last_name

                if row.profile_image is not None:
                    profile_image = row.profile_image

                s['image'] = op.join('/static', 'images',
                                     'profile', profile_image)
                students_object.append(s)

            return render_template('index.html', students=students_object, authenticated=authenticated, environment='development')

        app.add_url_rule('/', 'index', index_view, methods=['GET'])

        def page_not_found(error):
            return render_template('404.html'), 404

        app.register_error_handler(404, page_not_found)

        # Setup admin views
        admin = Admin(app, name='Virtual Treasure Chest',
                      template_mode='bootstrap4',
                      index_view=MyAdminIndexView())
        admin.add_view(StudentView(Student, db.session))
        admin.add_view(TreasureItemView(TreasureItem, db.session))
        admin.add_view(TransactionView(Transaction, db.session))
        admin.add_link(MenuLink(name='Logout',
                                category='', url='/logout'))

        return app
