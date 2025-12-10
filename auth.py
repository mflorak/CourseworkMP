from flask import jsonify, make_response
from flask_httpauth import HTTPBasicAuth
from models import User

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or user.password != password:
        return False
    return True

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)