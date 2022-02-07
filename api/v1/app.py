#!/usr/bin/python3
"""
Creates first Endpoint for our API
"""

from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, make_response, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_db(error):
    """
     Close Storage for SQLAlchemy
     Database
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Error 404 and this a error handler
    """
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    """
    Main Function for the hosts and portss
    """
    host_orgin = environ.get('HBNB_API_HOST')
    port_orgin = environ.get('HBNB_API_PORT')
    if not host_orgin:
        host = '0.0.0.0'
    if not port_orgin:
        port = '5000'
    app.run(host=host_orgin, port=port_orgin, threaded=True)

