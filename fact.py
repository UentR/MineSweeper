def loop(x):
    result = 1
    for i in range(2, x + 1):
        print(i)
        result *= i
    return result

def recursive(x):
    if x == 1:
        return 1
    else:
        return x * recursive(x - 1)

c = int(input())

print(loop(c))
print(recursive(c))