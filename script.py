from DiscreteTimeLib import DiscreteTimeSignal, DiscreteTimeSystem

if __name__ == '__main__':
    H = DiscreteTimeSystem([1, 2, 1], [1, -3, 2])
    print(H.iztrans())
    print(H.iztrans(n_range=(0, 4)))