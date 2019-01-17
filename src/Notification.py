class Notification:
    def __init__(self, event, notification):
        self._event = event
        self._notification = notification
       
    @property
    def event(self):
        return self._event

    @property
    def notification(self):
        return self._notification