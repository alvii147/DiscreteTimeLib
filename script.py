from DiscreteTimeLib import DiscreteTimeSignal, DiscreteTimeSystem

if __name__ == '__main__':
    H = DiscreteTimeSystem([1], [1, -2, 10])

    h_exp, n = H.iztrans()
    h_num = H.iztrans((0, 4))
    print(h_exp)
    print('')
    print(h_num)
    print('')
    print(h_num[0])
    print(type(h_num[0]))
    print(1 == h_num[0])