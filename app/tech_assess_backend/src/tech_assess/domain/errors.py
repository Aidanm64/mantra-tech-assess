
class Error(Exception):
    def __init__(self, message, error_code, traceback):
        self.error_code = error_code
        self.traceback = traceback
        super().__init__(message)
