# 斐波那契数列
def fib(n):
    if n == 1 or n == 2:
        return 1
    return fib(n-1) + fib(n - 2)


a = fib(10)
print(a)


# 汉诺塔
def hanNuo(n, a, b, c):
    if (n == 1):
        print(a, "->", c)
        return
    hanNuo(n - 1, a, c, b)
    hanNuo(1, a, b, c)
    hanNuo(n - 1, b, a, c)


hanNuo(5, "a", "b", "c")
