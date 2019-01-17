from abc import ABC, abstractmethod

class Status(ABC):
    @abstractmethod
    def __str__(self):
        pass

class Closed(Status):
    def __str__(self):
        return "Closed"

class Open(Status):
    def __str__(self):
        return "Open"

class Cancelled(Status):
    def __str__(self):
        return "Cancelled"