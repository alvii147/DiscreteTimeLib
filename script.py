import matplotlib.pyplot as plt
from DiscreteTimeLib import DiscreteTimeSystem

if __name__ == '__main__':
    b = [0.634, 0, 0.634]
    a = [1, 0, -0.268]
    H = DiscreteTimeSystem(b, a)
    imp = H.impz((0, 35))
    plt.stem(imp.keys(), imp.values())
    plt.show()