class Calculator(object):
    def evaluate(self, string):
        tokens = tokenizer(string)
        (pos, parse_tree) = parse(0, tokens)
        return process(parse_tree)

def process(parse_tree):
    if parse_tree['type'] == "Number":
        return float(parse_tree['value'])
    elif parse_tree['type'] == "Unary":
        child = process(parse_tree['child'])
        print(child)
        return -child;
    elif parse_tree['type'] == "Op":
        lhs = process(parse_tree['lhs'])
        rhs = process(parse_tree['rhs'])
        if parse_tree['value'] == "+":
            return lhs + rhs
        elif parse_tree['value'] == "-":
            return lhs - rhs
        elif parse_tree['value'] == "*":
            return lhs * rhs
        elif parse_tree['value'] == "/":
            return lhs / rhs


def get_op_prec(value):
    if value == "+" or value == "-":
        return 1
    elif value == "*" or value == "/":
        return 2


def parse(pos, tokens):
    root = None
    while pos < len(tokens):
        tok = tokens[pos]

        pos = pos + 1
        if tok['type'] == 'Op' and tok['value'] == '-' and root == None:
            (pos, node) = parse(pos, tokens)
            root = {}
            node['type'] = "Unary"
            node['value'] = "-"
            node['child'] = node
        elif tok['type'] == "Paren":
            if tok['value'] == "(":
                (pos, root) = parse(pos, tokens) 
            elif tok['value'] == ")":
                return (pos, root)
        elif tok['type'] == "Number":
            node = {}
            node['type'] = tok['type']
            node['value'] = tok['value']

            if not root:
                root = node

        elif tok['type'] == "Op":
            node = {}
            node['type'] = tok['type']
            node['value'] = tok['value']

            next_tok = tokens[pos]
            if next_tok['type'] == "Paren" and next_tok['value'] == "(":
                (pos, node['rhs']) = parse(pos+1, tokens)
            elif next_tok['type'] == "Number":

                rhs_node = {}
                rhs_node['value'] = next_tok['value']
                rhs_node['type'] = next_tok['type']
                pos = pos + 1
                node['rhs'] = rhs_node

            if root['type'] == "Number":
                node['lhs'] = root
                root = node
            elif get_op_prec(node['value']) > get_op_prec(root['value']):
                tmp = root['rhs']
                node['lhs'] = tmp
                root['rhs'] = node
            else:
                tmp = root
                root = node
                node['lhs'] = tmp

    return (pos, root)

def tokenizer(string):
    tokens=[]
    parens=["(",")"]
    ops=["+","-","*","/"]
    num=None
    for i in range(len(string)):
        c = string[i]
        if c.isdigit() or c == ".":
            if num:
                num = num + c
            else:
                num=c
        else:
            if num:
                tok = {}
                tok['value'] = num
                tok['type'] = "Number"
                tokens.append(tok)
                num = None
                
            if c in parens:
                tok = {}
                tok['value'] = c
                tok['type'] = "Paren"
                tokens.append(tok)
            elif c in ops:
                tok = {}
                tok['value'] = c
                tok['type'] = "Op"
                tokens.append(tok)
                          
    if num:
        tok = {}
        tok['type'] = "Number"
        tok['value'] = num
        tokens.append(tok)
                          
    return tokens
                         
            
#assert Calculator().evaluate("-1") == -1
assert Calculator().evaluate("2 / 2 + 3 * 4 - 6") == 7
assert Calculator().evaluate("3 * 4 + 3 * 7 - 6") == 27
assert Calculator().evaluate("1 + 1") == 2
assert Calculator().evaluate("10") == 10
assert Calculator().evaluate("(5)") == 5
assert Calculator().evaluate("( ( ( ( 1 ) * 2 ) ) )") == 2
assert Calculator().evaluate("6 / (3 + 3) * 4 - 6") == -2
assert Calculator().evaluate("1.1 * 2.2 * 3.3") - 7.986 < 0.001
