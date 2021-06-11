# Instructions
# Given a mathematical expression as a string you must return the result as a number.
#
# Numbers
# Number may be both whole numbers and/or decimal numbers. The same goes for the returned result.
#
# Operators
# You need to support the following mathematical operators:
#
# Multiplication *
# Division / (as floating point division)
# Addition +
# Subtraction -
# Operators are always evaluated from left-to-right, and * and / must be evaluated before + and -.
#
# Parentheses
# You need to support multiple levels of nested parentheses, ex. (2 / (2 + 3.33) * 4) - -6
#
# Whitespace
# There may or may not be whitespace between numbers and operators.
#
# An addition to this rule is that the minus sign (-) used for negating numbers and parentheses will never be separated by whitespace. I.e all of the following are valid expressions.
#
# 1-1    // 0
# 1 -1   // 0
# 1- 1   // 0
# 1 - 1  // 0
# 1- -1  // 2
# 1 - -1 // 2
#
# 6 + -(4)   // 2
# 6 + -( -4) // 10
# And the following are invalid expressions
#
# 1 - - 1    // Invalid
# 1- - 1     // Invalid
# 6 + - (4)  // Invalid
# 6 + -(- 4) // Invalid
# Validation
# You do not need to worry about validation - you will only receive valid mathematical expressions following the above rules.
#
# Restricted APIs
# NOTE: eval and exec are disallowed in your solution.

import codewars_test as Test



import enum

class TokenType(enum.Enum):
    PLUS = "+"
    MINUS = "-"
    MUL = "*"
    DIV = "/"
    NUMBER = "number"
    LPAREN = "{"
    RPAREN = "}"
    EOF = "eof"

class Token(object):
    def __init__(self, type: TokenType, value: str):
        self.type = type
        self.value = value

    def __str__(self):
        return "Token({type}, {value})".format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

class Node(object):
    def __init__(self):
        self.type = None

class NumberNode(Node):
    def __init__(self, token):
        self.type = "Number"
        self.token = token
        self.number = token.value

class OpNode(Node):
    def __init__(self, lhs, op, rhs):
        self.type = "Op"
        self.op = op
        self.token = op
        self.lhs = lhs
        self.rhs = rhs

class UnaryOpNode(Node):
    def __init__(self, op, operand):
        self.type = "Negation"
        self.of = op
        self.operand = operand

class Solver(object):
    def __init__(self):
        pass

    def solve(self, ast):
        if ast.type == "Number":
            return float(ast.token.value)
        if ast.type == "Negation":
            operand = self.solve(ast.operand)
            return -operand
        if ast.type == "Op":
            lhs = self.solve(ast.lhs)
            rhs = self.solve(ast.rhs)
            if ast.token.type == TokenType.PLUS:
                return lhs + rhs
            if ast.token.type == TokenType.MINUS:
                return lhs - rhs
            if ast.token.type == TokenType.MUL:
                return lhs * rhs
            if ast.token.type == TokenType.DIV:
                return lhs / rhs


class Parser(object):
    """Parser accepts a list of tokens and returns an abstract syntax tree"""
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_pos = 0
        self.current_token = self.tokens[self.token_pos]

    def get_parsed_tree(self):
        """
            expr -> term ((PLUS|MINUS) term)*
            term -> factor ((MUL|DIV) factor)*
            factor -> NUMBER|-factor|LPAREN expr RPAREN
        """

        root = self.expr()
        return root

    def expr(self):
        root = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            lhs = root
            op = self.current_token

            self.__advance_token()

            rhs = self.term()

            root = OpNode(lhs, op, rhs)
        return root

    def term(self):
        root = self.factor()

        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            lhs = root
            op = self.current_token
            self.__advance_token()
            rhs = self.factor()
            root = OpNode(lhs, op, rhs)

        return root

    def factor(self):
        if self.current_token.type == TokenType.NUMBER:
            root = NumberNode(self.current_token)
            self.__advance_token()
            return root

        if self.current_token.type == TokenType.MINUS:
            op = self.current_token
            self.__advance_token()
            operand = self.factor()
            return UnaryOpNode(op, operand)

        if self.current_token.type == TokenType.LPAREN:
            self.__advance_token()
            root = self.expr()
            self.__eat_token(TokenType.RPAREN)
            return root

    def __advance_token(self):
        if self.current_token.type != TokenType.EOF:
            self.token_pos = self.token_pos + 1
            self.current_token = self.tokens[self.token_pos]

    def __eat_token(self, token_type):
        if self.current_token.type == token_type:
            self.__advance_token()
        else:
            raise Exception("Parse Exception")

class Tokenizer(object):
    """Tokenizer accepts a text expression and returns a list of tokens"""
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    """Return a list of tokens"""
    def get_tokens(self):
        tokens = []
        while self.current_char is not None:
            token = self.__get_next_token()
            tokens.append(token)

        tokens.append(Token(TokenType.EOF, ""))
        return tokens

    def __get_next_token(self):
        if self.current_char.isspace():
            self.__skip_whitespace()

        if self.current_char in "0123456789.":
            return Token(TokenType.NUMBER, self.__get_number())

        if self.current_char == '+':
            self.__advance()
            return Token(TokenType.PLUS, '+')

        if self.current_char == '-':
            self.__advance()
            return Token(TokenType.MINUS, '-')

        if self.current_char == '*':
            self.__advance()
            return Token(TokenType.MUL, '*')

        if self.current_char == '/':
            self.__advance()
            return Token(TokenType.DIV, '/')

        if self.current_char == '(':
            self.__advance()
            return Token(TokenType.LPAREN, '(')

        if self.current_char == ')':
            self.__advance()
            return Token(TokenType.RPAREN, ')')

        raise Exception("Unhandled Character - " + self.current_char)

    def __skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.__advance()

    def __get_number(self):
        result = ''
        while self.current_char is not None and self.current_char in "0123456789.":
            result += self.current_char
            self.__advance()
        return result

    def __advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]


def calc(expression):
    print("expression", expression)
    tokenizer = Tokenizer(expression)
    tokens = tokenizer.get_tokens()
    print("tokens")
    print(*tokens, sep='\n')
    parser = Parser(tokens)
    ast = parser.get_parsed_tree()
    solver = Solver()
    rtn = solver.solve(ast)
    return rtn


tests = [
    ["1 + 1", 2],
    ["8/16", 0.5],
    ["3 -(-1)", 4],
    ["2 + -2", 0],
    ["10- 2- -5", 13],
    ["(((10)))", 10],
    ["3 * 5", 15],
    ["-7 * -(6 / 3)", 14]
]

for test in tests:
    Test.assert_equals(calc(test[0]), test[1])