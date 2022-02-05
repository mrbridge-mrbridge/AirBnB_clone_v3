"""
Creates first Endpoint for our API
"""

from models import storage
from flask import Flask, jsonify, make_response
from api.v1.views import app_views
import os



app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def tearDown():
    """Closes each SQLAlchemyTask"""
    storage.close()

@app.errorhandler(404)
def errnot():
    """Error 404"""
    make_response(jsonify({"error": "Not Found"}), 404)

host_origin = os.environ['HBNB_API_HOST', '0.0.0.0']
port_origin = os.environ['HBNB_API_PORT', 5000]

if __name__ == "__main__":
    app.run(host=host_origin, port=port_origin, threaded = True)
