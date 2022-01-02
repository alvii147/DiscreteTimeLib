import numpy as np
import matplotlib.pyplot as plt
from DiscreteTimeLib import DiscreteTimeSystem

if __name__ == '__main__':
    b = [0.634, 0, 0.634]
    a = [1, 0, -0.268]
    H = DiscreteTimeSystem(b, a)
    f = H.freqz((-np.pi, np.pi), num=50)
    plt.stem(np.linspace(-np.pi, np.pi, num=50), f)
    plt.show()