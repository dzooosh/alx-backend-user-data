#!/usr/bin/env python3
""" Basic Flask app
"""
from auth import Auth
from flask import Flask, jsonify, request, abort


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def index():
    """ return a JSON message
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users():
    """ returns JSON of the new user or alert if existing
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if email and password:
        # Register the user with the provided email and password
        try:
            user = AUTH.register_user(email, password)
            return jsonify({"email": user.email, "message": "user created"})
        except ValueError:
            return jsonify({"message": "email already registered"}), 400
    else:
        return jsonify({'error': 'Email and password are required.'}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ login route logic
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email and password:
        # Email and Password are present
        if not AUTH.valid_login(email, password):
            # User is not authenticated
            abort(401)
        else:
            # User is authenticated
            session_id = AUTH.create_session(email)
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie("session_id", session_id)
            return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
