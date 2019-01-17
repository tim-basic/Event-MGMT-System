from .Event import Course, Seminar
from .Session import Session
from .Status import Open, Closed, Cancelled
from datetime import datetime, date
from operator import attrgetter
import re
from .UserExceptions import *
from .Notification import Notification

class EventManager:
    def __init__(self):
            self._available_courses = []
            self._available_seminars = []
            self._unavailable_events = []
            self._users = []

    def find_user(self, ID):
        for user in self._users:
            if user.ID.lower() == ID.lower():
                return user
        return None

    def add_user(self, user):
        self._users.append(user)

    def get_users(self):
        return self._users

    def get_user_by_id(self, user_id):
        """ For Flask-Login use"""
        for user in self._users:
            if user.get_id() == user_id:
                return user
        return None

    def validate_login(self, ID, password):
        for user in self._users:
            if user.ID == ID and user.validate_password(password):
                return user
        return None

    def send_notification(self, users, event, notification):
        for user in users:
            user.new_notification(Notification(event, notification))

    def close_notification(self, curr_user, notification):
        user = self.find_user(curr_user.ID)
        user.close_notification(notification)

    def cancel_event(self, eventName, curr_user):
        user = self.find_user(curr_user.ID)
        event = self.get_event(eventName)
        if not event.is_creator(user):
            raise CancelEventError("Error: You are not the creator of this event!")
        if isinstance(self.get_event(eventName).status, Closed):
            raise CancelEventError("Error: Event has been closed. You can't cancel a closed event!")
        if isinstance(self.get_event(eventName).status, Cancelled):
            raise CancelEventError("Error: Event has already been cancelled!")
        # cancel event
        event.status = Cancelled()
        if isinstance(event, Course):
            self._available_courses.remove(event)
        else:
            self._available_seminars.remove(event)
        self._unavailable_events.append(event)
        user.open_events.remove(event)
        user.cancelled_events.append(event)
        # remove event from all users' list.....
        for attendee in event.attendees:
            attendee.registered_events.remove(event)
        self.send_notification(event.attendees, event, event.name + " has been cancelled")

    def close_event(self, eventName, curr_user):
        user = self.find_user(curr_user.ID)
        event = self.get_event(eventName)
        if isinstance(self.get_event(eventName).status, Closed):
            raise CloseEventError("Error: This event is already closed!")
        if isinstance(self.get_event(eventName).status, Cancelled):
            raise CloseEventError("Error: This event is cancelled!")
        if not event.is_creator(user):
            raise CloseEventError("Error: You are not the creator of this event!")
        if event.endDate > date.today():
            raise CloseEventError("Error: This event is still active!")

        event.status = Closed()
        if isinstance(event, Course):
            self._available_courses.remove(event)
        else:
            self._available_seminars.remove(event)
        self._unavailable_events.append(event)
        user.open_events.remove(event)
        user.closed_events.append(event)
        self.send_notification(event.attendees, event, event.name + " has been closed")

    def create_course(self, creator, form):
        user = self.find_user(creator.ID)
        if not self.validate_course_name(form['eventName']):
            raise CreateEventError("An event with this name already exists")

        date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
        if not date_pattern.search(form['startDate']):
            raise CreateEventError("Specify a valid start date")

        if not date_pattern.search(form['endDate']):
            raise CreateEventError("Specify a valid end date")

        if not date_pattern.search(form['deDate']):
            raise CreateEventError("Specify a valid deregisteration date")

        if not date_pattern.search(form['earlyBirdDate']):
            raise CreateEventError("Specify a valid early bird registration date")

        if not self.validate_date(datetime.strptime(form['deDate'],'%Y-%m-%d').date(), 
                        datetime.strptime(form['startDate'],'%Y-%m-%d').date(), 
                        datetime.strptime(form['endDate'],'%Y-%m-%d').date()):
            raise CreateEventError("Start and deregistration dates must be before end date")

        course = Course(form['eventName'], 
                        user, 
                        form['venue'], 
                        form['description'], 
                        int(form['numAttendees']), 
                        datetime.strptime(form['deDate'],'%Y-%m-%d').date(), 
                        datetime.strptime(form['startDate'],'%Y-%m-%d').date(), 
                        datetime.strptime(form['endDate'],'%Y-%m-%d').date(),
                        float(form['fee']), 
                        datetime.strptime(form['earlyBirdDate'],'%Y-%m-%d').date())
        self._available_courses.append(course)
        user.open_events.append(course)  

    def create_seminar(self, creator, form):
        user = self.find_user(creator.ID)
        if not self.validate_seminar_name(form['eventName']):
            raise CreateEventError("An event with this name already exists")

        date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
        if not date_pattern.search(form['startDate']):
            raise CreateEventError("Specify a valid start date")

        if not date_pattern.search(form['endDate']):
            raise CreateEventError("Specify a valid end date")

        if not date_pattern.search(form['deDate']):
            raise CreateEventError("Specify a valid deregisteration date")

        if not date_pattern.search(form['earlyBirdDate']):
            raise CreateEventError("Specify a valid early bird registration date")

        if not self.validate_date(datetime.strptime(form['deDate'],'%Y-%m-%d').date(), 
                        datetime.strptime(form['startDate'],'%Y-%m-%d').date(), 
                        datetime.strptime(form['endDate'],'%Y-%m-%d').date()):
            raise CreateEventError("Start and deregistration dates must be before end date")

        if (self.find_user(form['speaker'])):
            speaker = self.find_user(form['speaker'])
        else:
            speaker = user

        session = Session(speaker, form['sessionName'], int(form['maxCapacity']))
        seminar = Seminar(form['eventName'], 
                        user, 
                        form['venue'], 
                        form['description'], 
                        int(form['numAttendees']), 
                        datetime.strptime(form['deDate'],'%Y-%m-%d').date(), 
                        datetime.strptime(form['startDate'],'%Y-%m-%d').date(), 
                        datetime.strptime(form['endDate'],'%Y-%m-%d').date(),
                        session,
                        float(form['fee']), 
                        datetime.strptime(form['earlyBirdDate'],'%Y-%m-%d').date())
        self._available_seminars.append(seminar)   
        user.open_events.append(seminar)
        
    def edit_event(self, user, event, form):
        if isinstance(event, Course):
            self._available_courses.remove(event)
            if not self.validate_course_name(form['eventName']):
                self._available_courses.append(event)
                raise EditEventError("An event with this name already exists")
            self._available_courses.append(event)
        else:
            self._available_seminars.remove(event)
            if not self.validate_seminar_name(form['eventName']):
                self._available_seminars.append(event)
                raise EditEventError("An event with this name already exists")
            self._available_seminars.append(event)

        date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
        if not date_pattern.search(form['startDate']):
            raise EditEventError("Specify a valid start date")

        if not date_pattern.search(form['endDate']):
            raise EditEventError("Specify a valid end date")

        if not date_pattern.search(form['deDate']):
            raise EditEventError("Specify a valid deregisteration date")

        if not date_pattern.search(form['earlyBirdDate']):
            raise EditEventError("Specify a valid early bird registration date")

        if not self.validate_date(datetime.strptime(form['deDate'],'%Y-%m-%d').date(), 
                        datetime.strptime(form['startDate'],'%Y-%m-%d').date(), 
                        datetime.strptime(form['endDate'],'%Y-%m-%d').date()):
            raise EditEventError("Start and deregistration date must be before end date")

        notification = event.name + " has updated its "
        if not event.description == form['description']:
            notification = notification + "description, "
        if not event.maxAttendees == int(form['numAttendees']):
            notification = notification + "maximum number of attendees, "
        if not event.venue == form['venue']:
            notification = notification + "venue, "
        if not event.deregisterPeriod == datetime.strptime(form['deDate'],'%Y-%m-%d').date():
            notification = notification + "deregistration period, "
        if not event.startDate == datetime.strptime(form['startDate'], '%Y-%m-%d').date():
            notification = notification + "starting date, "
        if not event.endDate == datetime.strptime(form['endDate'], '%Y-%m-%d').date():
            notification = notification + "ending date, "
        if not event.fee == float(form['fee']):
            notification = notification + "fee, "
        if not event.name == form['eventName']:
            notification = notification + "name to " + form['eventName'] + ", "

        r = notification[:-2].rfind(",")
        if r == -1:
            notification_formatted = notification[:-2]
        else:
            notification_formatted = notification[:r] + " and" + notification[r+1:-2]
        if not notification_formatted == event.name + " has updated it":
            self.send_notification(event.attendees, event, notification_formatted)

        event.name = form['eventName']
        event.description = form['description']
        event.maxAttendees = int(form['numAttendees'])
        event.venue = form['venue']
        event.deregisterPeriod = datetime.strptime(form['deDate'],'%Y-%m-%d').date()
        event.startDate = datetime.strptime(form['startDate'], '%Y-%m-%d').date()
        event.endDate = datetime.strptime(form['endDate'], '%Y-%m-%d').date()
        event.fee = float(form['fee'])
        event.earlyBirdDate = datetime.strptime(form['earlyBirdDate'], '%Y-%m-%d').date()

    def register_event(self, curr_user, event):
        user = self.find_user(curr_user.ID)
        if event.is_creator(user):
            raise RegisterEventError("Registration Failed: Cannot register as the event creator")
            # return some message due to same creator

        # case for user already registered
        if event in user.registered_events:
            raise RegisterEventError("Registration Failed: You are already registered for this event")

        # check that max attendees has NOT been exceeded                
        if event.maxAttendees <= len(event.attendees):
            raise RegisterEventError("Registration Failed: Event capacity exceeded")

        event.attendees.append(user)
        user.registered_events.append(event)
        if isinstance(event, Course) and user.is_guest:
            if date.today() <= event.get_earlyBirdDate(event):
                user.add_fee(event.fee/2)
            else:
                user.add_fee(event.fee)


    def register_session(self, curr_user, seminar, sessionName):
        user = self.find_user(curr_user.ID)
        session = self.get_session(seminar, sessionName)
        if user in session.attendees:
            raise SessionRegisterError("Error: You are already registered in that session")

        if seminar.is_creator(user):
            raise SessionRegisterError("Error: Cannot register as the creator of the event")

        if user.ID == session.speaker.ID:
            raise SessionRegisterError("Error: You are the speaker of this event")

        if session.maxCapacity <= len(session.attendees):
            raise SessionRegisterError("Error: Session is full")

        if user.is_guest and not seminar.is_registered(user) and not seminar.is_speaker(user):
            if date.today() <= seminar.get_earlyBirdDate(seminar):
                user.add_fee(seminar.fee/2)
            else:
                user.add_fee(seminar.fee)
                
        if not seminar.is_registered(user):
            try:
                self.register_event(user, seminar)
            except RegisterEventError as e:
                raise SessionRegisterError(e.message)
        session.attendees.append(user)


    def deregister_event(self,curr_user,event):
        if not event.is_registered(curr_user):
            return "You are not registered in"
            

        if (date.today() > event._deregisterPeriod):
            state = "Deregister Period expired: Deregistration Unsuccessful for"
        else:
            self.deregister_sessions(curr_user,event)
            user = self.find_user(curr_user.ID)
            user.registered_events.remove(event)
            event.attendees.remove(user)
            state = "Deregistration Successful for"

        return state

    def deregister_sessions(self,curr_user,semminar):
        if (isinstance(semminar, Seminar)):
            user = self.find_user(curr_user.ID)
            for session in semminar.sessions:
                if user in session._attendees:
                    session._attendees.remove(user)
        pass


    def add_session(self, curr_user, seminarName, form):
        user = self.find_user(curr_user.ID)
        if (self.find_user(form['speaker'])):
            speaker = self.find_user(form['speaker'])
        else:
            speaker = user
        seminar = self.get_event(seminarName)
        if not self.validate_session_name(seminar, form['sessionName']):
            raise CreateSessionError("Session name already exists")

        session = Session(speaker, form['sessionName'], int(form['maxCapacity']))
        seminar.sessions.append(session)

    def edit_session(self, curr_user, seminar, session, form):
        user = self.find_user(curr_user.ID)
        if (self.find_user(form['speaker'])):
            speaker = self.find_user(form['speaker'])
        else:
            speaker = user

        seminar.sessions.remove(session)
        if not self.validate_session_name(seminar, form['sessionName']):
            seminar.sessions.append(session)
            raise EditSessionError("Session name already exists for this seminar")

        seminar.sessions.append(session)
        session.title = form['sessionName']
        session.speaker = speaker
        session.maxCapacity = form['maxCapacity']

    def remove_session(self, seminar, session):
        seminar.sessions.remove(session)
    
    def validate_date(self, deregisterPeriod, startDate, endDate):
        if (endDate < startDate or endDate < deregisterPeriod):
            return False
        return True

    def validate_course_name(self, eventName):
        for event in self.available_all:
            if event.name == eventName:
                return False
        return True

    def validate_seminar_name(self, eventName):
        for event in self.available_all:
            if event.name == eventName:
                return False
        return True

    def validate_session_name(self, seminar, title):
        for session in seminar.sessions:
            if session.title == title:
                return False
        return True

    def get_event(self, eventName):
        for event in self.all_events:
            if eventName == event.name:
                return event

    def get_session(self, seminar, sessionName):
        for session in seminar.sessions:
            if sessionName == session.title:
                return session

    def get_staff_dashboard(self, curr_user):
        user = self.find_user(curr_user.ID)
        (currentRegisteredEvents, pastRegisteredEvents, notifications) = self.get_student_dashboard(curr_user)
        openEvents = sorted(user.open_events, key=attrgetter('startDate'))
        closedEvents = sorted(user.closed_events, key=attrgetter('startDate'))
        cancelledEvents = sorted(user.cancelled_events, key=attrgetter('startDate'))
        return (currentRegisteredEvents, pastRegisteredEvents, openEvents, closedEvents, cancelledEvents, notifications)

    def get_student_dashboard(self, curr_user):
        user = self.find_user(curr_user.ID)
        tempEvents = user.registered_events
        currentRegisteredEvents = []
        pastRegisteredEvents = []
        for event in tempEvents:
            if isinstance(event.status, Closed):
                pastRegisteredEvents.append(event)
            elif isinstance(event.status, Open):
                currentRegisteredEvents.append(event)
        return (sorted(currentRegisteredEvents, key=attrgetter('startDate')), sorted(pastRegisteredEvents, key=attrgetter('startDate')), user.notifications)

    @property
    def available_courses(self):
        return sorted(self._available_courses, key=attrgetter('startDate'))

    @property
    def available_seminars(self):
        return sorted(self._available_seminars, key=attrgetter('startDate'))

    @property
    def available_all(self):
        return sorted(self._available_courses + self._available_seminars, key=attrgetter('startDate'))

    @property
    def all_events(self):
        return self._available_courses + self._available_seminars + self._unavailable_events

    def search_event(self):
        pass
