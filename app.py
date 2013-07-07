#!/usr/bin/env python

from flask import Flask, request, render_template, url_for, redirect, session, flash
from humanapi import get_authorize_url, get_auth_session, recreate_session
from datetime import datetime, timedelta
import json

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

@app.route('/humanapi', methods=['GET', 'POST'])
def humanapi():
    if request.method == 'POST':
        redirect_uri = url_for('humanapi_callback', _external=True)
        authorize_url = get_authorize_url(redirect_uri)
        return redirect(authorize_url)

    # Display intro page with login button that posts to here
    return render_template('humanapi.html')

@app.route('/humanapi/callback')
def humanapi_callback():
    # Get code from response
    code = request.args.get('code')
    if not code:
        return 'Error: code parameter must be provided in oauth2 callback', 400

    session['logged_in'] = True

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

    profile_session = recreate_session(session['access_token'])
    session_all(profile_session)
    long_series_activity(7, profile_session)

    flash(chartData())
    return render_template('profile.html')

@app.route('/chartData')
def chartData():
  # Returns json weight time series data

    chart_session = recreate_session(session['access_token'])
    session_all(chart_session)
    long_series_activity(7, chart_session)
    series_data = session['long_series_activity']

    return series_data

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/team')
def team():
    return render_template('team.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for(''))

# ----------- Human API starts here ----------------

# All events
def session_all(x_session):
  profile(x_session)
  summary(x_session)
  all_activity(x_session)
  all_blood_glucose(x_session)
  all_blood_pressures(x_session)
  all_bmis(x_session)
  all_body_fats(x_session)
  all_heart_rates(x_session)
  all_heights(x_session)
  all_locations(x_session)
  all_sleep(x_session)
  all_weight(x_session)

# Profile
def profile(x_session):
  session['profile'] = x_session.get("profile").json()


def summary(x_session):
  session['summary'] = x_session.get("").json()


# Activity
def all_activity(x_session):
  session['all_activity'] = x_session.get("activity").json()

def activity(id, x_session):
  session['activity'] = x_session.get("activity/{0}".format(id)).json()

def daily_activity(date, x_session):
  session['daily_activity'] = x_session.get("activity/daily/{0}".format(date.strftime('%Y-%m-%d'))).json()

def series_activity(date, x_session):
 session['series_activity'] = x_session.get("activity/series/{0}".format(date.strftime('%Y-%m-%d'))).json()

def long_series_activity(daysago, x_session):
  if daysago < 0:
    return None

  end_dt = datetime.now()
  long_series = {}
  for i in reversed(range(daysago)):
    series_activity(end_dt - timedelta(i), x_session)
    day_series = session['series_activity']
    if day_series:
        long_series.update(day_series)

  session['long_series_activity'] = json.dumps(long_series) 

# Blood Glucose
def all_blood_glucose(x_session):
  session['all_blood_glucose'] = x_session.get("blood_glucose").json()

def blood_glucose(id, x_session):
  session['blood_glucose'] = x_session.get("blood_glucose/{0}".format(id)).json()

def daily_blood_glucose(date, x_session):
  session['daily_blood_glucose'] = x_session.get("blood_glucose/daily/{0}".format(date.strftime('%Y-%m-%d'))).json()


# Blood presure
def all_blood_pressures(x_session):
  session['all_blood_pressures'] = x_session.get("blood_pressure").json()

def blood_pressure(id, x_session):
    session['blood_pressure'] = x_session.get("blood_pressure/{0}".format(id)).json()

def daily_blood_pressure(date, x_session):
  session['daily_blood_pressure'] = x_session.get("blood_pressure/daily/{0}".format(date.strftime('%Y-%m-%d'))).json()


# BMI
def all_bmis(x_session):
  session['all_bmis'] = x_session.get("bmi").json()

def bmi(id, x_session):
  session['bmi'] = x_session.get("bmi/#{id}").json()

def daily_bmi(date, x_session):
  session['daily_bmi'] = x_session.get("bmi/daily/{0}".format(date.strftime('%Y-%m-%d'))).json()


# Body fat
def all_body_fats(x_session):
  session['all_body_fats'] = x_session.get("body_fat").json()

def body_fat(id, x_session):
  session['body_fat'] = x_session.get("body_fat/{0}".format(id)).json()

def daily_body_fat(date, x_session):
  session['daily_body_fat'] = x_session.get("body_fat/daily/{0}".format(date.strftime('%Y-%m-%d'))).json()


# Genetics
def genetic_traits(x_session):
  session['genetic_traits'] = x_session.get("genetic/traits").json()


# Heart rate
def all_heart_rates(x_session):
  session['all_heart_rates'] = x_session.get("heart_rate").json()

def heart_rate(id, x_session):
  session['heart_rate'] = x_session.get("heart_rate/{0}".format(id)).json()

def daily_heart_rate(date, x_session):
  session['daily_heart_rate'] = x_session.get("heart_rate/daily/{0}".format(date.strftime('%Y-%m-%d'))).json()


# Height
def all_heights(x_session):
  session['all_heights'] = x_session.get("height").json()

def height(id, x_session):
  session['height'] = x_session.get("height/#{id}").json()

def daily_height(date, x_session):
  session['daily_height'] = x_session.get("height/daily/{0}".format(date.strftime('%Y-%m-%d'))).json()


# Location
def all_locations(x_session):
  session['all_locations'] = x_session.get("location").json()

def daily_location(date, x_session):
  session['daily_location'] = x_session.get("location/daily/{0}".format(date.strftime('%F'))).json()


# Sleep
def all_sleep(x_session):
  session['all_sleep'] = x_session.get("sleep").json()

def sleep(id, x_session):
  session['sleep'] = x_session.get("sleep/{0}".format(id)).json()

def daily_sleep(date, x_session):
  session['daily_sleep'] = x_session.get("sleep/daily/{0}".format(date.strftime('%F'))).json()


# Weight
def all_weight(x_session):
  session['all_weight'] = x_session.get("weight").json()

def weight(id, x_session):
  session['weight'] = x_session.get("weight/{0}".format(id)).json()

def daily_weight(date, x_session):
  session['daily_weight'] = x_session.get("weight/daily/{0}".format(date.strftime('%F'))).json()
  
# ----------- Human API ends here ----------------

if __name__ == '__main__':
    app.run(debug=True)



