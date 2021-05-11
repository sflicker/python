import enum

class TokenType(enum.Enum):
    NUM = "number"
    PLUS = "+"
    MINUS = "-"
    MUL = "*"
    DIV = "/"
    LPAREN = "("
    RPAREN = ")"
    EOF = "eof"

class Token(object):

    def __init__(self, type: TokenType, value: str):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

class Calculator(object):

    def __init__(self):
        self.tokens = []
        self.token_pos = None
        self.current_token = None


    def evaluate(self, string):
        tokenizer = Tokenizer();
        self.tokens = tokenizer.get_tokens(string)
        self.token_pos = 0
        self.current_token = self.tokens[self.token_pos]
        parse_tree = self.parse()
        result = self.solve(parse_tree)
        return result

    def solve(self, parse_tree) -> float:
        # type: (object) -> object
        if parse_tree['type'] == TokenType.NUM:
            res = float(parse_tree['value'])
            return res
        elif parse_tree['type'] == "Neg":
            child = self.solve(parse_tree['child'])
            rtn = -child
            print(rtn)
            return rtn;
        elif parse_tree['type'] in (TokenType.PLUS, TokenType.MINUS, TokenType.MUL, TokenType.DIV):
            lhs = self.solve(parse_tree['lhs'])
            rhs = self.solve(parse_tree['rhs'])
            print(lhs, parse_tree['value'], rhs)
            if parse_tree['value'] == "+":
                return lhs + rhs
            elif parse_tree['value'] == "-":
                return lhs - rhs
            elif parse_tree['value'] == "*":
                return lhs * rhs
            elif parse_tree['value'] == "/":
                return lhs / rhs

    def parse(self):

        """expr -> term ((PLUS|MINUS) term)*
       term -> factor ((MUL|DIV) factor)*
       factor -> NUMBER|-factor|LPAREN expr RPAREN
       """

        root = self.expr()
        return root


    def get_next_token(self):
        if self.current_token.type != TokenType.EOF:
            self.token_pos = self.token_pos + 1
            self.current_token = self.tokens[self.token_pos]


    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.get_next_token()
        else:
            raise Exception("Parse Error")

    def expr(self):

        root = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            lhs = root

            root = {}
            root['type'] = self.current_token.type
            root['value'] = self.current_token.value
            root['lhs'] = lhs
            self.get_next_token()

            root['rhs'] = self.term()

        return root

    def term(self):

        root = self.factor()

        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            lhs = root

            root = {}
            root['type'] = self.current_token.type
            root['value'] = self.current_token.value
            root['lhs'] = lhs

            self.get_next_token()
            root['rhs'] = self.factor()

        return root

    def factor(self):

        if self.current_token.type == TokenType.NUM:
            root = {}
            root['type'] = self.current_token.type
            root['value'] = self.current_token.value
            self.get_next_token()
            return root
        elif self.current_token.type == TokenType.MINUS:
            root = {}
            root['type'] = "Neg"
            root['value'] = self.current_token.value
            self.get_next_token()
            root['child'] = self.factor()
            return root
        elif self.current_token.type == TokenType.LPAREN:
            self.get_next_token()
            root = self.expr()
            self.eat(TokenType.RPAREN)
            return root

class Tokenizer(object):

    def __init__(self):
        self.text = None
        self.pos = None
        self.current_char = None

    def get_tokens(self, string):
        tokens = []
        self.text = string
        self.pos = 0
        self.current_char = self.text[0]

        while self.current_char is not None:
            tok = self.get_next_token()
            tokens.append(tok)

        tokens.append(Token(TokenType.EOF, ""))
        return tokens

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_number(self):
        result = ''
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        return result

    def get_next_token(self) :

        if self.current_char.isspace():
            self.skip_whitespace()

        if self.current_char.isdigit() or self.current_char == '.':
            return Token(TokenType.NUM, self.get_number())

        if self.current_char == '+':
            self.advance()
            return Token(TokenType.PLUS, '+')

        if self.current_char == '-':
            self.advance()
            return Token(TokenType.MINUS, '-')

        if self.current_char == '*':
            self.advance()
            return Token(TokenType.MUL, '*')

        if self.current_char == '/':
            self.advance()
            return Token(TokenType.DIV, '/')

        if self.current_char == '(':
            self.advance()
            return Token(TokenType.LPAREN, '(')

        if self.current_char == ')':
            self.advance()
            return Token(TokenType.RPAREN, ')')

        self.error()

assert Calculator().evaluate("1 + 1") == 2.0
assert Calculator().evaluate("-1") == -1
assert Calculator().evaluate("2*3") == 6
assert Calculator().evaluate("1 - -1") == 2
assert Calculator().evaluate("2 / 2 + 3 * 4 - 6") == 7
assert Calculator().evaluate("3 * 4 + 3 * 7 - 6") == 27
assert Calculator().evaluate("1 + 1") == 2
assert Calculator().evaluate("10") == 10
assert Calculator().evaluate("(5)") == 5
assert Calculator().evaluate("( ( ( ( 1 ) * 2 ) ) )") == 2
assert Calculator().evaluate("6 / (3 + 3) * 4 - 6") == -2
assert Calculator().evaluate("1.1 * 2.2 * 3.3") - 7.986 < 0.001
assert Calculator().evaluate("8/16") - 0.5 < 0.001
assert Calculator().evaluate("-7 * -(6 / 3)") == 14.0
assert Calculator().evaluate("36 + -7 - -11 - -31 - 61 * -26 + 89 - -18") == 1764
