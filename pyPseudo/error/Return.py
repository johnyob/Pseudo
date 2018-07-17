class Return(Exception):
    def __init__(self, value):
        self._value = value

    def getValue(self):
        return self._value