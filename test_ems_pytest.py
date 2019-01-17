import pytest
from src.UserExceptions import *
from src.system import init_system
from src.EventManager import EventManager
from src.User import Staff, Student, Guest

def test_create_seminar_valid():
    system = EventManager()
    staff_user = Staff("3466724", "123", "staffName", "a@m.com")
    speaker = Guest("123abc", "Ash Getrichquick", "ash.g@mail.com")
    system.add_user(staff_user)
    system.add_user(speaker)
    system.create_seminar(staff_user, {'eventName': "All About Cryptocurrency", 
                                        'venue': "John Clancy Auditorium", 
                                        'description': "Overview and insight into cryptocurrency", 
                                        'numAttendees': "100", 
                                        'startDate': "2018-06-01", 
                                        'endDate': "2018-06-10", 
                                        'deDate': "2018-05-30",
                                        'speaker': "ash.g@mail.com",
                                        'sessionName': "What is Cryptocurrency all about?", 
                                        'maxCapacity': "50", 
                                        'fee': "10",
                                        'earlyBirdDate': "2018-04-20"})
    event = system.get_event("All About Cryptocurrency")
    assert event.creator.name == staff_user.name
    assert event.sessions[0].speaker.name == speaker.name

def test_create_seminar_invalid_period():
    system = EventManager()
    staff_user = Staff("3466724", "123", "staffName", "a@m.com")
    system.add_user(staff_user)
    with pytest.raises(CreateEventError) as e:
        system.create_seminar(staff_user, {'eventName': "All About Cryptocurrency", 
                                            'venue': "John Clancy Auditorium", 
                                            'description': "Overview and insight into cryptocurrency", 
                                            'numAttendees': "100", 
                                            'startDate': "2018-06-01", 
                                            'endDate': "2018-05-10", 
                                            'deDate': "2018-05-30",
                                            'speaker': "ash.g@mail.com",
                                            'sessionName': "What is Cryptocurrency all about?", 
                                            'maxCapacity': "50", 
                                            'fee': "10",
                                            'earlyBirdDate': "2018-04-20"})

def test_create_seminar_invalid_date_input():
    system = EventManager()
    staff_user = Staff("3466724", "123", "staffName", "a@m.com")
    system.add_user(staff_user)
    with pytest.raises(CreateEventError) as e:
        system.create_seminar(staff_user, {'eventName': "All About Cryptocurrency", 
                                            'venue': "John Clancy Auditorium", 
                                            'description': "Overview and insight into cryptocurrency", 
                                            'numAttendees': "100", 
                                            'startDate': "randomtext", 
                                            'endDate': "thisissupposed", 
                                            'deDate': "tobeadate",
                                            'speaker': "ash.g@mail.com",
                                            'sessionName': "What is Cryptocurrency all about?", 
                                            'maxCapacity': "50", 
                                            'fee': "10",
                                            'earlyBirdDate': "2018-04-20"})

def test_create_seminar_guest_speaker_unregistered():
    system = EventManager()
    staff_user = Staff("3466724", "123", "staffName", "a@m.com")
    system.add_user(staff_user)
    system.create_seminar(staff_user, {'eventName': "All About Cryptocurrency", 
                                        'venue': "John Clancy Auditorium", 
                                        'description': "Overview and insight into cryptocurrency", 
                                        'numAttendees': "100", 
                                        'startDate': "2018-06-01", 
                                        'endDate': "2018-06-10", 
                                        'deDate': "2018-05-30",
                                        'speaker': "",
                                        'sessionName': "What is Cryptocurrency all about?", 
                                        'maxCapacity': "50", 
                                        'fee': "10",
                                        'earlyBirdDate': "2018-04-20"})
    event = system.get_event("All About Cryptocurrency")
    assert event.sessions[0].speaker.name == staff_user.name

# def test_register_for_seminar_as_guest():
# def test_register_for_seminar_as_guest_speaker():
# def test_register_for_seminar_as_guest_speaker_of_session_in_seminar():
# def test_register_for_seminar_as_creator():
#     with pytest.raises(RegisterEventError) as e:
# def test_register_for_seminar_as_user():