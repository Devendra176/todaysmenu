from fastapi import HTTPException


class Error(Exception):
    default = {
        "message": None,
        "code": None
    }

    def __init__(self, message=None, code=None, **kwargs):
        self.message = message or self.default["message"]
        self.code = code or self.default["code"]
        self.context = kwargs
        super(Error, self).__init__(message)

    def __str__(self):
        return self.message


class UserNotFoundError(Error):
    message = "User Not found in DB"


class UserAlreadyExists(Error):
    default = {
        "message": "User Already Exists in the DB",
        "code": "EXISTS"
    }


class HTTPExceptionBaseError(HTTPException):
    default = {
        "status_code": None,
        "detail": None
    }

    def __init__(self, status_code=None, detail=None, headers=None):
        self.status_code = status_code or self.default['status_code']
        self.detail = detail or self.default['detail']
        super(HTTPExceptionBaseError, self).__init__(status_code=self.status_code, detail=self.detail, headers=headers)


class RestaurantNotFoundError(HTTPExceptionBaseError):
    default = {
        "status_code": 404,
        "detail": {
            "message": "Restaurant Not Found",
            "status_code": 404
        }
    }


class MenuNotFoundError(HTTPExceptionBaseError):
    default = {
        "status_code": 404,
        "detail": {
            "message": "Menu Not Found",
            "status_code": 404
        }
    }


class MenuItemNotFoundError(HTTPExceptionBaseError):
    default = {
        "status_code": 404,
        "detail": {
            "message": "Menu Item Not Found",
            "status_code": 404
        }
    }


class ExceptionHandling(HTTPExceptionBaseError):
    default = {
        "status_code": 500,
        "detail": None
    }
