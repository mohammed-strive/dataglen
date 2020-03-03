from flask import Flask
import os

def create_app(config=None):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='development',
        DATABASE=os.path.join(app.instance_path, 'dataglen.sqlite')
    )

    if config is not None:
        app.config.from_pyfile(config, silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    from . import sensor
    app.register_blueprint(sensor.bp)
    app.register_blueprint(auth.bp)

    return app