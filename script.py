from DiscreteTimeLib import DiscreteTimeSignal

if __name__ == '__main__':
    # data = ((0, 1), (1, 2), (2, 3), (3, 4), (4, 5))
    x = DiscreteTimeSignal()
    print(x)
    print(x.min_idx)
    print(x.max_idx)
    data = ((-1, -1), (0, 2), (1, 1))
    h = DiscreteTimeSignal(data)
    conv = x * h
    print(conv)