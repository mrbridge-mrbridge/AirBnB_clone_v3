#!/usr/bin/python3
"""
Creates first Endpoint for our API
"""

from models import storage
from flask import Flask, jsonify, make_response
from api.v1.views import app_views
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app, origins="0.0.0.0")
app.register_blueprint(app_views)


@app.teardown_appcontext
def tearDown():
    """Closes each SQLAlchemyTask"""
    storage.close()


@app.errorhandler(404)
def errnot():
    """Error 404"""
    make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host_origin = os.getenv['HBNB_API_HOST']
    port_origin = os.getenv['HBNB_API_PORT']
    if not host_origin:
        host_origin = '0.0.0.0'
    if not port_origin:
        port_origin = '5000'
    app.run(host=host_origin,
            port=port_origin,
            threaded=True)
