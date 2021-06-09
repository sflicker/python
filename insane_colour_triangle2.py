# Let R,G,B=0,1,2
# for x y
#      z
# notice that z==(2*(x+y)) (Mod 3)
#
# a        b        c
#   2(a+b)   2(b+c)
#      4(a+2b+c)
#
# a      b         c        d
#  2(a+b)   2(b+c)   2(c+d)
#    4(a+2b+c) 4(b+2c+d)
#      8(a+3b+3c+d)
#
# Using induction, we can prove the result of
# x0 x1 x2 ... xn    is
# 2^n*(Sum((n,k)*xk))
# where (n,k) is binomial coefficient
# As a result,
# if n%3==0, any k, (n,k)%3==0
import random

def triangle(row):
    n = len(row)
#    print(n)
#    if n > 8000000:
#        return "B"

    reduce = [3 ** i + 1 for i in range(25) if 3 ** i <= 100000000][::-1]
    for length in reduce:
        while len(row) >= length:
            row = [row[i] if row[i] == row[i + length - 1] else ({"R", "G", "B"} - {row[i], row[i + length - 1]}).pop()
                   for i in range(len(row) - length + 1)]
    return row[0]

def generate_random_row(n):

    random.seed()
    s = (''.join(random.choice("RGB") for i in range(n)))
    return s

def test(input, expected):
    print(input, expected)
    actual = triangle(input)
    print(actual)
    assert actual == expected


#test("B", "B")
#test("GB", "R")
#print(triangle("RRR"))
#print(triangle("RGBG"))
#print(triangle("RBRGBRB"))
#print(triangle("RBRGBRBGGRRRBGBBBGG"))
print(triangle(generate_random_row(10000000)));
