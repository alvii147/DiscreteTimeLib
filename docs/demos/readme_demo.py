from DiscreteTimeLib import DiscreteTimeSignal
import numpy as np
import matplotlib.pyplot as plt

data = [
    (n, np.sin(x)) for n, x in enumerate(np.linspace(0, 2 * np.pi, num=100))
]
x_n = DiscreteTimeSignal(data)
print(x_n)

markerline, stemlines, baseline = plt.stem(x_n.keys(), x_n.values())
plt.setp(markerline, 'markerfacecolor', 'salmon')
plt.setp(markerline, 'markeredgecolor', 'firebrick')
plt.setp(stemlines, 'color', 'orangered')
plt.setp(baseline, 'color', 'red')
plt.show()

data = [
    (n, np.cos(x)) for n, x in enumerate(np.linspace(0, 2 * np.pi, num=100))
]
h_n = DiscreteTimeSignal(data)
y_n = h_n * x_n
print(y_n)

markerline, stemlines, baseline = plt.stem(y_n.keys(), y_n.values())
plt.setp(markerline, 'markerfacecolor', 'lawngreen')
plt.setp(markerline, 'markeredgecolor', 'olive')
plt.setp(stemlines, 'color', 'palegreen')
plt.setp(baseline, 'color', 'green')
plt.show()

from DiscreteTimeLib import DiscreteTimeSystem

b = (1,)
a = (1, -1)
H = DiscreteTimeSystem(b, a)
y_n = H.filter(x_n)
print(y_n)

markerline, stemlines, baseline = plt.stem(y_n.keys(), y_n.values())
plt.setp(markerline, 'markerfacecolor', 'deepskyblue')
plt.setp(markerline, 'markeredgecolor', 'teal')
plt.setp(stemlines, 'color', 'turquoise')
plt.setp(baseline, 'color', 'cyan')
plt.show()

h_n, n = H.iztrans()
print(h_n)