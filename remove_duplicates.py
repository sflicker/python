def solve(arr):
    not_checked = set(arr);
    while not_checked:
        curr = None
        for count, value in reversed(list(enumerate(arr))):
            if curr == None:
                if value in not_checked:
                    curr = value
                    not_checked.remove(value)
            else:
                if curr == value:
                    arr.pop(count)
    return arr;

res = solve([3,4,4,3,6,3])
print(res)