from enum import Enum, auto


class TokenType(Enum):
    NUMBER = auto()
    MINUS = auto()
    LEFT_PAREN = auto()
    PLUS = auto()
    RIGHT_PAREN = auto
    STAR = auto()
    SLASH = auto()
    EOF = auto()


class Token:
    """ Token class"""
    def __init__(self, token_type, lexeme, literal, line):
        self.type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return "{0} {1} {2}".format(self.type, self.lexeme, self.literal)


class BytecodeInst(Enum):
    ADD: 1
    SUB: 2
    MUL: 3
    DIV: 4


class BinaryExpr:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class Literal:
    def __init__(self, value):
        self.value = value


class Scanner:
    def __init__(self, source):
        self.tokens = []
        self._start = 0
        self._current = 0
        self._line = 1
        self._source = source

    def scan_tokens(self):
        while not self._at_end():
            self._start = self._current
            self._scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self._source))
        return self.tokens

    def _scan_token(self):
        c = self._advance()
        if c == '-':
            self._add_token(TokenType.MINUS)
        elif c == '+':
            self._add_token(TokenType.PLUS)
        elif c == '(':
            self._add_token(TokenType.LEFT_PAREN)
        elif c == ')':
            self._add_token(TokenType.RIGHT_PAREN)
        elif c.isdigit():
            self._number()
        elif c == '*':
            self._add_token(TokenType.STAR)
        elif c == '/':
            self._add_token(TokenType.SLASH)
        elif c in {' ', '\n', '\t'}:
            pass
        else:
            print("{} is not recognized".format(c))

    def _add_token(self, token_type, literal=None):
        text = self._source[self._start:self._current]
        self.tokens.append(Token(token_type, text, literal, self._line))

    def _advance(self):
        self._current += 1
        return self._source[self._current - 1]

    def _at_end(self):
        return self._current >= len(self._source)

    def _number(self):
        while self._peek().isdigit():
            self._advance()
        if self._peek() == '.' and self._peek_next().isdigit():
            self._advance()
            while self._peek().isdigit():
                self._advance()
        self._add_token(TokenType.NUMBER, float(self._source[self._start:self._current]))

    def _peek_next(self):
        if self._current + 1 > len(self._source):
            return '/0'
        return self._source[self._current + 1]

    def _peek(self):
        if self._at_end():
            return '\0'
        else:
            return self._source[self._current]


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self._current = 0

    def parse(self):
        return self._addition()

    def _addition(self):
        """ addition or subtraction """
        # check for higher order precedence
        expr = self._multiplication()
        while self._match(types=(TokenType.MINUS, TokenType.PLUS)):
            operator = self._previous()
            right = self._multiplication()
            expr = BinaryExpr(expr, operator, right)
        return expr

    def _multiplication(self):
        """ multiplication or division """
        expr = self._primary()
        while self._match(types=[TokenType.STAR, TokenType.SLASH]):
            operator = self._previous()
            right = self._primary()
            expr = BinaryExpr(expr, operator, right)
        return expr

    def _primary(self):
        if self._match(types=[TokenType.NUMBER]):
            return Literal(self._previous().literal)

        if self._match(types=[TokenType.LEFT_PAREN]):
            expr = self.parse()
            self._consume(TokenType.RIGHT_PAREN, 'Missing closing paren')
            return expr
        raise Exception("unexpected token")

    def _consume(self, token_type, error_message):
        if not self._check(token_type):
            raise Exception(error_message)
        self._advance()

    def _match(self, types):
        for t in types:
            if self._check(t):
                self._advance()
                return True
        return False

    def _previous(self):
        return self.tokens[self._current - 1]

    def _advance(self):
        self._current += 1

    def _peek(self):
        return self.tokens[self._current]

    def _at_end(self):
        return self._peek().type == TokenType.EOF

    def _check(self, token_type):
        if self._at_end():
            return False
        return self._peek().type == token_type


OP_FOR_TOKEN = {
    TokenType.MINUS: lambda x, y: x - y,
    TokenType.PLUS: lambda x, y: x + y,
    TokenType.STAR: lambda x, y: x * y,
    TokenType.SLASH: lambda x, y: x / y
}


def eval(ast):
    """ recursively eval ast """
    if type(ast) == Literal:
        return ast.value
    elif type(ast) == BinaryExpr:
        return OP_FOR_TOKEN[ast.operator.type](eval(ast.left), eval(ast.right))
    else:
        raise Exception('Invalid AST node type')

what_to_execute = {
    "instructions": [("LOAD_VALUE", 0),  # the first number
                     ("LOAD_VALUE", 1),  # the second number
                     ("ADD_TWO_VALUES", None),
                     ("PRINT_ANSWER", None)],
    "numbers": [7, 5] }

class Interpreter:
    def __init__(self):
        self.stack = []

    def LOAD_VALUE(self, number):
        self.stack.append(number)

    def PRINT_ANSWER(self):
        answer = self.stack.pop()
        print(answer)

    def ADD_TWO_VALUES(self):
        first_num = self.stack.pop()
        second_num = self.stack.pop()
        total = first_num + second_num
        self.stack.append(total)

    def run_code(self, what_to_execute):
        instructions = what_to_execute["instructions"]
        numbers = what_to_execute["numbers"]
        for each_step in instructions:
            instruction, argument = each_step
            if instruction == "LOAD_VALUE":
                number = numbers[argument]
                self.LOAD_VALUE(number)
            elif instruction == "ADD_TWO_VALUES":
                self.ADD_TWO_VALUES()
            elif instruction == "PRINT_ANSWER":
                self.PRINT_ANSWER()

if __name__ == "__main__":
    # cannot evaluate/tokenize negative numbers yet
    # line1 = "5 * (2 - (3 + 4))"
    # scanner = Scanner(line1)
    # tokens = scanner.scan_tokens()
    # ast = Parser(tokens).parse()
    # assert eval(ast) == -25.0

    interpreter = Interpreter()
    interpreter.run_code(what_to_execute)
