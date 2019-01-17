class Session:
    def __init__(self, speaker, title, maxCapacity):
        self._speaker = speaker
        self._title = title
        self._maxCapacity = maxCapacity
        self._attendees = []
       
    @property
    def speaker(self):
        return self._speaker
    @speaker.setter
    def speaker(self, value):
        self._speaker = value

    @property
    def title(self):
        return self._title
    @title.setter
    def title(self, value):
        self._title = value

    @property
    def maxCapacity(self):
        return self._maxCapacity
    @maxCapacity.setter
    def maxCapacity(self, value):
        self._maxCapacity = value
    
    @property
    def attendees(self):
        return self._attendees