from DiscreteTimeLib import DiscreteTimeSignal

if __name__ == '__main__':
    data = (
        (-2, 1),
        (-1, 1.5),
        (0, 2),
        (1, 5),
    )
    sig = DiscreteTimeSignal(data)

    print(sig)