import numpy as np
from scipy.signal import lfilter, residuez
from sympy import Symbol, Heaviside, KroneckerDelta

from DiscreteTimeLib.signals import DiscreteTimeSignal


class DiscreteTimeSystem:
    '''
    Discrete-time system object, implemented as a digital filter.

    Parameters `b` and `a` are numerator and denominator coefficients for
    the transfer function of the system.

    .. math::
        H(z) =
        \\frac{b_0 + b_1 z^{-1} + ... + b_n z^{-n}}
        {a_0 + a_1 z^{-1} + ... + a_m z^{-m}}

    Parameters
    ----------
    b : ndarray
        One-dimensional array-like representing transfer function
        numerator coefficients.
    a : ndarray
        One-dimensional array-like representing transfer function
        denominator coefficients.
    '''

    def __init__(self, b, a):
        '''
        Initializer for discrete-time system object.

        Parameters
        ----------
        b : ndarray
            One-dimensional array-like representing transfer function
            numerator coefficients.

        a : ndarray
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

    def filter(self, sig):
        '''
        Apply digital filter on discrete-time signal.

        Parameters
        ----------
        sig : DiscreteTimeSignal
            Given discrete-time signal.

        Returns
        -------
        DiscreteTimeSignal
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

    def iztrans(self, n_range=None):
        '''
        Compute z-transform of system.

        Parameters
        ----------
        n_range : ndarray, optional
            Range of indices to compute z-transform for. For e.g. set
            ``n_range = [-1, 3]`` to compute from ``n = -1`` to ``n = 2``
            inclusive.

        Returns
        -------
        iztrans : ndarray or sympy expression
            Z-transform of the system, computed as an array if ``n_range``
            is given, computed as a sympy expression otherwise.

        n : sympy Symbol
            Symbolic variable used to create sympy expression. This is only
            returned if ``n_range`` is not given.
        '''

        numeric_answer = False
        # raise error if n_range shape is not (2,)
        if n_range is not None:
            n_range_shape = np.shape(n_range)
            if len(n_range_shape) != 1 or n_range_shape[0] != 2:
                raise ValueError('n_range must be a two-element array')

            numeric_answer = True

        iztrans_exp = 0
        # get partial fraction decomposition
        r, p, k = residuez(self.b, self.a)

        # create expression for inverse z-transform
        n = Symbol('n')
        for i in range(max(np.shape(r)[0], np.shape(p)[0])):
            p_coeff = p[i] if p[i] == 1.0 else p[i] ** n
            iztrans_exp += r[i] * p_coeff * Heaviside(n, 1)

        for i in range(np.shape(k)[0]):
            iztrans_exp += k[i] * KroneckerDelta(n - i, 0)

        if numeric_answer:
            # compute inverse z-transform values for n_range
            data = ()
            for n_idx in range(*n_range):
                val = iztrans_exp.subs(n, n_idx)
                try:
                    val = np.float64(iztrans_exp.subs(n, n_idx))
                except TypeError:
                    val = np.clongdouble(iztrans_exp.subs(n, n_idx))

                data += ((n_idx, val),)

            iztrans_num = DiscreteTimeSignal(
                data,
                dtype=np.array(data).dtype,
            )

            return iztrans_num

        return iztrans_exp, n
