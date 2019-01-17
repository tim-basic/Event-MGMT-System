from abc import ABC
from .Session import Session
from .Status import Closed, Open, Cancelled
from datetime import datetime

class Event(ABC):
    def __init__(self, name, creator, venue, description, maxAttendees, deregisterPeriod, startDate, endDate, fee, earlyBirdDate):
        self._attendees = []
        self._name = name
        self._creator = creator
        self._venue = venue
        self._description = description
        self._maxAttendees = maxAttendees
        self._deregisterPeriod = deregisterPeriod
        self._startDate = startDate
        self._endDate = endDate 
        self._status = Open()
        self._fee = fee
        self._earlyBirdDate = earlyBirdDate

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def creator(self):
        return self._creator

    @property
    def venue(self):
        return self._venue
    @venue.setter
    def venue(self, value):
        self._venue = value
    
    @property
    def description(self):
        return self._description
    @description.setter
    def description(self, value):
        self._description = value

    @property
    def maxAttendees(self):
        return self._maxAttendees
    @maxAttendees.setter
    def maxAttendees(self, value):
        self._maxAttendees = value

    @property
    def deregisterPeriod(self):
        return self._deregisterPeriod
    @deregisterPeriod.setter
    def deregisterPeriod(self, value):
        self._deregisterPeriod = value

    def deregisterPeriodStr(self):
        return self._deregisterPeriod.strftime('%d/%m/%Y')

    @property
    def startDate(self):
        return self._startDate
    @startDate.setter
    def startDate(self, value):
        self._startDate = value

    def startDateStr(self):
        return self._startDate.strftime('%d/%m/%Y')

    @property
    def endDate(self):
        return self._endDate
    @endDate.setter
    def endDate(self, value):
        self._endDate = value

    def endDateStr(self):
        return self._endDate.strftime('%d/%m/%Y')

    @property    
    def status(self):
        return self._status
    @status.setter
    def status(self, value):
        self._status = value

    @property
    def attendees(self):
        return self._attendees
        
    def attendee_names(self):
        attendees = []
        for attendee in self._attendees:
            attendees.append(attendee.name)
        return attendees

    @property
    def fee(self):
        return self._fee
    @fee.setter
    def fee(self, value):
        self._fee = value

    @property
    def earlyBirdDate(self):
        return self._earlyBirdDate
    @earlyBirdDate.setter
    def earlyBirdDate(self, value):
        self._earlyBirdDate = value
        
    def earlyBirdDateStr(self):
        return self._earlyBirdDate.strftime('%d/%m/%Y')

    def get_earlyBirdDate(self, event):
        return self._earlyBirdDate

    def is_creator(self, user):
        return user.ID is self._creator.ID

    def is_registered(self, user):
        for attendee in self._attendees:
            if user.ID == attendee.ID:
                return True
        return False


class Course(Event):
    def __init__(self, name, creator, venue, description, maxAttendees, deregisterPeriod, startDate, endDate, fee, earlyBirdDate):
        super().__init__(name, creator, venue, description, maxAttendees, deregisterPeriod, startDate, endDate, fee, earlyBirdDate)


class Seminar(Event):
    def __init__(self, name, creator, venue, description, maxAttendees, deregisterPeriod, startDate, endDate, session, fee, earlyBirdDate):
        super().__init__(name, creator, venue, description, maxAttendees, deregisterPeriod, startDate, endDate, fee, earlyBirdDate)
        self._sessions = [session]

    @property
    def sessions(self):
        return self._sessions

    def is_speaker(self, user):
        for session in self._sessions:
            if session.speaker.ID == user.ID:
                return True
        return False