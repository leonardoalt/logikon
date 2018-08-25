from logikon_token import LogikonToken

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
        if c in self._separators:
            token = c
        else:
            token = self.next_token()

        t_type = ""
        if self.isKeyword(token):
            t_type = self._keywords[token]
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
        while needle < len(self.code) and self.code[needle] not in (self._separators + self._blanks):
            needle += 1
        return self.code[self.needle : needle]

    def consume_blanks(self):
        while self.needle < len(self.code) and self.code[self.needle] in self._blanks:
            self.needle += 1

    _blanks = [' ', '\t', '\n']
    _separators = ['(', ')', '[', ']', ',', '.']

    _keywords = {
        "declare-var" : "state_var_declaration",
        "declare-pred": "predicate_declaration",
        "public" : "visibility_specifier",
        "UInt" : "type",
        "Array" : "type",
        "sum" : "unary_operator",
        "prove" : "unary_operator",
        "not" : "unary_operator",
        "syncUInt" : "binary_operator",
        "select" : "binary_operator",
        "store" : "ternary_operator",
        "syncArray" : "ternary_operator",
        "ite" : "ternary_operator",
        "=" : "binary_operator",
        "!=" : "binary_operator",
        "<" : "binary_operator",
        "<=" : "binary_operator",
        ">" : "binary_operator",
        ">=" : "binary_operator",
        "and" : "binary_operator",
        "or" : "binary_operator",
        "+" : "binary_operator",
        "-" : "binary_operator",
        "*" : "binary_operator",
        "/" : "binary_operator",
        "(" : "left_parent",
        ")" : "right_parent",
        "[" : "left_brack",
        "]" : "right_brack",
        ":-" : "entails",
        "." : "period",
        "," : "comma"
    }

    def isKeyword(self, word):
        return word in self._keywords

