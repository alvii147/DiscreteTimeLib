.. DiscreteTimeLib documentation master file, created by
   sphinx-quickstart on Thu Nov 11 13:29:55 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to DiscreteTimeLib's documentation!
===========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules


Overview
--------

Discrete-Time Signals
^^^^^^^^^^^^^^^^^^^^^

The ``DiscreteTimeSignal`` class can be used to model a discrete-time signal:

>>> from DiscreteTimeLib import DiscreteTimeSignal
>>> import numpy as np
>>> import matplotlib.pyplot as plt

>>> data = [
...     (n, np.sin(x)) for n, x in enumerate(np.linspace(0, 2 * np.pi, num=100))
... ]
>>> x_n = DiscreteTimeSignal(data)
>>> print(x_n)
            x[n]
0   0.000000e+00
1   6.342392e-02
2   1.265925e-01
3   1.892512e-01
4   2.511480e-01
..           ...
95 -2.511480e-01
96 -1.892512e-01
97 -1.265925e-01
98 -6.342392e-02
99 -2.449294e-16
<BLANKLINE>
[100 rows x 1 columns]

>>> markerline, stemlines, baseline = plt.stem(x_n.keys(), x_n.values())
>>> plt.setp(markerline, 'markerfacecolor', 'salmon')
>>> plt.setp(markerline, 'markeredgecolor', 'firebrick')
>>> plt.setp(stemlines, 'color', 'orangered')
>>> plt.setp(baseline, 'color', 'red')
>>> plt.show()

.. image:: ../img/discrete_time_signal_plot.png
   :alt: Discrete Time Signal Plot


Convolution
^^^^^^^^^^^

``DiscreteTimeSignal`` supports various operations, including **convolution**:

>>> data = [
...     (n, np.cos(x)) for n, x in enumerate(np.linspace(0, 2 * np.pi, num=100))
... ]
>>> h_n = DiscreteTimeSignal(data)
>>> y_n = h_n * x_n
>>> print(y_n)
            x[n]
0    0.000000e+00
1    6.342392e-02
2    1.898887e-01
3    3.785025e-01
4    6.278700e-01
..            ...
194 -6.278700e-01
195 -3.785025e-01
196 -1.898887e-01
197 -6.342392e-02
198 -2.449294e-16
<BLANKLINE>
[199 rows x 1 columns]

>>> markerline, stemlines, baseline = plt.stem(y_n.keys(), y_n.values())
>>> plt.setp(markerline, 'markerfacecolor', 'lawngreen')
>>> plt.setp(markerline, 'markeredgecolor', 'olive')
>>> plt.setp(stemlines, 'color', 'palegreen')
>>> plt.setp(baseline, 'color', 'green')
>>> plt.show()

.. image:: ../img/convolution_plot.png
   :alt: Convolution Plot


Filtering
^^^^^^^^^

The ``DiscreteTimeSystem`` class can be used to model a discrete-time system and apply the system filter on a signal:

>>> from DiscreteTimeLib import DiscreteTimeSystem

>>> b = (1,)
>>> a = (1, -1)
>>> H = DiscreteTimeSystem(b, a)
>>> y_n = H.filter(x_n)
>>> print(y_n)
            x[n]
0   0.000000e+00
1   6.342392e-02
2   1.900164e-01
3   3.792676e-01
4   6.304156e-01
..           ...
95  3.792676e-01
96  1.900164e-01
97  6.342392e-02
98  1.665335e-15
99  1.420405e-15
<BLANKLINE>
[100 rows x 1 columns]

>>> markerline, stemlines, baseline = plt.stem(y_n.keys(), y_n.values())
>>> plt.setp(markerline, 'markerfacecolor', 'deepskyblue')
>>> plt.setp(markerline, 'markeredgecolor', 'teal')
>>> plt.setp(stemlines, 'color', 'turquoise')
>>> plt.setp(baseline, 'color', 'cyan')
>>> plt.show()

.. image:: ../img/filtered_signal_plot.png
   :alt: Filtered Signal Plot


Inverse z-transforms
^^^^^^^^^^^^^^^^^^^^

The ``DiscreteTimeSystem`` class can also compute the **inverse z-transform** in the form of a `Sympy <https://www.sympy.org/>`_ expression:

>>> h_n, n = H.iztrans()
>>> print(h_n)
1.0*Heaviside(n, 1)


Installation
------------

Clone the repository:

::
   git clone https://github.com/alvii147/DiscreteTimeLib.git

Install dependencies:

::
   cd DiscreteTimeLib/
   pip3 install -r requirements.txt


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
