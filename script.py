from DiscreteTimeLib import DiscreteTimeSignal

if __name__ == '__main__':
    t1 = ((0, 1), (1, 3), (2, -3))
    s1 = DiscreteTimeSignal(t1)
    t2 = ((-3, 1), (-2, 1), (-1, 3))
    s2 = DiscreteTimeSignal(t2)

    print(s1 + s2)