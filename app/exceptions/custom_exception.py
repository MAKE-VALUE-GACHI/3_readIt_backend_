class CustomException(Exception):

    def __init__(self, message=None, status_code=200, error_code=None):
        self.status_code = status_code
        self.message = message
        self.error_code = error_code
