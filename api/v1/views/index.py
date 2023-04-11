#!/usr/bin/python3
"""index module"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status_route():
    return jsonify({'status': 'OK'})
