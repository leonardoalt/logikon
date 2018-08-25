class LogikonToken:
    def __init__(self, _value, _type, _position):
        self.value = _value
        self.type = _type
        self.position = _position

    def toString(self):
        return "Value: " + self.value + ", Type: " + self.type + ", Position: " + str(self.position)
