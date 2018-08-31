class LogikonToken:
    def __init__(self, _value, _type, _position, _length):
        self.value = _value
        self.type = _type
        self.position = _position
        self.length = _length

    def toString(self):
        return "Value: " + self.value + ", Type: " + self.type + ", Position: " + str(self.position) + ", Length: " + str(self.length)
