from fractions import Fraction


def pascal(p):
    if p == 0:
        return [[1]]
    if p == 1:
        return [[1]]
    t = pascal(p - 1)
    k = [0] * p
    t.append(k)
    i = p - 1
    for j in range(p):
        if j == 0:
            t[i][j] = t[i - 1][0]
        elif j < p - 1:
            t[i][j] = t[i - 1][j - 1] + t[i - 1][j]
        else:
            t[i][j] = t[i - 1][-1]

    return t


def bernoulli_number(n):
    print("n", n)
    if n == 0:
        return 1
    pascal_triangle = pascal(n+2)
    print(pascal_triangle)
    b = [1]
    b = b * (n+1)
    print(b)
    for i in range(1, n+1):
        sum = 1
        for j in range(1, i):
            sum += pascal_triangle[i+1][j+1]*b[j]
        b[i] = Fraction(-sum, pascal_triangle[i + 1][i])
    return b[-1]

#print(0, bernoulli_number((0)))
print(1, bernoulli_number((1)))
#print(2, bernoulli_number((2)))
#print(3, bernoulli_number((3)))

