from pyPseudo.error.RuntimeError import RuntimeError

class PseudoList:
    def __init__(self, values):
        self._values = values

    def getValues(self):
        return self._values

    def __len__(self):
        return len(self._values)

    def index(self, brackets, indices):
        index = indices.pop(0)

        self._checkIndex(brackets, index)

        value = self._values[int(index)]
        return value.index(brackets, indices) if len(indices) > 0 else value

    def set(self, brackets, indices, value):
        index = indices.pop(0)
        self._checkIndex(brackets, index)

        if len(indices) > 0:
            self._values[int(index)].set(brackets, indices, value)
        else:
            self._values[int(index)] = value


    def _checkIndex(self, brackets, index):
        if not isinstance(index, float) or not index == int(index):
            raise RuntimeError(brackets, "Index not integer '{0}'.".format(index))

        if index < 0 or index > len(self) - 1:
            raise RuntimeError(brackets, "Index not in range. length: '{0}', Index: '{1}'.".format(len(self), index))

    def __str__(self):
        return "{" + ", ".join([str(value) for value in self._values]) + "}"
