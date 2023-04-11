#!/usr/bin/python3
"""API module"""
from flask import Flask
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


if __name__ == "__main__":
    app.run(host=a_host, port=a_port, threaded=True, debug=True)
