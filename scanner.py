from enum import Enum, auto

class TokenType(Enum):
    NUMBER = auto()
    MINUS = auto()
    LEFT_PAREN = auto()
    PLUS = auto()
    RIGHT_PAREN = auto()
    EOF = auto()

class Token():
    def __init__(self, type, lexeme, literal, line):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return "{0} {1} {2}".format(self.type, self.lexeme, self.literal)

class Scanner:
    def __init__(self, source):
        self._source = source
        self.tokens = []
        self._start = 0
        self._current = 0
        self._line = 1
        self._error = None

    def _scan_token(self):
        c = self._advance()
        if c == '-': self._add_token(TokenType.MINUS)
        elif c == '+': self._add_token(TokenType.PLUS)
        elif c == '(': self._add_token(TokenType.LEFT_PAREN)
        elif c == ')': self._add_token(TokenType.RIGHT_PAREN)
        elif c.isdigit():
            self._number()
        else:
            self._error(self._line, "unexpected character: {}".format(c))

    def _at_end(self):
        return self._current >= len(self._source)

    def _advance(self):
        self._current += 1
        return self._source[self._current-1]

    def _add_token(self, type, literal=None):
        text = self._source[self._start:self._current]
        self.tokens.append(Token(type, text, literal, self._line))

    def _peek(self):
        if self._at_end():
            return '\0'
        else:
            return self._source[self._current]

    def _peek_next(self):
        if self._current + 1 > len(self._source):
            return '/0'
        return self._source[self._current + 1]

    def _number(self):
        while self._peek().isdigit():
            self._advance()
        if self._peek() == '.' and self._peek_next().isdigit():
            self._advance()
            while self._peek().isdigit():
                self._advance()
        self._add_token(TokenType.NUMBER, float(self._source[self._start:self._current]))

    def scan_tokens(self):
        while not self._at_end():
            self._start = self._current
            self._scan_token()

