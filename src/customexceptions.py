class OutOfRange(Exception):
    def __init__(self, message='The value is out of range'):
        self.message = message
        super().__init__(self.message)


class InvalidSign(Exception):
    def __init__(self, sign, message='The sign user provided is invalid'):
        self.message = message
        self.sign = sign
        super().__init__(self.message)


class InvalidArgument(Exception):
    def __init__(self, message='The argument/s passed is/are invalid'):
        self.message = message
        super().__init__(self.message)
