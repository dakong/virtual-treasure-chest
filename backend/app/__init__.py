import os
import os.path as op
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_migrate import Migrate
from app.model_view.admin import MyAdminIndexView

# Create global db object and global file_path for other modules to access
db = SQLAlchemy()
# Where we will store images for treasure_items
file_path = op.join(op.dirname(__file__), 'static', 'images', 'treasure_items')


def create_app():
    """Construct the core application."""
    # Initialize our flask app and database
    app = Flask(__name__, template_folder='template', static_folder='static')
    app.config.from_object("config.Config")
    db.init_app(app)
    migrate = Migrate(app, db, compare_type=True)

    # Create directory if it does not exist
    try:
        os.mkdir(file_path)
    except OSError:
        pass

    # test_request_context is needed in order to use url_for in this file.
    # will need to remove this line when we go into production.
    with app.app_context(), app.test_request_context():
        # Initialize routes for the application
        from app import routes
        from app.model.student import Student
        from app.model.treasure_item import TreasureItem
        from app.model.transaction import Transaction
        from app.model_view.student import StudentView
        from app.model_view.treasure_item import TreasureItemView
        from app.model_view.transaction import TransactionView

        # Create database tables for our data models
        # db.create_all()

        # Setup admin views
        admin = Admin(app, name='Virtual Treasure Chest',
                      template_mode='bootstrap4',
                      index_view=MyAdminIndexView())
        admin.add_view(StudentView(Student, db.session))
        admin.add_view(TreasureItemView(TreasureItem, db.session))
        admin.add_view(TransactionView(Transaction, db.session))
        admin.add_link(MenuLink(name='Logout',
                                category='', url=url_for('logout')))

        return app
