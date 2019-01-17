# class UserManager:
#     def __init__(self):
#         #self._staff = []
#         #self._students = []
#         self._users = []

#     def find_user(self, zID):
#         for user in self._users:
#             if user.zID == zID:
#                 return user
#         return None

#     # def add_staff(self, staff):
#     #     self._staff.append(staff)

#     # def add_student(self, student):
#     #     self._students.append(student)

#     def add_user(self, user):
#         self._users.append(user)

#     # def get_staff(self):
#     #     return self._staff

#     # def get_students(self):
#     #     return self._students

#     def get_users(self):
#         return self._users

#     def get_user_by_id(self, user_id):
#         """ For Flask-Login use"""
#         for user in self._users:
#             if user.get_id() == user_id:
#                 return user
#         return None

#     def validate_user(self, zID, password):
#         for user in self._users:
#             if user.zID == zID and user.validate_password(password):
#                 return user
#         return None