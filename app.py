#!/usr/bin/env python

from flask import Flask, request, render_template, url_for, redirect, session
from humanapi import get_authorize_url, get_auth_session

import settings

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        redirect_uri = url_for('humanapi_callback', _external=True)
        authorize_url = get_authorize_url(redirect_uri)
        return redirect(authorize_url)

    # Display intro page with login button that posts to here
    return render_template('index.html')


@app.route('/humanapi/callback')
def humanapi_callback():
    # Get code from response
    code = request.args.get('code')
    if not code:
        return 'Error: code parameter must be provided in oauth2 callback', 400

    # Get an authorized session with HumanAPI
    auth_session = get_auth_session(code)

    # Fetch user profile
    profile = auth_session.get('profile').json()
    print profile

    session['id'] = profile['userId'] 
    session['email'] = profile['email'] 
    session['access_token'] = auth_session.access_token

    # Redirect to location page
    return redirect(url_for('profile'))


@app.route('/profile')
def profile():
    # Profile data is pulled from session and populated from humanapi_callback
    return render_template('profile.html')


@app.route('/location')
def location():
    # TODO: Pull in user's location data

    # display in template
    return render_template('location.html')


if __name__ == '__main__':
    app.run(debug=True)
