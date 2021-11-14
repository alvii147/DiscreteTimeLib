from DiscreteTimeLib import DiscreteTimeSignal, DiscreteTimeSystem

if __name__ == '__main__':
    # H = DiscreteTimeSystem([1, 2, 1], [1, -3, 2])
    # print(H.iztrans())
    # print(H.iztrans(n_range=(0, 4)))
    # H = DiscreteTimeSystem([1, -2, 1], [1, 0, -1])
    A = DiscreteTimeSystem([1, -1], [1, 1])
    B = DiscreteTimeSystem([1], [1, 1])
    C = A * B