class ScanError(Exception):
    def __init__(self, path, line, message):
        self._path = path
        self._line = line
        self._message = message

    def report(self):
        return "File: {0}, Line: {1},  Message: {3}.".format(self._path, self._line, self._message)
