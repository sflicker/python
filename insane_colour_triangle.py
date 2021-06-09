import random

color_to_num = {"R": 0,
                "G": 1,
                "B": 2}

num_to_color = {0: "R",
                1: "G",
                2: "B"}


def binomial_mod3(n, k):
    result = 1
    while n > 0:
        n3 = n % 3
        k3 = k % 3
        if k3 > n3:
            return 0
        temp = 1 if k3 == 0 or k3 == n3 else 2
        result = (result * temp) % 3
        n = n // 3
        k = k // 3
    return result


def triangle(row):
    n = len(row) - 1

    result = 0
    for k, color in enumerate(row):
        temp = binomial_mod3(n, k) * color_to_num[color]
        result = (result + temp) % 3

    if n % 2 == 1:
        result = (- result) % 3
    return num_to_color[result]

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
print(triangle(generate_random_row(1000000000)));

