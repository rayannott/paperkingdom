class CustomException(Exception):
    pass


class InvalidMoveException(CustomException):
    pass


class InvalidShotException(CustomException):
    pass


class InvalidCompleteMoveException(CustomException):
    pass
