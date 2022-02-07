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


host_origin = os.environ['HBNB_API_HOST', '0.0.0.0']
port_origin = int(os.environ['HBNB_API_PORT', 5000])

if __name__ == "__main__":
    app.run(host=host_origin,
            port=port_origin,
            threaded=True)
