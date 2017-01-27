"""
Routes and views for the Flask application.
"""

from flask import render_template, request, session, redirect, url_for, flash
from urllib2 import Request, urlopen, URLError
import json
from CourseGrab import app
from CourseGrab.models.sql_client import Client
from CourseGrab import google


@app.route('/')
@app.route('/home')
def index():
    courses = None
    access_token = session.get('access_token')
    if access_token is not None:
        user_dict = get_user_dict()
        user_id = user_dict["id"]
        client = Client()
        courses = client.get_courses(str(user_id))
    return render_template('index.html', courses = courses)


@app.route('/sign_in')
def sign_in():
    callback = url_for('authorized', _external = True)
    return google.authorize(callback=callback)
 
 
@app.route('/oauth2callback')
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('index'))
 
 
@google.tokengetter
def get_access_token():
    return session.get('access_token')


@app.route('/submitted', methods = ['POST'])
def submit_request():
    if session.get('access_token') is None:
        # need to notify user to sign in. Right now it's redirecting to sign in, but
        # the entered course isn't being tracked.
        return redirect(url_for('sign_in'))
    else:
        user_dict = get_user_dict()
        user_id = user_dict["id"]
        user_email = user_dict["email"]

        course_code = request.form["course_number"]
        client = Client()
        try:
            client.submit_request(user_id, user_email, course_code)
            client.connection.close()
        except UserWarning as err:
            if err == "This course number does not exist.":
                flash('This course number does not exist.')
                return render_template('templates/index.html')
            elif err == "You are already tracking this course.":
                flash("You are already tracking this course.")
                return render_template('templates/index.html')
            elif err == "You cannot track more than three courses at a time.":
                flash("You cannot track more than three courses at a time.")
                return render_template('templates/index.html')


    return redirect(url_for('index'))


@app.route('/remove/<int:course_num>', methods = ['POST'])
def remove(course_num):
    user_dict = get_user_dict()
    user_id = user_dict["id"]
    client = Client()
    client.remove_course(user_id, course_num)
    return redirect(url_for('index'))


@app.route('/sign_out')
def sign_out():
    # remove the token from the session if it's there
    session.pop('access_token', None)
    return redirect(url_for('index'))


def get_user_dict():
    access_token = session.get('access_token')
    assert access_token is not None
    access_token = access_token[0]
    headers = {'Authorization': 'OAuth ' + access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    res = urlopen(req)
    
    return json.loads(res.read())


@app.errorhandler(400)
def bad_request(e):
    return "400 error", 400


@app.errorhandler(404)
def page_not_found(e):
    return "404 error", 404


@app.errorhandler(500)
def internal_server_error(e):
    return "500 error", 500
