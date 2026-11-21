import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'application.sqlite'),
    )

    # if test_config is None:
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    from . import questions_db as q_db
    q_db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import lecture
    app.register_blueprint(lecture.bp)
    app.add_url_rule('/', endpoint='index') #The lecture is the main feature of the application - this makes sense to be the main index

    return app