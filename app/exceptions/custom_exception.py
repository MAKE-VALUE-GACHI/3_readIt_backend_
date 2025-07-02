class CustomException(Exception):

    def __init__(self, message=None, status_code=200):
        self.status_code = status_code
        self.message = message
