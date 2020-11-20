import os
import os.path as op
from flask import Flask, url_for, render_template
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_migrate import Migrate

from app.database import db

# Where we will store images for treasure_items
file_path = op.join(op.dirname(__file__), 'static', 'images', 'treasure_items')


def create_app(config_object):
    """Construct the core application."""
    # Initialize our flask app and database
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_object)
    db.init_app(app)
    migrate = Migrate(app, db, compare_type=True)

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
