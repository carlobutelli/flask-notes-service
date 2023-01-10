class BaseError(BaseException):
    """Base Error in which all the Error of the service are base"""


class Error(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, message):
        self.message = message


class ExtensionError(BaseError):

    def __init__(self, extension):
        self.extension = extension

    def __repr__(self):
        return f'The extension {self.extension} is not supported'


class PhotoTypeError(BaseError):
    def __init__(self, photo_type):
        self.photo_type = photo_type

    def __repr__(self):
        return f"Photo type {self.photo_type} is not supported"


class ValidationError(BaseError):
    def __init__(self, message: str, fields: list = ()):
        self.message = message
        self.fields = fields

    def __repr__(self):
        return f"{self.message}, {self.fields} are not valid"


class NotFoundError(BaseError):
    def __init__(self, message:str):
        self.message = message

    def __repr__(self):
        return self.message


class DuplicatedError(BaseError):
    def __init__(self, message: str):
        self.message = message

    def __repr__(self):
        return self.message


class WrongConfiguration(Error):
    """
    Exception raised when the configuration is not valid.

    Attributes:
        message -- explanation of the error
    """


class ValidationErrorData():
    def __init__(self, field:str=None, message:str=None):
        self.field = field
        self.message = message
