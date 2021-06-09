import codewars_test as test

#### samples from test criteria

# if input == ".":
#     rtn = Any()
#     print(str(rtn))
#     return rtn
#
# if input == "a":
#     return Normal("a")
#
# if input == "a|b":
#     return Or(Normal("a"), Normal("b"))
#
# if input == "a*":
#     return ZeroOrMore(Normal("a"))
#
# if input == "(a)":
#     return Normal("a")
#
# if input == "(a)*":
#     return ZeroOrMore(Normal("a"))
#
# if input == "(a|b)*":
#     return ZeroOrMore(Or(Normal("a"), Normal("b")))

##### submission starts after this line

def parseRegExp(input):
    print(input)
    parser = Parser(input)
    try:
        rtn = parser.regex()
        print(rtn, type(rtn).__name__)
        if parser.at_eof():
            return rtn
        else:
            return ""

    except Exception:
        return ""


class Parser(object):
    """Regular Expression Parser
    grammar
    regex ::= term '|' regex
            | term
    term ::= { factor }
    factor ::= base { '*' }
    base ::= char                     # a single character not in ()*|.
            | '.'                     # any character
            | '(' regex ')'
    """

    def __init__(self, input):
        self.input = input
        self.pos = 0

    def at_eof(self):
        return self.pos == len(self.input)

    def peek(self):
        if self.pos >= len(self.input):
            raise Exception("Pos beyond input length")
        return self.input[self.pos]

    def eat(self, c):
        if self.peek() == c:
            self.pos = self.pos + 1
        else:
            raise Exception("Parse exception - expected", c, "got", self.peek())

    def next_token(self):
        c = self.peek()
        self.eat(c)
        return c

    def more(self):
        return len(self.input) > self.pos

    def regex(self):
        term = self.term()

        if self.more() and self.peek() == '|':
            self.eat('|')
#            regex = self.regex()
            term2 = self.term()
#            return Or(term, regex)
            return Or(term, term2)
        else:
            return term

    def term(self):
        # factor = BlankAST
        v = []
        while self.more() and self.peek() not in ')|':
            nextFactor = self.factor()
            #  factor = Str(factor, nextFactor)
            v.append(nextFactor)

        # return factor
        if len(v) == 0:
            return ""
        return Str(v) if len(v) > 1 else v[0]

    def factor(self):
        base = self.base()
#        while self.more() and self.peek() == '*':
        if self.more() and self.peek() == '*':
            self.eat('*')
            base = ZeroOrMore(base)

        return base

    def base(self):
        c = self.peek()
        if c == '(':
            self.eat('(')
            if self.peek() == ')':
                raise Exception("Invalid empty ()")
            r = self.regex()
            self.eat(')')
            return r
        if c not in '()|.*':
            return Normal(self.next_token())
        if c == '.':
            self.next_token()
            return Any()

        raise Exception("Parser Error - Invalid character " + c + " at pos " + self.pos)

### submission ends
######## THESE REGEX CLASSES SHOULD NOT BE INCLUDED IN THE SUBMISSION AS THEY ARE PROVIDED BY
## THE TEST
class AST(object):
    pass

class Or(AST):
    def __init__(self, operand1, operand2):
        self.operand1 = operand1
        self.operand2 = operand2

class Normal(AST):
    def __init__(self, c):
        self.c = c

    def __str__(self):
        return self.c

class Any(AST):

    def __init__(self):
        pass

    def __str__(self):
        return "."

class ZeroOrMore(AST):
    def __init__(self, operand):
        self.operand = operand

class BlankAST(AST):
    pass

class Str(AST):
    def __init__(self, operands):
        self.operands = operands

def shouldBe (input, expected):
  result = str (parseRegExp (input))
  test.assert_equals (result, expected, "parse '{}' = '{}' shouldBe '{}'\n".format (input, result, expected))

shouldBe ('BXwd9VcJ%s$-Q ^v31krt>@gHpF`E,+()Z:#|"fA=;h*Ci_\u<NWU84l].e526T/[', "")

test.describe ("regexp parser")
test.it ("core tests")
print (Normal ('a'))
print (ZeroOrMore (Normal ('a')))
print (Or (Any (),ZeroOrMore (Normal ('a'))))
print (Str([Normal ('a'), Normal ('b')]))
print (Str ([Normal ('b'), Or (Normal ('c'), Normal ('d')), ZeroOrMore (Normal ('e'))]))

test.it ("basic tests")
shouldBe (".", ".")
shouldBe ("a", "a")
shouldBe ("a|b", "(a|b)")
shouldBe ("a*", "a*")
shouldBe ("(a)", "a")
shouldBe ("(a)*", "a*")
shouldBe ("(a|b)*", "(a|b)*")
shouldBe ("a|b*", "(a|b*)")
shouldBe ("abcd", "(abcd)")
shouldBe ("ab|cd", "((ab)|(cd))")

test.it ("precedence examples")
shouldBe ("ab*", "(ab*)")
shouldBe ("(ab)*", "(ab)*")
shouldBe ("ab|a", "((ab)|a)")
shouldBe ("a(b|a)", "(a(b|a))")
shouldBe ("a|b*", "(a|b*)")
shouldBe ("(a|b)*", "(a|b)*")

test.it ("the_other examples")
shouldBe ("a", "a")
shouldBe ("ab", "(ab)")
shouldBe ("a.*", "(a.*)")
shouldBe ("(a.*)|(bb)", "((a.*)|(bb))")

test.it ("invalid examples")
shouldBe ("", "")
shouldBe ("(", "")
shouldBe ("(hi!", "")
shouldBe (")(", "")
shouldBe ("a|t|y", "")
shouldBe ("a**", "")

test.it ("complex examples")
shouldBe ("((aa)|ab)*|a", "(((aa)|(ab))*|a)")
shouldBe ("((a.)|.b)*|a", "(((a.)|(.b))*|a)")
