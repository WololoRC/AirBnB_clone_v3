#!/usr/bin/python3
"""index module"""
from flask import jsonify
from viwes import app_views

@app_views('/status', methods=['GET'])
def status_route():
    return jsonify({'status': 'OK'})
