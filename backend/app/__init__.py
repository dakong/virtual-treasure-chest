import os
import os.path as op
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from sqlalchemy.event import listens_for
from flask_migrate import Migrate

from app.config import config


db = SQLAlchemy()
# Create directory for file fields to use
file_path = op.join(op.dirname(__file__), 'images', 'treasure_items')


def create_app():
    """Construct the core application."""
    # Initialize our flask app
    app = Flask(__name__, static_folder='images')
    # Initialize our database and ORM
    # app.config['SQLALCHEMY_DATABASE_URI'] = config['DB']
    # app.config['FLASK_ADMIN_SWATCH'] = 'flatly'
    # app.secret_key = config['SECRET_KEY']

    app.config.from_object("config.Config")
    db.init_app(app)

    migrate = Migrate(app, db, compare_type=True)

    try:
        os.mkdir(file_path)
    except OSError:
        pass
    print(db)
    with app.app_context():
        print('creating app')

        from app import routes  # Import routes
        from app.models.student import Student
        from app.models.treasure_item import TreasureItem
        from app.views.student import StudentView
        from app.views.treasure_item import TreasureItemView

        @listens_for(TreasureItem, 'after_delete')
        def del_image(mapper, connection, target):
            if target.image_path:
                # Delete image
                try:
                    os.remove(op.join(file_path, target.image_path))
                except OSError:
                    pass

                # Delete thumbnail
                try:
                    os.remove(op.join(file_path,
                                      form.thumbgen_filename(target.image_path)))
                except OSError:
                    pass

        # db.create_all()  # Create database tables for our data models
        admin = Admin(app, name='Virtual Treasure Chest',
                      template_mode='bootstrap4')
        admin.add_view(StudentView(Student, db.session))
        admin.add_view(TreasureItemView(TreasureItem, db.session))
        return app
