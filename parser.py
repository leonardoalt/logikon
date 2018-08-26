from logikon_token import LogikonToken
from keywords import Keywords

class Parser:
    def parse(self, code):
        self.code = code
        self.needle = 0

        tokens = []
        while self.needle < len(self.code):
            tokens.append(self.parse_token())
        return tokens

    def parse_token(self):
        self.consume_blanks()
        if self.needle >= len(self.code):
            return LogikonToken("", "EOF", self.needle)

        c = self.current_char()
        if c in Keywords._separators:
            token = c
        else:
            token = self.next_token()

        t_type = ""
        if token in Keywords._types:
            t_type = Keywords._types[token]
        elif token.isnumeric():
            t_type = "number"
        elif token.isidentifier():
            t_type = "identifier"
        else:
            print("ParserError: Invalid token \"" + token + "\".")

        needle = self.needle
        self.needle += len(token)
        return LogikonToken(token, t_type, needle)

    def current_char(self):
        return self.code[self.needle]

    def next_token(self):
        needle = self.needle
        while needle < len(self.code) and self.code[needle] not in (Keywords._separators + Keywords._blanks):
            needle += 1
        return self.code[self.needle : needle]

    def consume_blanks(self):
        while self.needle < len(self.code) and self.code[self.needle] in Keywords._blanks:
            self.needle += 1
