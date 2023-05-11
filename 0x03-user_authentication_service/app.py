#!/usr/bin/env python3
""" Basic Flask app
"""
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect, url_for

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def index() -> str:
    """ return a JSON message
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users() -> str:
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


@app.route('/sessions', methods=["POST"], strict_slashes=False)
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
        # User is authenticated
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response


@app.route('/sessions', methods=["DELETE"], strict_slashes=False)
def logout():
    """ logout logic
    """
    session_id = request.cookies.get('session_id', None)
    if session_id is not None:
        # Session id is present
        user = AUTH.get_user_from_session_id(session_id)
        # Destroy the session
        if user:
            AUTH.destroy_session(user.id)
            redirect('/')
    # respond with a 403 HTTP status if any step is None
    abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """ profile route logic
    """
    session_id = request.cookies.get('session_id', None)
    user = AUTH.get_user_from_session_id(session_id)
    if user is not None and session_id is not None:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """ gets the reset password token
    """
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
