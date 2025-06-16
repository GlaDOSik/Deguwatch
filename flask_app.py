import logging

from flask import Flask, g

from database import DBSession
from endpoint.api import api_blueprint
from endpoint.api.content_api import content_api
from endpoint.api.entity_api import entity_api
from endpoint.page.dashboard_blueprint import dashboard_blueprint
from endpoint.page.shot_blueprint import shot_blueprint
from vial.blueprint.web_callback import web_callback_blueprint
from service import task_service
from service.webcam_service import webcam_service

logger = logging.getLogger()


def create_app():
    webcam_service.initialize_cameras()
    task_service.initialize_tasks()
    webcam_service.start_updates()
    app = Flask(__name__, template_folder="templates")

    @app.before_request
    def before_request():
        g.transaction_session = DBSession()

    @app.after_request
    def shutdown_session(response):
        transaction_session = getattr(g, "transaction_session", None)

        if transaction_session is None:
            return response

        try:
            transaction_session.commit()
        except BaseException as ex:
            transaction_session.rollback()
            logger.error("Commit failed with error: " + str(ex))
        finally:
            transaction_session.close()

        return response

    register_blueprints(app)
    return app

def register_blueprints(app: Flask):
    app.register_blueprint(dashboard_blueprint)
    app.register_blueprint(shot_blueprint)

    api_blueprint.register_blueprint(content_api)
    api_blueprint.register_blueprint(web_callback_blueprint)
    api_blueprint.register_blueprint(entity_api)
    app.register_blueprint(api_blueprint)