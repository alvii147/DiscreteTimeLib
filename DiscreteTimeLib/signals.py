import numpy as np
import pandas as pd


class DiscreteTimeSignal:
    '''
    Discrete-time signal object, implemented with digital signal processing
    functions.

    Parameters
    ----------
    data : array-like
        Two-dimensional array representing signal data.

        For e.g., ``((0, 2), (1, 4))`` indicates ``x[0] = 2`` and
        ``x[1] = 4``.

    dtype : float, optional
        Data type of signal values.

    Examples
    --------
    >>> data = ((-3, -2.2),
    ...         (-2, -1),
    ...         (-1, 1.5),
    ...         (0, 2),
    ...         (1, 3.3),
    ...         (2, 5),
    ...         (5, 12))
    >>> x_n = DiscreteTimeSignal(data)
    >>> print(x_n)
        x[n]
    -3  -2.2
    -2  -1.0
    -1   1.5
    0   2.0
    1   3.3
    2   5.0
    5  12.0
    '''

    def __init__(self, data=(), dtype=np.float64):
        '''
        Initializer for discrete-time signal object.

        Parameters
        ----------
        data : array-like
            Two-dimensional array representing signal data.

            For e.g., ``((0, 2), (1, 4))`` indicates ``x[0] = 2`` and
            ``x[1] = 4``.

        dtype : float, optional
            Data type of signal values.
        '''

        data_shape = np.shape(data)

        # raise error if data is not of shape (_, 2, ...)
        if data_shape[0] > 0 and (len(data_shape) < 2 or data_shape[1] != 2):
            raise ValueError('data must consist of key-value pairs')

        # set NumPy array priority
        self.__array_priority__ = 10000

        # discrete signal indices
        keys = np.zeros(data_shape[0], dtype=np.int64)
        # discrete signal values
        self.dtype = dtype
        values = np.zeros(data_shape[0], dtype=self.dtype)
        # lowest index with non-zero value
        self.min_idx = float('inf')
        # highest index with non-zero value
        self.max_idx = float('-inf')

        for n in range(data_shape[0]):
            keys[n] = data[n][0]
            values[n] = data[n][1]
            self.min_idx = min(self.min_idx, data[n][0])
            self.max_idx = max(self.max_idx, data[n][0])

        # create dataframe with signal indices and values
        self.signal = pd.DataFrame(
            {
                'x[n]': values,
            },
            index=keys,
        )

    def __str__(self):  # pragma: no cover
        '''
        String representation of object.

        Returns
        -------
        str
            String representation.
        '''

        return str(self.signal)

    def __len__(self):
        '''
        Get length of signal.

        Returns
        -------
        int
            Length of signal.
        '''

        return self.signal.shape[0]

    def __getitem__(self, key):
        '''
        Fetch signal value by index.

        Parameters
        ----------
        key : int
            Index to fetch.

        Returns
        -------
        float
            Value at index.
        '''

        # access value in dataframe using key
        try:
            return self.signal.loc[key]['x[n]']
        # return 0 if key does not exist
        except KeyError:
            return 0.0

    def keys(self):
        '''
        Fetch all signal keys.

        Returns
        -------
        numpy.ndarray
            Signal keys array.
        '''

        return np.arange(self.min_idx, self.max_idx + 1)

    def values(self):
        '''
        Fetch all signal values.

        Returns
        -------
        values : numpy.ndarray
            Signal values array.
        '''

        # fill array with values
        values = np.zeros(
            self.max_idx - self.min_idx + 1,
            dtype=self.dtype,
        )
        for n in range(self.min_idx, self.max_idx + 1):
            values[n - self.min_idx] = self[n]

        return values

    def __eq__(self, sig):
        '''
        Compare this and given discrete-time signal for equality.

        Parameters
        ----------
        sig : DiscreteTimeSignal
            Given discrete-time signal.

        Returns
        -------
        bool
            Boolean value indicating equality.
        '''

        # get iterator range
        if len(self) == 0:
            if len(sig) == 0:
                return True
            else:
                iter_min_idx = sig.min_idx
                iter_max_idx = sig.max_idx
        elif len(sig) == 0:
            iter_min_idx = self.min_idx
            iter_max_idx = self.max_idx
        else:
            iter_min_idx = min(self.min_idx, sig.min_idx)
            iter_max_idx = max(self.max_idx, sig.max_idx)

        # iterate each index and test equality
        for n in range(iter_min_idx, iter_max_idx + 1):
            if not np.isclose(self[n], sig[n]):
                return False

        return True

    def __ne__(self, sig):
        '''
        Compare this and given discrete-time signal for inequality.

        Parameters
        ----------
        sig : DiscreteTimeSignal
            Given discrete-time signal.

        Returns
        -------
        bool
            Boolean value indicating inequality.
        '''

        return not self.__eq__(sig)

    def element_wise_operation(self, sig, op='add'):
        '''
        Perform element-wise operation between this and given discrete-time
        signal objects.

        Parameters
        ----------
        sig : DiscreteTimeSignal
            Given discrete-time signal.

        op : str
            Operation to perform ('add'/'sub')

        Returns
        -------
        result_signal : DiscreteTimeSignal
            Resulting discrete-time signal.
        '''

        # get iterator range
        if len(self) == 0:
            if len(sig) == 0:
                empty_signal = DiscreteTimeSignal()

                return empty_signal
            else:
                result_min_idx = sig.min_idx
                result_max_idx = sig.max_idx
        elif len(sig) == 0:
            result_min_idx = self.min_idx
            result_max_idx = self.max_idx
        else:
            result_min_idx = min(self.min_idx, sig.min_idx)
            result_max_idx = max(self.max_idx, sig.max_idx)

        # iterate each index and record resulting values
        data = ()
        for n in range(result_min_idx, result_max_idx + 1):
            if op == 'add':
                data += ((n, self[n] + sig[n]),)
            elif op == 'sub':
                data += ((n, self[n] - sig[n]),)

        # create new discrete-time signal object using data
        result_signal = DiscreteTimeSignal(
            data,
            dtype=np.result_type(self.dtype, sig.dtype),
        )

        return result_signal

    def __add__(self, sig):
        '''
        Add adjacent elements between this and given discrete-time signal
        objects.

        Parameters
        ----------
        sig : DiscreteTimeSignal
            Given discrete-time signal.

        Returns
        -------
        DiscreteTimeSignal
            Summation discrete-time signal.
        '''

        return self.element_wise_operation(sig, op='add')

    def __sub__(self, sig):
        '''
        Subtract adjacent elements between this and given discrete-time signal
        objects.

        Parameters
        ----------
        sig : DiscreteTimeSignal
            Given discrete-time signal.

        Returns
        -------
        DiscreteTimeSignal
            Subtracted discrete-time signal.
        '''

        return self.element_wise_operation(sig, op='sub')

    def scalar_mul(self, scalar):
        '''
        Compute scalar multiplication on signal.

        Parameters
        ----------
        scalar : int
            Given scalar value.

        Returns
        -------
        scaled_signal : DiscreteTimeSignal
            Scaled discrete-time signal.
        '''

        data = ()
        for n in range(self.min_idx, self.max_idx + 1):
            data += ((n, self[n] * scalar),)

        # create new discrete-time signal object using data
        scaled_signal = DiscreteTimeSignal(
            data,
            dtype=np.result_type(self.dtype, type(scalar)),
        )

        return scaled_signal

    def conv(self, sig):
        '''
        Compute discrete convolution between this and given discrete-time
        signal objects.

        Parameters
        ----------
        sig : DiscreteTimeSignal
            Given discrete-time signal.

        Returns
        -------
        conv_signal : DiscreteTimeSignal
            Discrete convolution discrete-time signal.
        '''

        if len(self) == 0 or len(sig) == 0:
            empty_conv = DiscreteTimeSignal()

            return empty_conv

        # minimum value of n for convolution computation
        conv_min_idx = self.min_idx + sig.min_idx
        # maximum value of n for convolution computation
        conv_max_idx = self.max_idx + sig.max_idx

        # compute convolution
        conv = np.convolve(self.values(), sig.values())

        # create new discrete-time signal object using data
        data = ()
        for n in range(conv_min_idx, conv_max_idx + 1):
            data += ((n, conv[n - conv_min_idx]),)

        conv_signal = DiscreteTimeSignal(
            data,
            dtype=np.result_type(self.dtype, sig.dtype),
        )

        return conv_signal

    def __mul__(self, param):
        '''
        Compute scalar multiplication or discrete convolution, depending on
        parameter type.

        Parameters
        ----------
        param : float or DiscreteTimeSignal
            Given scalar value or discrete-time signal.

        Returns
        -------
        DiscreteTimeSignal
            Resulting discrete-time signal.
        '''

        # scalar multiplication if scalar
        if np.isscalar(param):
            return self.scalar_mul(param)
        # convolution if discrete-time signal
        elif isinstance(param, DiscreteTimeSignal):
            return self.conv(param)
        # TypeError otherwise
        else:
            err_msg = f'Unknown type {type(param)}.'
            err_msg += 'Use scalar for scalar multiplication '
            err_msg += 'or DiscreteTimeSignal object for convolution'

            raise TypeError(err_msg)

    def __rmul__(self, param):
        '''
        Compute scalar multiplication or discrete convolution, depending on
        parameter type (reverse method).

        Parameters
        ----------
        param : float or DiscreteTimeSignal
            Given scalar value or discrete-time signal.

        Returns
        -------
        DiscreteTimeSignal object
            Resulting discrete-time signal.
        '''

        return self.__mul__(param)
