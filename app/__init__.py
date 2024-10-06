from flask import Flask
from .main import create_dash_app
# from flask_mail import Mail
# from flask_moment import Moment
from .extensions import db
from config import config

# mail = Mail()
# moment = Moment()
# db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # mail.init_app(app)
    # moment.init_app(app)
    db.init_app(app)

    # Create the tables (inside the app context)
    with app.app_context():
        db.create_all()

    models_to_load = [cls for cls in db.Model.__subclasses__() \
                  if (cls.__name__ != "Base" \
                      and cls.__name__ in app.config['MODELS_TO_LOAD'])]
    
    tbl_cls_cols = {cls.__tablename__: {'object': cls, 'cols': cls.__table__.columns.keys()} \
                for cls in models_to_load}

    dash_app = create_dash_app(app, tbl_cls_cols)

    return app, dash_app