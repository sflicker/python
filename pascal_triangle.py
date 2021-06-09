
def pascals_triangle_recursive(n):
    if n <= 0:
        raise Exception("N must greater than zero")
    if n == 1:
        p = []
        p.append([1])
        return p
    p = pascals_triangle_recursive(n-1)
    k = [0] * n
    p.append(k)
    i = n-1
    for j in range(n):

        if j == 0:
            p[i][j] = p[i - 1][j]
        elif j < n-1:
            p[i][j] = p[i - 1][j - 1] + p[i - 1][j]
        else:
            p[i][j] = p[i - 1][i - 1]

       # print("i", i, "j", j, "p", p)

    return p


def pascals_triangle(n):
    print("n", n)
    p = [1]
    k = [1]
    k[0] = 1
    p[0] = k
    p[0][0] = 1
    print("p", p)
    print()
    for i in range(1, n+1):
        print("i", i)
        k = [0]*(i+1)
        p.append(k)
        print("p", p, "k", k)
        for j in range(i+1):
            print("j", j)

            print (j==0, j < i, not (j<i) )
            if j == 0:
                p[i][j] = p[i-1][j]
            elif j < i:
                p[i][j] = p[i-1][j-1] + p[i-1][j]
            else:
                p[i][j] = p[i-1][j-1]

            print("i", i, "j", j, "p", p)
        print("p", p)
        print()

    print("p", p)
    flatten_p = [j for sub in p for j in sub]
    print("flatten_p", flatten_p)
    return flatten_p

def pretty_print(p):
    def format_row(row):
        return ' '.join(map(str, row))
    width = len(format_row(p[-1]))
    for row in p:
        print(format_row(row).center(width))

for i in range(1, 30+1):
    p = pascals_triangle_recursive(i)
    pretty_print(p)
    print()

#p = pascals_triangle_recursive(2)
#pretty_print(p)
#print()

#p = pascals_triangle_recursive(3)
#pretty_print(p)