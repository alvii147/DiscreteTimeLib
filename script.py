from DiscreteTimeLib import DiscreteTimeSignal, DiscreteTimeSystem
import matplotlib.pyplot as plt

if __name__ == '__main__':
    data = (
        (-3, -2.2),
        (-2, -1),
        (-1, 1.5),
        (0, 2),
        (1, 3.3),
        (2, 5),
        (5, 12),
    )
    sig = DiscreteTimeSignal(data)

    H = DiscreteTimeSystem([1], [1, -1])
    filtered_sig = H.filter(sig)

    print(filtered_sig)

    markerline, stemlines, baseline = plt.stem(
        filtered_sig.keys(),
        filtered_sig.values(),
    )
    plt.setp(markerline, 'markerfacecolor', 'salmon')
    plt.setp(markerline, 'markeredgecolor', 'firebrick')
    plt.setp(stemlines, 'color', 'orangered')
    plt.setp(baseline, 'color', 'red')
    plt.show()