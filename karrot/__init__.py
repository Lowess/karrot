#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import structlog

from flask import Flask, redirect, url_for, render_template, send_from_directory
from karrot.reporters.factory import ReporterFactory
from karrot.config.logger import Logger

# Init application logging
Logger().init(os.getenv("KARROT_LOG", "INFO"))
logger = structlog.get_logger()
# Lower some logging levels
structlog.get_logger("botocore").setLevel(logging.CRITICAL)
structlog.get_logger("urllib3").setLevel(logging.WARN)


def create_app():

    app = Flask(__name__)

    # Make context available in blueprints
    app.app_context().push()

    ################################################################################
    # Override with specific settings based on the FLASK_ENV env var
    ################################################################################

    if "FLASK_ENV" in os.environ:
        if os.environ["FLASK_ENV"] == "prod":
            app.config.from_object("karrot.config.config.ProductionConfig")
        else:
            logger.setLevel(logging.DEBUG)
            app.config.from_object("karrot.config.config.DevelopmentConfig")
    else:
        logger.setLevel(logging.DEBUG)
        app.config.from_object("karrot.config.config.DevelopmentConfig")

    ################################################################################
    # Configure list of active reporters
    ################################################################################
    app.config["REPORTERS"] = {}

    for reporter in app.config["KARROT_REPORTERS"]:
        logger.debug("Initializing reporter", reporter=reporter)
        app.config["REPORTERS"][reporter] = ReporterFactory.get(reporter=reporter)

    logger.info(
        "Karrot initialized with the following reporters",
        reporters=app.config["REPORTERS"].keys(),
    )

    ################################################################################
    # Blueprints registration
    ################################################################################

    from karrot.burrow.controllers import burrow
    from karrot.heartbeat.controllers import heartbeat
    from karrot.config.controllers import config
    from karrot.reporters.controllers import reporters
    from karrot.reporters.prometheus.controllers import prometheus

    app.register_blueprint(burrow)
    app.register_blueprint(heartbeat)
    app.register_blueprint(config)
    app.register_blueprint(reporters)
    app.register_blueprint(prometheus)

    @app.route("/", methods=["GET"])
    def index(error=None):
        return redirect(url_for("heartbeat.health"))

    @app.route("/favicon.ico")
    def favicon():
        return send_from_directory(
            os.path.join(app.root_path, "static"),
            "img/favicon.ico",
            mimetype="image/vnd.microsoft.icon",
        )

    ################################################################################
    # Global errors handling
    ################################################################################

    if not app.config["DEBUG"]:

        @app.errorhandler(500)
        def internal_server_error(error):
            return render_template("error.html", error=str(error), code=500), 500

        @app.errorhandler(404)
        def page_not_found(error):
            return render_template("error.html", error=str(error), code=404), 404

        @app.errorhandler(Exception)
        def exception_handler(error):
            return render_template("error.html", error=error)

    return app
