import numpy as np
from DiscreteTimeLib import DiscreteTimeSignal, DiscreteTimeSystem
from scipy.signal import residuez

if __name__ == '__main__':
    x_n = [1, 4, 2, -1, 6]
    data_x = [[n, x_n[n]] for n in range(len(x_n))]
    x = DiscreteTimeSignal(data_x)
    print(x.values())
    print('')

    b = [1]
    a = [1, -1]
    H = DiscreteTimeSystem(b, a)
    y = H.filter(x)
    print(y.values())
    print('')

    Hinv = DiscreteTimeSystem(a, b)
    x_reconstructed = Hinv.filter(y)
    print(x_reconstructed.values())

    # r, p, k = residuez(a, b)
    # print(r, p, k)
    # print('')
    # sig = np.zeros(signal_len)
    # for n in range(signal_len):
    #     if n >= 0:
    #         for i in range(min(len(r), len(p))):
    #             sig[n] += r[i] * pow(p[i], n)

    #     if n < len(k):
    #         sig[n] += k[n]

    # print(sig)
    # print(np.convolve(x_n, sig))