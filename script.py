import numpy as np
import matplotlib.pyplot as plt
from DiscreteTimeLib import DiscreteTimeSystem

if __name__ == '__main__':
    b = [0.5]
    a = [1, -0.5]
    H = DiscreteTimeSystem(b, a)
    fr, w = H.freqz((-np.pi, np.pi), num=50)
    plt.stem(w, fr)
    plt.show()