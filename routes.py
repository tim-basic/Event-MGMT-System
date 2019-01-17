from server import app, system
from flask import render_template, flash, request, redirect, url_for, abort
from flask_login import current_user, login_required, login_user, logout_user
from src.EventManager import EventManager 
from src.Event import Seminar, Course
from src.Status import Closed, Cancelled
from src.UserExceptions import *
from datetime import datetime, date
from src.User import Guest

@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        user = system.validate_login(request.form['ID'], request.form['password'])
        if user is None:
            flash("Incorrect username or password")
            return render_template('login.html')
        login_user(user)
        return redirect(url_for('events'))

    if not current_user.is_anonymous:
        return redirect(url_for('events'))

    return render_template('login.html')

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/guest_register', methods=['POST','GET'])
def guest_register():
    if (request.method == "POST"):
        guest = Guest(request.form['password'], request.form['name'], request.form['email'])
        if system.get_user_by_id(guest.ID) is None:
            system.add_user(guest)
            flash("You have successfully registered!")
            return redirect(url_for('login'))
        else:
            flash("Email already registered")
            return redirect(url_for('guest_register'))
    if not current_user.is_anonymous:
        return redirect(url_for('events'))
    return render_template('guest_register.html')

@app.route('/404', methods=['GET'])
@login_required
def event_not_found():
    return render_template('404.html')

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    if current_user.is_staff:
        (curRegEvents, pastRegEvents, openEvents, closedEvents, cancelledEvents, notifications) = system.get_staff_dashboard(current_user)
        return render_template('dashboard.html', 
            crEvents=curRegEvents, 
            prEvents=pastRegEvents, 
            openEvents=openEvents, 
            closedEvents=closedEvents, 
            cancelledEvents=cancelledEvents, 
            notifications=notifications)
    else:
        (curRegEvents, pastRegEvents, notifications) = system.get_student_dashboard(current_user)
        return render_template('dashboard.html', crEvents=curRegEvents, prEvents=pastRegEvents, notifications=notifications)

@app.route('/events', methods=['GET', 'POST'])
@login_required
def events():
    if request.method == 'POST':
        if request.form['filter'] == "courses":
            return render_template('events.html', events=system.available_courses, courses=True)
        elif request.form['filter'] == "seminars":
            return render_template('events.html', events=system.available_seminars, seminars=True)
    return render_template('events.html', events=system.available_all, all=True)

@app.route('/event/<eventName>', methods=['GET'])
@login_required
def display_event(eventName):
    event = system.get_event(eventName)
    if isinstance(event.status, Cancelled) and not event.is_creator(current_user):
        return redirect(url_for('event_not_found'))
    if event.is_creator(current_user):
        attendees = event.attendee_names()
        return render_template('display_event.html', event=event, seminar=isinstance(event, Seminar), attendees=attendees)
    return render_template('display_event.html', event=event, seminar=isinstance(event, Seminar))

@app.route('/create_seminar/<seminarName>/session', methods=['GET', 'POST'])
@login_required
def create_session(seminarName):
    if not current_user.is_staff:
        return redirect(url_for('events'))
    if request.method == 'POST':
        try:
            system.add_session(current_user, seminarName, request.form)
        except CreateSessionError as e:
            return render_template('create_session.html', seminarName=seminarName, message=e.message, form=request.form)
        flash("Session successfully created")
        return redirect(url_for('display_event', eventName=seminarName))
    return render_template('create_session.html', seminarName=seminarName)

@app.route('/create_seminar', methods = ['GET','POST'])
@login_required
def create_seminar():
    if not current_user.is_staff:
        return redirect(url_for('events'))
    if request.method == 'POST':
        try:
            system.create_seminar(current_user, request.form)
        except CreateEventError as e:
            return render_template('create_seminar.html', message=e.message, form=request.form)
        flash("Seminar successfully created")
        return redirect(url_for('display_event', eventName=request.form['eventName']))
    return render_template('create_seminar.html')

@app.route('/create_course', methods = ['GET','POST'])
@login_required
def create_course():
    if not current_user.is_staff:
        return redirect(url_for('events'))
    if request.method == 'POST':
        try:
            system.create_course(current_user, request.form)
        except CreateEventError as e:
            return render_template('create_course.html', message=e.message, form=request.form) 
        flash("Course successfully created")
        return redirect(url_for('display_event', eventName=request.form['eventName']))
    return render_template('create_course.html')

@app.route('/event/<eventName>/edit', methods = ['GET','POST'])
@login_required
def edit_event(eventName):
    if not current_user.is_staff:
        return redirect(url_for('events'))
    event = system.get_event(eventName)
    if request.method == 'POST':
        try:
            system.edit_event(current_user, event, request.form)
        except EditEventError as e:
            return render_template('create_course.html', edit=True, message=e.message, event=event)
        flash("Event successfully edited")
        return redirect(url_for('display_event', eventName=request.form['eventName']))
    return render_template('create_course.html', edit=True, event=event)

@app.route('/event/<seminarName>/sessions', methods=['GET'])
@login_required
def select_session(seminarName):
    if not current_user.is_staff:
        return redirect(url_for('events'))
    seminar = system.get_event(seminarName)
    return render_template('select_session.html', event=seminar)

@app.route('/event/<seminarName>/register', methods = ['GET'])
@login_required
def select_session_registration(seminarName):
    seminar = system.get_event(seminarName)
    return render_template('sessionRegister.html', event=seminar)

@app.route('/event/<seminarName>/<sessionName>/edit', methods=['GET', 'POST'])
@login_required
def edit_session(seminarName, sessionName):
    if not current_user.is_staff:
        return redirect(url_for('events'))
    seminar = system.get_event(seminarName)
    session = system.get_session(seminar, sessionName)
    previousSpeaker = session.speaker.name
    if request.method == 'POST':
        try:
            system.edit_session(current_user, seminar, session, request.form)
        except EditSessionError as e:
            return render_template('create_session.html', message=e.message, edit=True, seminarName=seminarName, sessionName=sessionName, session=session)
        if previousSpeaker != current_user.name and session.speaker.name == current_user.name:
            flash("Nominated speaker not registered; defaulted to creator. All other changes successfully edited")
        else:
            flash("Session successfully edited")
        return redirect(url_for('display_event', eventName=seminarName))
    return render_template('create_session.html', edit=True, seminarName=seminarName, session=session)

@app.route('/register/<eventName>/<sessionName>', methods = ['GET','POST'])
@login_required
def session_registration(eventName, sessionName):
    seminar = system.get_event(eventName)

    fee = 0
    #need to make it fee only applies if first time registering seminar
    if current_user.is_guest and not seminar.is_registered(current_user) and not seminar.is_speaker(current_user):
        if date.today() <= seminar.get_earlyBirdDate(seminar):
            fee = seminar.fee/2
        else:
            fee = seminar.fee
    try:
        system.register_session(current_user, seminar, sessionName)
    except SessionRegisterError as e:
        flash(e.message)
        return redirect(url_for('display_event', eventName=eventName))
    if current_user.is_guest:
        flash("Registration successful! Total fee charged = $" + fee.__str__())
    else:
        flash("Registration successful!")
    return redirect(url_for('display_event', eventName=eventName))

@app.route('/close_event/<eventName>', methods = ['POST'])
@login_required
def close_event(eventName):
    if not current_user.is_staff:
        return redirect(url_for('events'))
    try:
        system.close_event(eventName, current_user)
    except CloseEventError as e:
        flash(e.message)
        return redirect(url_for('display_event', eventName=eventName))
    flash(eventName + " has been closed")
    return redirect(url_for('display_event', eventName=eventName))

@app.route('/cancel_event/<eventName>', methods = ['POST'])
@login_required
def cancel_event(eventName):
    if not current_user.is_staff:
        return redirect(url_for('events'))
    try:
        system.cancel_event(eventName, current_user)
    except CancelEventError as e:
        flash(e.message)
        return redirect(url_for('display_event', eventName=eventName))
    flash(eventName + " has been cancelled")
    return redirect(url_for('display_event', eventName=eventName))

@app.route('/register/<eventName>', methods=['POST'])
@login_required
def registration(eventName):
    event = system.get_event(eventName)
    if (isinstance(event, Seminar)):
       return redirect(url_for('select_session_registration', seminarName=eventName))
    try:
        system.register_event(current_user, event)
    except RegisterEventError as e:
        flash(e.message)
        return

    if current_user.is_guest:
        if date.today() <= event.get_earlyBirdDate(event):
            flash("Registration successful! Total fee charged = $" + (event.fee/2).__str__())
        else:
            flash("Registration successful! Total fee charged = $" + event.fee.__str__())
    else:
        flash("Registration successful!")
    return redirect(url_for('display_event', eventName=eventName))

@app.route('/deregister/<eventName>', methods=['POST'])
@login_required
def deregistration(eventName):
    state = system.deregister_event(current_user, system.get_event(eventName))
    # print(state)
    return render_template('deregister.html', event = eventName, message = state)

@app.route('/close_notification/<notification>', methods=['GET'])
@login_required
def close_notification(notification):
    system.close_notification(current_user, notification)
    return redirect(url_for('dashboard'))
