"""
请求错误处理
"""
from . import code, pretty_result
from flask import jsonify, current_app


def register_errors(app):

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify(pretty_result(code.FORBIDDEN_ERROR,data=str(e)))

    @app.errorhandler(404)
    def database_not_found_error_handler(e):
        return jsonify(pretty_result(code.NOT_EXIST_ERROR,data=str(e)))

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify(pretty_result(code.METHOD_NOT_ALLOW_ERROR,data=str(e)))

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify(pretty_result(code.SERVER_ERROR,data=str(e)))

    # The default_error_handler function as written above will not return any response if the Flask application
    # is running in DEBUG mode.
    @app.errorhandler
    def default_error_handler(e):
        message = 'An unhandled exception occurred. -> {}'.format(str(e))
        # logger.error(message)
        current_app.logger.error(message)
        # if not settings.FLASK_DEBUG:
        return jsonify(pretty_result(code.UNKNOWN_ERROR,data=str(e)))