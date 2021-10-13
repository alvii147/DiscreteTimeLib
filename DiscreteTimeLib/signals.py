import numpy as np
import pandas as pd

class DiscreteTimeSignal:
    '''
    Discrete-time signal object implemented with digital signal processing
    functions.
    '''

    def __init__(self, data=()):
        '''
        Initializer for discrete-time signal object.

        Parameters
        ----------
        *data : numpy.ndarray
            Two-dimensional array-like representing signal data.

            For e.g., `((0, 2), (1, 4))` indicates `x[0] = 2` and `x[1] = 4`
        '''

        data_shape = np.shape(data)

        # raise error if data is not of shape (_, 2, ...)
        if data_shape[0] > 0 and (len(data_shape) < 2 or data_shape[1] != 2):
            raise ValueError('data must consist of key-value pairs')

        # discrete signal indices
        keys = np.zeros(data_shape[0], dtype=np.int64)
        # discrete signal values
        values = np.zeros(data_shape[0], dtype=np.float64)
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

    def __str__(self): # pragma: no cover
        '''
        String representation of object.

        Returns
        -------
        signal_string : str
        '''

        return str(self.signal)

    def length(self):
        '''
        Get length of signal.

        Returns
        -------
        length : int
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
        value : float
        '''

        try:
            return self.signal.loc[key]['x[n]']
        except KeyError:
            return 0.0

    def __mul__(self, sig):
        '''
        Compute discrete convolution between this and given discrete-time
        signal objects.

        Parameters
        ----------
        sig : DiscreteTimeSignal
            Given discrete-time signal

        Returns
        -------
        conv : DiscreteTimeSignal
            Discrete convolution discrete-time signal object.
        '''

        if self.length() == 0 or sig.length() == 0:
            empty_conv = DiscreteTimeSignal()

            return empty_conv

        # minimum value of n for convolution computation
        conv_min_idx = self.min_idx + sig.min_idx
        # maximum value of n for convolution computation
        conv_max_idx = self.max_idx + sig.max_idx

        # compute convolution
        data = ()
        idx = 0
        for n in range(conv_min_idx, conv_max_idx + 1):
            conv_sum = 0
            for k in range(self.min_idx, self.max_idx + 1):
                conv_sum += self[k] * sig[n - k]

            data += ((n, conv_sum),)

            idx += 1

        # create new discrete-time signal object using data
        conv = DiscreteTimeSignal(data)

        return conv