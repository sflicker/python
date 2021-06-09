import codewars_test as test

# Solution by Scott Flicker

def simple_assembler(program):
    print("Assembly Program to Execute")
    print(*program, sep='\n')
    print()
    reg_file = {}
    pc = 0
    instructions_executed = 0
    print()
    print("Beginning Execution")
    while pc < len(program):

        instructions_executed += 1
        instr = program[pc]
        args = instr.split()
        #    print (pc, args, reg_file)

        op = args[0]
        arg1 = args[1]
        arg2 = None
        if len(args) > 2:
            arg2 = args[2]

        if op == "mov":
            if is_integer(arg2):
                reg_file[arg1] = int(arg2)
            else:
                reg_file[arg1] = reg_file[arg2]
        elif op == "inc":
            reg_file[arg1] += 1
        elif op == "dec":
            reg_file[arg1] -= 1
        elif op == "jnz":
            if not is_zero(arg1, reg_file):
                if is_integer(arg2):
                    pc += int(arg2)
                else:
                    pc += reg_file[arg2]
                continue
        pc += 1
    print("Execution Ended Successfully")
    print("Instructions Executed: ", instructions_executed)
    print("Registers After Execution: ", reg_file)
    return reg_file


def is_zero(x, reg_file):
    #   print(x, is_integer(x))
    if is_integer(x):
        if int(x) == 0:
            return True
        else:
            return False
    if reg_file[x] == 0:
        return True


def is_integer(x):
    if x.lstrip("-").isnumeric():
        return True
    return False

#####################
## TESTS FROM CODEWARS PROBLEM
#################

### Simple Example Tests

code = '''\
mov a 5
inc a
dec a
dec a
jnz a -1
inc a'''
test.assert_equals(simple_assembler(code.splitlines()), {'a': 1})

code = '''\
mov c 12
mov b 0
mov a 200
dec a
inc b
jnz a -2
dec c
mov a b
jnz c -5
jnz 0 1
mov c a'''
test.assert_equals(simple_assembler(code.splitlines()), {'a': 409600, 'c': 409600, 'b': 409600})

### Main Test Cases

test.assert_equals(
    simple_assembler(['mov a 5', 'inc a', 'dec a', 'dec a', 'jnz a -1', 'inc a']),
    {'a': 1}
);

test.assert_equals(
    simple_assembler(['mov a -10', 'mov b a', 'inc a', 'dec b', 'jnz a -2']),
    {'a': 0, 'b': -20}
);

test.assert_equals(
    simple_assembler(
        ['mov a 1', 'mov b 1', 'mov c 0', 'mov d 26', 'jnz c 2', 'jnz 1 5', 'mov c 7', 'inc d', 'dec c', 'jnz c -2',
         'mov c a', 'inc a', 'dec b', 'jnz b -2', 'mov b c', 'dec d', 'jnz d -6', 'mov c 18', 'mov d 11', 'inc a',
         'dec d', 'jnz d -2', 'dec c', 'jnz c -5']),
    {'a': 318009, 'b': 196418, 'c': 0, 'd': 0}
);

test.assert_equals(
    simple_assembler(['mov d 100', 'dec d', 'mov b d', 'jnz b -2', 'inc d', 'mov a d', 'jnz 5 10', 'mov c a']),
    {'a': 1, 'b': 0, 'd': 1}
);

test.assert_equals(
    simple_assembler(
        ['mov c 12', 'mov b 0', 'mov a 200', 'dec a', 'inc b', 'jnz a -2', 'dec c', 'mov a b', 'jnz c -5', 'jnz 0 1',
         'mov c a']),
    {'a': 409600, 'c': 409600, 'b': 409600}
);

import random
from re import match


class Assembly:
    def __init__(self, program=None):
        self.instruction = program
        self.register = {}
        self.num_instruction = 0

    def __str__(self):
        out = ""
        for key in sorted(self.register):
            out += "{0}: {1}\n".format(key, self.register[key])

        return out

    def load(self, program):
        self.instruction = program

    def execute(self):
        while self.num_instruction < len(self.instruction):
            cur_instr = self.instruction[self.num_instruction]
            instr_mov = match(r"mov (\w) (-?\d+|\w)", cur_instr)
            instr_inc = match(r"inc (\w)", cur_instr)
            instr_dec = match(r"dec (\w)", cur_instr)
            instr_jnz = match(r"jnz (-?\d+|\w) (-?\d+)", cur_instr)

            if instr_mov:
                value = self.read(instr_mov.group(2))
                reg = instr_mov.group(1)
                self.mov(reg, value)
            elif instr_inc:
                reg = instr_inc.group(1)
                self.add(reg, 1)
            elif instr_dec:
                reg = instr_dec.group(1)
                self.add(reg, -1)
            elif instr_jnz:
                value1 = self.read(instr_jnz.group(1))
                value2 = self.read(instr_jnz.group(2))
                self.jnz(value1, value2)

            self.num_instruction += 1

    def read(self, value):
        if value in self.register:
            return self.register[value]
        else:
            return int(value)

    def add(self, reg, value):
        self.register[reg] += value

    def mov(self, reg, value):
        self.register[reg] = value

    def jnz(self, value1, value2):
        if value1 != 0:
            self.num_instruction += value2 - 1


def my_simple_assembler(program):
    asm = Assembly(program)
    asm.execute()
    return asm.register


vars = ['a', 'b', 'd', 't', 'h', 'k', 's', 'm', 'n', 'g', 'q', 'e', 'c', 'o', 'i', 'u']
myvars = []
prog = []
for i in range(35):
    random.shuffle(vars)
    myvars = vars[0:random.randint(2, 6)]
    # make mov
    for i in myvars:
        prog.append("mov {} {}".format(i, random.randint(20, 40)))
    # create variable z that mght or not be 0 and use jnz
    prog.append("mov {} {}".format('z', random.randint(0, 2)))
    prog.append("jnz {} {}".format('z', random.randint(2, 5)))
    # this jnz over first variable is not used if z != 0
    prog.append("jnz {} {}".format(myvars[0], random.randint(2, 5)))
    # make inc/dec
    for i in myvars:
        for j in range(random.randint(2, 5)):
            prog.append("{} {}".format(random.choice(['inc', 'inc', 'dec']), i))
    # print prog
    solution = my_simple_assembler(prog)
    test.assert_equals(simple_assembler(prog), solution);
    myvars, prog = [], []