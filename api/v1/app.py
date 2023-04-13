#!/usr/bin/python3
"""API module"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os


a_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
a_port = os.getenv('HBNB_API_PORT', 5000)

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(exeption):
    """Close current session"""
    storage.close()


@app.errorhandler(404)
def err_handler(error):
    """a handler for 404 errors that returns a JSON-formatted
        404 status code response"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host=a_host, port=a_port, threaded=True, debug=True)
