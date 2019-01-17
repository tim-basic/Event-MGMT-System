# Invalid details for creating event
class CreateEventError(Exception):
    def __init__(self, msg):
        super().__init__()
        self.message = msg


# Invalid details for editing an event
class EditEventError(Exception):
    def __init__(self, msg):
        super().__init__()
        self.message = msg


class CloseEventError(Exception):
    def __init__(self, msg):
        super().__init__()
        self.message = msg


class CancelEventError(Exception):
    def __init__(self, msg):
        super().__init__()
        self.message = msg


class CreateSessionError(Exception):
    def __init__(self, msg):
        super().__init__()
        self.message = msg


class EditSessionError(Exception):
    def __init__(self, msg):
        super().__init__()
        self.message = msg


class SessionRegisterError(Exception):
    def __init__(self, msg):
        super().__init__()
        self.message = msg


class RegisterEventError(Exception):
    def __init__(self, msg):
        super().__init__()
        self.message = msg