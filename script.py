import numpy as np
from DiscreteTimeLib import DiscreteTimeSignal, DiscreteTimeSystem
import matplotlib.pyplot as plt


if __name__ == '__main__':
    N = 64
    data_f = [
        [n, np.cos(2 * np.pi * n) / (N - 1)]
        for n in range(N)
    ]
    f = DiscreteTimeSignal(data_f)

    a = -2 + np.sqrt(3)

    Hp = DiscreteTimeSystem([1], [1, -a])
    c_p = Hp.filter(f)

    Hm = DiscreteTimeSystem([1], [1, -1/a])
    c_m = Hm.filter(f)

    g = (6 * a) / ((a ** 2) - 1)
    c = g * (c_p - c_m)

    data_b = (
        (-1, 1/6),
        (0, 2/3),
        (1, 1/6),
    )
    b = DiscreteTimeSignal(data_b)

    fc = c * b

    plt.plot(fc.values(), color='orchid')
    plt.ylim(-1.5, 1.5)
    plt.show()