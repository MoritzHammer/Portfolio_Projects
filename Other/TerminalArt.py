import time


def power(n):
    return lambda a: pow(a, n)


quadratic = power(2)
cubic = power(3)
quartic = power(4)
quintic = power(5)

fun_start = time.perf_counter()
for x in range(1, 1001):
    s = f"{x} - {quadratic(x)}\t{cubic(x)}\t{quartic(x)}\t{quintic(x)}"
    print(s)
fun_stop = time.perf_counter()
print(fun_stop - fun_start)
