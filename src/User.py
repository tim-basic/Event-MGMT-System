from flask_login import UserMixin
from abc import ABC, abstractmethod

class User(UserMixin, ABC):
    def __init__(self, ID, password, name, email):
        self._id = ID
        #self._zID = zID
        self._password = password
        self._name = name
        self._email = email
        self._registered_events = []
        self._notifications = []

    def register_event(self, event):
        self._registered_events.append(event)

    def deregister_event(self, event):
        self._registered_events.remove(event)

    def new_notification(self, notification):
        self._notifications.append(notification)

    def close_notification(self, notification):
        for n in self._notifications:
            if n.notification == notification:
                self._notifications.remove(n)

    @property
    def ID(self):
        return self._id

    @property        
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email
    @property
    def password(self):
        return self._password

    @property
    def notifications(self):
        return self._notifications

    @property
    def registered_events(self):
        return self._registered_events

    def validate_password(self, password):
        return self._password == password

    def get_id(self):
        """Required by Flask-login"""
        return str(self._id)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @abstractmethod
    def is_staff(self):
        pass

    @abstractmethod
    def is_guest(self):
        pass


class Student(User):
    def __init__(self, ID, password, name, email):
        super().__init__(ID, password, name, email)

    @property
    def is_staff(self):
        return False

    @property
    def is_guest(self):
        return False

class Guest(User):
    def __init__(self, password, name, email):
        super().__init__(email, password, name, email)
        self._fees = 0

    @property
    def is_staff(self):
        return False

    @property
    def is_guest(self):
        return True

    @property
    def fees(self):
        return self._fees

    def add_fee(self, fee):
        self._fees = self._fees + fee


class Staff(User):
    def __init__(self, ID, password, name, email):
        super().__init__(ID, password, name, email)
        self._open_events = []
        self._closed_events = []
        self._cancelled_events = []

    def new_event(self):
        pass

    def close_event(self):
        pass

    def cancel_event(self):
        pass

    @property
    def open_events(self):
        return self._open_events

    @property
    def closed_events(self):
        return self._closed_events

    @property
    def cancelled_events(self):
        return self._cancelled_events

    @property
    def is_staff(self):
        return True

    @property
    def is_guest(self):
        return False
