from .EventManager import EventManager
from .User import Student, Staff, Guest
from .Event import Course, Seminar
from .Session import Session
import csv
from datetime import datetime, date

def init_system():
    system = EventManager()
    # with open("user.csv", newline='') as csvfile:
    #     (name, zID, email, password, role) = line.readline().split(',')
    #     if role == 'trainer':
    #         user = Staff(...)
    #         add_staff(user)
    #     else:
    #         user = Student(...)
    #         add_student(user)
    staff_user = None
    student_user = None
    with open('user.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['role'] == 'trainer':
                staff_user = Staff(row['zID'], row['password'], row['name'], row['email']) #debugging maybe?
                system.add_user(staff_user)
            else:
                student_user = Student(row['zID'], row['password'], row['name'], row['email'])
                system.add_user(student_user)

    # add some guest users/speakers...
    g1 = Guest("123abc", "Anita Guest", "a.guest@mail.com")
    g2 = Guest("123abc", "Test Guest", "test@mail.com")
    g3 = Guest("123abc", "John Smith", "john.smith@mail.com")
    system.add_user(Guest("123abc", "Jane Smith", "jane.smith@mail.com"))
    system.add_user(Guest("123abc", "Ash Getrichquick", "ash.g@mail.com"))
    system.add_user(Guest("123abc", "Peter Scamyourmoney", "peter.s@mail.com"))
    system.add_user(g1)
    system.add_user(g2)
    system.add_user(g3)
    # add some events...
    # active course
    system.create_course(staff_user, {'eventName': "Software Engineering Fundamentals - COMP1531", 
                                        'venue': "Mathews Theatre A", 
                                        'description': "This course provides an introduction to software engineering principles: basic software lifecycle concepts, modern development methodologies, conceptual modeling and how these activities relate to programming. It also introduces the basic notions of team-based project management via conducting a project to design, build and deploy a simple web-based application. It is typically taken in the semester after completing COMP1511, but could be delayed and taken later. It provides essential background for the teamwork and project management required in many later courses.", 
                                        'numAttendees': "400", 
                                        'startDate': "2018-02-01", 
                                        'endDate': "2018-06-01", 
                                        'deDate': "2018-02-21",
                                        'fee': "1000",
                                        'earlyBirdDate': "2018-01-14"})
    for user in system.get_users():
        if isinstance(user, Student):
            system.register_event(user, system.get_event("Software Engineering Fundamentals - COMP1531"))

    # active course
    system.create_course(staff_user, {'eventName': "Computer Systems Fundamentals - COMP1521", 
                                        'venue': "Colombo A", 
                                        'description': "This course provides a programmer's view on how a computer system executes programs, manipulates data and communicates. It enables students to become effective programmers in dealing with issues of performance, portability, and robustness. It is typically taken in the semester after completing COMP1511, but could be delayed and taken later. It serves as a foundation for later courses on networks, operating systems, computer architecture and compilers, where a deeper understanding of systems-level issues is required.", 
                                        'numAttendees': "150", 
                                        'startDate': "2018-02-01", 
                                        'endDate': "2018-06-01", 
                                        'deDate': "2018-02-21", 
                                        'fee': "1000",
                                        'earlyBirdDate': "2018-01-14"})
    system.register_event(student_user, system.get_event("Computer Systems Fundamentals - COMP1521"))
    system.register_event(g1, system.get_event("Computer Systems Fundamentals - COMP1521"))

    # closed course
    system.create_course(staff_user, {'eventName': "Object-Oriented Design & Programming - COMP2511", 
                                        'venue': "Colombo B", 
                                        'description': "This course aims to introduce students to the principles of object-oriented design and to fundamental techniques in object-oriented programming. It is typically taken in the second year of study, after COMP2521, to ensure an appropriate background in data structures. The knowledge gained in COMP2511 is useful in a wide range of later-year CS courses.", 
                                        'numAttendees': "50", 
                                        'startDate': "2017-08-01", 
                                        'endDate': "2017-11-01", 
                                        'deDate': "2017-08-21", 
                                        'fee': "1000",
                                        'earlyBirdDate': "2017-08-14"})
    system.register_event(student_user, system.get_event("Object-Oriented Design & Programming - COMP2511"))
    system.close_event("Object-Oriented Design & Programming - COMP2511", staff_user)

    # future course
    system.create_course(staff_user, {'eventName': "Security Engineering and Cyber Security - COMP6441", 
                                        'venue': "Scientia Theatre", 
                                        'description': "Introduction to computer security, prevention of cybercrime and cyberterror. The principles of engineering secure systems. How to think like a security engineer. Engineering secure systems. How security fails. Security analysis and design. Private and public cryptographic protocols. Introduction to information security: Confidentiality, Integrity, Authentication, Non-repudiation, hashing, signatures, bits of security. Physical security, social engineering, sniffing, intrusion detection, prevention and response, firewalls, honeypots. Overview of vulnerabilities and exploits including areas such as buffer overflow, inter overflow, heap attacks, Return-Oriented-Programming, heap attacks. Principles of risk and security. Case studies drawn from the history of hacking and from current events.", 
                                        'numAttendees': "100", 
                                        'startDate': "2018-08-01", 
                                        'endDate': "2018-11-01", 
                                        'deDate': "2018-08-21", 
                                        'fee': "1000",
                                        'earlyBirdDate': "2018-08-14"})
    for user in system.get_users():
        if user.ID == staff_user.ID:
            continue
        system.register_event(user, system.get_event("Security Engineering and Cyber Security - COMP6441"))

    # cancelled course
    system.create_course(staff_user, {'eventName': "Engineering Design in Computing - COMP2911", 
                                        'venue': "Rex Vowels", 
                                        'description': "The engineering design and use of reliable and complex systems. Object orientation and design. Problem solving design methodologies: backtrack, greedy method, divide and conquer, dynamic methods. Practical assignments, laboratory exercises, formal examination.", 
                                        'numAttendees': "50", 
                                        'startDate': "2016-02-01", 
                                        'endDate': "2016-06-01", 
                                        'deDate': "2016-02-21", 
                                        'fee': "1000",
                                        'earlyBirdDate': "2017-02-14"})
    system.register_event(student_user, system.get_event("Engineering Design in Computing - COMP2911"))
    system.cancel_event("Engineering Design in Computing - COMP2911", staff_user)

    # future seminar
    system.create_seminar(staff_user, {'eventName': "Australasian Symposium on Big Data & Analytics", 
                                        'venue': "CLB 5", 
                                        'description': "...stuff on big data and analytics...", 
                                        'numAttendees': "200", 
                                        'startDate': "2018-10-02", 
                                        'endDate': "2018-10-03", 
                                        'deDate': "2018-09-30",
                                        'speaker': "john.smith@mail.com",
                                        'sessionName': "Using Machine Learning to analyse financial data", 
                                        'maxCapacity': "100", 
                                        'fee': "10",
                                        'earlyBirdDate': "2018-09-15"})
    seminar = system.get_event("Australasian Symposium on Big Data & Analytics")
    system.add_session(staff_user, seminar.name, {'speaker': "jane.smith@mail.com", 
                                                'sessionName': "Semantic ontologies for financial data analysis", 
                                                'maxCapacity': "50"})
    system.add_session(staff_user, seminar.name, {'speaker': "", 'sessionName': "Predictive Analysis", 'maxCapacity': "50"})
    system.register_event(student_user, seminar)
    system.register_session(student_user, seminar, "Using Machine Learning to analyse financial data")
    system.register_session(student_user, seminar, "Semantic ontologies for financial data analysis")
    system.register_session(g1, seminar, "Semantic ontologies for financial data analysis")

    # future seminar
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
    seminar = system.get_event("All About Cryptocurrency")
    system.add_session(staff_user, seminar.name, {'speaker': "peter.s@mail.com", 
                                                'sessionName': "The Different Currencies; which is better?", 
                                                'maxCapacity': "50"})
    system.register_event(student_user, seminar)
    system.register_session(student_user, seminar, "What is Cryptocurrency all about?")
    system.register_session(g2, seminar, "What is Cryptocurrency all about?")
    system.register_session(student_user, seminar, "The Different Currencies; which is better?")

    # print("Staff: " + staff_user.ID)
    # print("Student: " + student_user.ID)
    return system
