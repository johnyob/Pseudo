def readFile(path):
    try:
        with open(path, "r") as file:
            return file.read()
    except:
        print(
            "{Error: Failed to load file. File doesn't exist or invalid file path, "
            + "Message: Please check arguments or import strings.}"
        )
        return ""


class Stack:
    def __init__(self):
        self._stack = []

    def isEmpty(self):
        return len(self._stack) == 0

    def peek(self):
        return self._stack[-1] if not self.isEmpty() else None

    def push(self, element):
        self._stack.append(element)

    def pop(self):
        return self._stack.pop() if not self.isEmpty() else None

    def get(self, index):
        return self._stack[index] if index < len(self._stack) and index >= 0 else None

    def __len__(self):
        return len(self._stack)
