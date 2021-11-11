import numpy as np
from scipy.signal import lfilter

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
    b : numpy.ndarray
        One-dimensional array-like representing transfer function
        numerator coefficients.
    a : numpy.ndarray
        One-dimensional array-like representing transfer function
        denominator coefficients.
    '''

    def __init__(self, b, a):
        '''
        Initializer for discrete-time system object.

        Parameters
        ----------
        b : numpy.ndarray
            One-dimensional array-like representing transfer function
            numerator coefficients.

        a : numpy.ndarray
            One-dimensional array-like representing transfer function
            denominator coefficients.
        '''

        b_shape = np.shape(b)
        a_shape = np.shape(a)

        # raise error if b is not one-dimensional
        if len(b_shape) != 1:
            err_msg = 'Numerator coefficients b, '
            err_msg += 'must be one-dimensional.'
            raise ValueError(err_msg)

        # raise error if a is not one-dimensional
        if len(a_shape) != 1:
            err_msg = 'Denominator coefficients a, '
            err_msg += 'must be one-dimensional.'
            raise ValueError(err_msg)

        # raise error if b has no coefficients
        if b_shape[0] < 1:
            err_msg = 'Numerator coefficients b, '
            err_msg += 'must have at least one coefficient.'
            raise ValueError(err_msg)

        # raise error if a has no coefficients
        if a_shape[0] < 1:
            err_msg = 'Numerator coefficients a, '
            err_msg += 'must have at least one coefficient.'
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

        sig_values = sig.values()
        y_values = lfilter(self.b, self.a, sig_values)

        data = ()
        for n in range(sig.min_idx, sig.max_idx + 1):
            data += ((n, y_values[n - sig.min_idx]),)

        y_n = DiscreteTimeSignal(data)

        return y_n
