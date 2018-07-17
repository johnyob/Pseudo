class RuntimeError(Exception):
    def __init__(self, token, message):
        self._token = token
        self._message = message

    def report(self):
        return "File: {0}, Line: {1}, Where: {2},  Message: {3}.".format(self._token.getPath(), self._token.getLine(), self._token.getLexeme(), self._message)

