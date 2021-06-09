from re import match
import codewars_test as test

#solution by scott flicker

def assembler_interpreter(program):
    print("Assembler Interpreter")
    print("Program");
    print(program)

    program_lines = program.splitlines()
    msg = ""
    reg_file = {}
    label_table = {}
    ## scan for labels
    for line_num, line_text in enumerate(program_lines):
        label = match(r"([a-z].+:)", line_text)
        if label:
            label_table[label.group(0)[:-1]] = line_num

    pc = 0
    instructions_executed = 0
    print()
    print("Beginning Execution")
    while pc < len(program_lines):
        instr = program_lines[pc]
        instr_mov = match(r"mov\W*(\w),\W*(-?\d+|\w)", instr)
        instr_inc = match(r"inc\W*(\w)",instr)
        instr_dec = match(r"dec\W*(\w)",instr)
        instr_add = match(r"add\W*(\w),\W*(-?\d+|\w)", instr)
        instr_sub = match(r"sub\W*(\w),\W*(-?\d+|\w)", instr)
        instr_mul = match(r"mul\W*(\w),\W*(-?\d+|\w)", instr)
        instr_div = match(r"div\W*(\w),\W*(-?\d+|\w)", instr)
        instr_jmp = match(r"jmp\W*(\w)",instr)
        instr_cmp = match(r"cmp\W*(-?\d+|\w),\W(-?\d+|\w)", instr)
        instr_jne = match(r"jne\W*(\w+)",instr)
        instr_je = match(r"je\W*(\w+)", instr)
        instr_jge = match(r"jge\W*(\w+)", instr)
        instr_jg = match(r"jg\W*(\w+)", instr)
        instr_jle = match(r"jle\W*(\w+)", instr)
        instr_jl = match(r"jl\W*(\w+)", instr)
        instr_call = match(r"call\W*(\w+)", instr)
        instr_ret = match(r"ret", instr)
        instr_msg = match(r"msg(.*)", instr)
        instr_end = match(r"end", instr)

        if instr_mov:

            pc += 1

        elif instr_inc:
            pass
        elif instr_dec:
            pass
        elif instr_add:
            pass
        elif instr_sub:
            pass
        elif instr_mul:
            pass
        elif instr_div:
            pass
        elif instr_jmp:
            pc = label_table[instr_jmp.group(0)]

        instructions_executed += 1







    return "" # output





#####################
## Sample tests from Codewars

program = '''
; My first program
mov  a, 5
inc  a
call function
msg  '(5+1)/2 = ', a    ; output message
end

function:
    div  a, 2
    ret
'''

test.assert_equals(assembler_interpreter(program), '(5+1)/2 = 3')

program_factorial = '''
mov   a, 5
mov   b, a
mov   c, a
call  proc_fact
call  print
end

proc_fact:
    dec   b
    mul   c, b
    cmp   b, 1
    jne   proc_fact
    ret

print:
    msg   a, '! = ', c ; output text
    ret
'''

test.assert_equals(assembler_interpreter(program_factorial), '5! = 120')

program_fibonacci = '''
mov   a, 8            ; value
mov   b, 0            ; next
mov   c, 0            ; counter
mov   d, 0            ; first
mov   e, 1            ; second
call  proc_fib
call  print
end

proc_fib:
    cmp   c, 2
    jl    func_0
    mov   b, d
    add   b, e
    mov   d, e
    mov   e, b
    inc   c
    cmp   c, a
    jle   proc_fib
    ret

func_0:
    mov   b, c
    inc   c
    jmp   proc_fib

print:
    msg   'Term ', a, ' of Fibonacci series is: ', b        ; output text
    ret
'''

test.assert_equals(assembler_interpreter(program_fibonacci), 'Term 8 of Fibonacci series is: 21')

program_mod = '''
mov   a, 11           ; value1
mov   b, 3            ; value2
call  mod_func
msg   'mod(', a, ', ', b, ') = ', d        ; output
end

; Mod function
mod_func:
    mov   c, a        ; temp1
    div   c, b
    mul   c, b
    mov   d, a        ; temp2
    sub   d, c
    ret
'''

test.assert_equals(assembler_interpreter(program_mod), 'mod(11, 3) = 2')

program_gcd = '''
mov   a, 81         ; value1
mov   b, 153        ; value2
call  init
call  proc_gcd
call  print
end

proc_gcd:
    cmp   c, d
    jne   loop
    ret

loop:
    cmp   c, d
    jg    a_bigger
    jmp   b_bigger

a_bigger:
    sub   c, d
    jmp   proc_gcd

b_bigger:
    sub   d, c
    jmp   proc_gcd

init:
    cmp   a, 0
    jl    a_abs
    cmp   b, 0
    jl    b_abs
    mov   c, a            ; temp1
    mov   d, b            ; temp2
    ret

a_abs:
    mul   a, -1
    jmp   init

b_abs:
    mul   b, -1
    jmp   init

print:
    msg   'gcd(', a, ', ', b, ') = ', c
    ret
'''

test.assert_equals(assembler_interpreter(program_gcd), 'gcd(81, 153) = 9')

program_fail = '''
call  func1
call  print
end

func1:
    call  func2
    ret

func2:
    ret

print:
    msg 'This program should return -1'
'''

test.assert_equals(assembler_interpreter(program_fail), -1)

program_power = '''
mov   a, 2            ; value1
mov   b, 10           ; value2
mov   c, a            ; temp1
mov   d, b            ; temp2
call  proc_func
call  print
end

proc_func:
    cmp   d, 1
    je    continue
    mul   c, a
    dec   d
    call  proc_func

continue:
    ret

print:
    msg a, '^', b, ' = ', c
    ret
'''

test.assert_equals(assembler_interpreter(program_power), '2^10 = 1024')





