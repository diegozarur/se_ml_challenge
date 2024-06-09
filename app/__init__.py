import os
from flask import Flask
from flask_cors import CORS
from app.api import api_bp
import logging
from celery import Celery

from config import Config


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app(config_name: Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_name)

    CORS(app)
    app.register_blueprint(api_bp, url_prefix='/api')

    upload_directory = os.path.join(app.root_path, config_name.UPLOAD_FOLDER)

    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory)
    app.config["UPLOAD_FOLDER"] = upload_directory
    logging.info(f"Upload directory set to: {upload_directory}")

    celery = make_celery(app)

    app.extensions["celery"] = celery

    return app
