# DiscreteTimeLib

**DiscreteTimeLib** is a Python library for the analysis of discrete-time signals and systems. See [documentation](https://alvii147.github.io/DiscreteTimeLib/build/html/index.html) for more information.

## Overview

### Discrete-Time Signals

The `DiscreteTimeSignal` class can be used to model a discrete-time signal:

```python
>>> from DiscreteTimeLib import DiscreteTimeSignal
>>> import matplotlib.pyplot as plt
```

```python
>>> data = ((-1, -2), (0, 1), (1, 2.5), (4, 4))
>>> x_n = DiscreteTimeSignal(data)
>>> print(x_n)
    x[n]
-1  -2.0
 0   1.0
 1   2.5
 4   4.0
```

```python
>>> markerline, stemlines, baseline = plt.stem(x_n.keys(), x_n.values())
>>> plt.setp(markerline, 'markerfacecolor', 'salmon')
>>> plt.setp(markerline, 'markeredgecolor', 'firebrick')
>>> plt.setp(stemlines, 'color', 'orangered')
>>> plt.setp(baseline, 'color', 'red')
>>> plt.show()
```

![Discrete Time Signal Plot](img/discrete_time_signal_plot.png)

### Convolution

`DiscreteTimeSignal` supports various operations, including **convolution**:

```python
>>> data = ((-1, 2), (0, 2.5), (1, 2.1))
>>> h_n = DiscreteTimeSignal(data)
>>> y_n = h_n * x_n
>>> print(y_n)
     x[n]
-2  -4.00
-1  -3.00
 0   3.30
 1   8.35
 2   5.25
 3   8.00
 4  10.00
 5   8.40
```

```python
>>> markerline, stemlines, baseline = plt.stem(y_n.keys(), y_n.values())
>>> plt.setp(markerline, 'markerfacecolor', 'lawngreen')
>>> plt.setp(markerline, 'markeredgecolor', 'olive')
>>> plt.setp(stemlines, 'color', 'palegreen')
>>> plt.setp(baseline, 'color', 'green')
>>> plt.show()
```

![Convolution Plot](img/convolution_plot.png)

### Filtering

The `DiscreteTimeSystem` class can be used to model a discrete-time system and apply the system filter on a signal:

```python
>>> from DiscreteTimeLib import DiscreteTimeSystem
```

```python
>>> H = DiscreteTimeSystem([1], [1, -1])
>>> y_n = H.filter(x_n)
>>> print(y_n)
    x[n]
-1  -2.0
 0  -1.0
 1   1.5
 2   1.5
 3   1.5
 4   5.5
```

```python
>>> markerline, stemlines, baseline = plt.stem(y_n.keys(), y_n.values())
>>> plt.setp(markerline, 'markerfacecolor', 'deepskyblue')
>>> plt.setp(markerline, 'markeredgecolor', 'teal')
>>> plt.setp(stemlines, 'color', 'turquoise')
>>> plt.setp(baseline, 'color', 'cyan')
>>> plt.show()
```

![Filtered Signal Plot](img/filtered_signal_plot.png)

### Inverse z-transforms

The `DiscreteTimeSystem` class can also compute the **inverse z-transform** in the form of a [Sympy](https://www.sympy.org/) expression:

```python
>>> h_n, n = H.iztrans()
>>> print(h_n)
1.0*Heaviside(n, 1)
```

## Installation

Clone the repository:

```
git clone https://github.com/alvii147/DiscreteTimeLib.git
```

Install dependencies:

```
cd DiscreteTimeLib/
pip3 install -r requirements.txt
```
