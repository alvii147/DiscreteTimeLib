import numpy as np
from scipy.signal import lfilter, residuez
from sympy import Symbol, Heaviside, KroneckerDelta

from DiscreteTimeLib.signals import DiscreteTimeSignal


class DiscreteTimeSystem:
    '''
    Discrete-time system object, implemented as a digital filter.

    Parameters `b` and `a` are numerator and denominator coefficients for the
    transfer function of the system.

    .. math::
        H(z) =
        \\frac{b_0 + b_1 z^{-1} + ... + b_n z^{-n}}
        {a_0 + a_1 z^{-1} + ... + a_m z^{-m}}

    Parameters
    ----------
    b : array-like
        One-dimensional array-like representing transfer function numerator
        coefficients.
    a : array-like
        One-dimensional array-like representing transfer function denominator
        coefficients.
    '''

    def __init__(self, b, a):
        '''
        Initializer for discrete-time system object.

        Parameters
        ----------
        b : array-like
            One-dimensional array-like representing transfer function numerator
            coefficients.

        a : array-like
            One-dimensional array-like representing transfer function
            denominator coefficients.
        '''

        b_shape = np.shape(b)
        a_shape = np.shape(a)

        # raise error if b is not one-dimensional
        if len(b_shape) != 1:
            err_msg = 'Numerator coefficients b, '
            err_msg += 'must be one-dimensional'
            raise ValueError(err_msg)

        # raise error if a is not one-dimensional
        if len(a_shape) != 1:
            err_msg = 'Denominator coefficients a, '
            err_msg += 'must be one-dimensional'
            raise ValueError(err_msg)

        # raise error if b has no coefficients
        if b_shape[0] < 1:
            err_msg = 'Numerator coefficients b, '
            err_msg += 'must have at least one coefficient'
            raise ValueError(err_msg)

        # raise error if a has no coefficients
        if a_shape[0] < 1:
            err_msg = 'Numerator coefficients a, '
            err_msg += 'must have at least one coefficient'
            raise ValueError(err_msg)

        # save numerator and denominator coefficients
        self.b = np.array(b)
        self.a = np.array(a)

    def eval(self, z):
        '''
        Evaluate filter at given input value.

        Parameters
        ----------
        z : numpy.clongdouble
            Given input value.

        Returns
        -------
        val : numpy.clongdouble
            Conputed output value.
        '''

        # sum numerator values
        numerator = np.clongdouble(0)
        for i, b_i in enumerate(self.b):
            numerator += b_i * (z ** (-i))

        # sum denominator values
        denominator = np.clongdouble(0)
        for i, a_i in enumerate(self.a):
            denominator += a_i * (z ** (-i))

        val = numerator / denominator

        return val

    def filter(self, sig):
        '''
        Apply digital filter on discrete-time signal.

        Parameters
        ----------
        sig : DiscreteTimeSignal
            Given discrete-time signal.

        Returns
        -------
        y_n : DiscreteTimeSignal
            Filtered discrete-time signal.
        '''

        # get signal values
        sig_values = sig.values()
        # pass signal values through filter
        y_values = lfilter(self.b, self.a, sig_values)

        data = ()
        for n in range(sig.min_idx, sig.max_idx + 1):
            data += ((n, y_values[n - sig.min_idx]),)

        y_n = DiscreteTimeSignal(
            data,
            dtype=y_values.dtype,
        )

        return y_n

    def iztrans(self):
        '''
        Compute inverse z-transform of system.

        Returns
        -------
        exp : sympy.core.expr.Expr
            Z-transform of the system, computed as a sympy expression.

        n : sympy.core.symbol.Symbol
            Symbolic variable used to create sympy expression.
        '''

        exp = 0
        # get partial fraction decomposition
        r, p, k = residuez(self.b, self.a)

        # create expression for inverse z-transform
        n = Symbol('n')
        for i in range(max(np.shape(r)[0], np.shape(p)[0])):
            p_coeff = p[i] if p[i] == 1.0 else p[i] ** n
            exp += r[i] * p_coeff * Heaviside(n, 1)

        for i in range(np.shape(k)[0]):
            exp += k[i] * KroneckerDelta(n - i, 0)

        return exp, n

    def impz(self, n_range):
        '''
        Compute impulse response of system.

        Parameters
        ----------
        n_range : array-like, optional
            Range of indices to compute impulse response for. For e.g. set
            ``n_range = [-1, 3]`` to compute from ``n = -1`` to ``n = 2``
            inclusive.

        Returns
        -------
        response : DiscreteTimeSignal
            Impulse response signal of system.
        '''

        # raise error if n_range shape is not (2,)
        n_range_shape = np.shape(n_range)
        if len(n_range_shape) != 1 or n_range_shape[0] != 2:
            raise ValueError('n_range must be a two-element array')

        # compute inverse z-transform values for n_range
        iztrans_exp, n = self.iztrans()

        data = ()
        for n_idx in range(*n_range):
            val = iztrans_exp.subs(n, n_idx)
            try:
                val = np.float64(iztrans_exp.subs(n, n_idx))
            except TypeError:
                val = np.clongdouble(iztrans_exp.subs(n, n_idx))

            data += ((n_idx, val),)

        response = DiscreteTimeSignal(
            data,
            dtype=np.array(data).dtype,
        )

        return response

    def freqz(self, w_range, num=50):
        '''
        Compute magnitude frequency response of system.

        Parameters
        ----------
        w_range : array-like
            Range of angular velocities to compute frequency response for. For
            e.g. set ``n_range = [-np.pi, np.pi]`` to compute from
            :math:`\\omega = -\\pi` to :math:`\\omega = -\\pi`.

        num : int, optional
            Number of points to divide range into.

        Returns
        -------
        freq_response : numpy.ndarray
            Frequency response of system.
        '''

        freq_response = np.zeros(num, dtype=np.float64)
        # calculate frequency response using w values
        for i, w in enumerate(np.linspace(w_range[0], w_range[1], num=num)):
            # compute z value given w
            z = np.cos(w) + (np.clongdouble(1j) * np.sin(w))
            # compute magnitude of response
            freq_response[i] = np.abs(self.eval(z))

        return freq_response
