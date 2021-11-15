from DiscreteTimeLib import DiscreteTimeSignal, DiscreteTimeSystem
import numpy as np

if __name__ == '__main__':
    data = (
        (0, 1),
        (1, 2),
        (2, 4),
    )
    x_n = DiscreteTimeSignal(data)
    print(x_n)
    print('')

    H = DiscreteTimeSystem([1, 2, 1], [1, -3, 2])
    y_n = H.filter(x_n)
    print(y_n)
    print('')

    h_exp, n = H.iztrans()
    h_num = H.iztrans((0, 10))
    print(h_exp)
    print('')
    print(h_num)