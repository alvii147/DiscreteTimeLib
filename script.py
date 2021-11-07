import numpy as np
from DiscreteTimeLib import DiscreteTimeSignal, DiscreteTimeSystem

if __name__ == '__main__':
    x_n = [1, 4, 2, -1, 6]
    data_x = [[n, x_n[n]] for n in range(-3, len(x_n) - 3)]
    x = DiscreteTimeSignal(data_x)
    print(x)
    print('')

    b = [1]
    a = [1, -1]
    H = DiscreteTimeSystem(b, a)
    y = H.filter(x)
    print(y)
    print('')

    y_expected = []
    for n in range(data_x[0][0], data_x[-1][0] + 1):
        val = 0
        for i in range(len(b)):
            val += b[i] * x[n - i]

        for i in range(1, len(a)):
            val -= a[i] * y[n - i]

        val = val / a[0]
        y_expected.append(val)

    print(y_expected)