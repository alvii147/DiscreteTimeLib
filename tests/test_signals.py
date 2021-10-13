import pytest
import numpy as np
import numpy.testing as npt
import random

from DiscreteTimeLib import DiscreteTimeSignal

EXECUTION_COUNT = 5

def generate_random_dts(
        num_values_range=(1, 10),
        start_idx_range=(-100, 100),
        values_range=(-1000.0, 1000.0),
    ):
    num_values = random.randint(*num_values_range)
    start_idx = random.randint(*start_idx_range)

    data = ()
    idx = 0
    for n in range(start_idx, start_idx + num_values):
        data += ((n, np.float64(random.uniform(*values_range))),)
        idx += 1

    x_n = DiscreteTimeSignal(data)

    return x_n, data

@pytest.mark.parametrize('execution_id', range(EXECUTION_COUNT))
def test_DiscreteTimeSignal_init(execution_id):
    x_n, data = generate_random_dts()

    assert x_n.length() == np.shape(data)[0]

    npt.assert_almost_equal(x_n[data[0][0] - 1], 0)

    for i in range(np.shape(data)[0]):
        npt.assert_almost_equal(x_n[data[i][0]], data[i][1])

@pytest.mark.parametrize('execution_id', range(EXECUTION_COUNT))
def test_DiscreteTimeSignal_init_error_shape(execution_id):
    dim1 = random.randint(1, 20)
    data = np.random.rand(dim1)

    with pytest.raises(ValueError):
        x_n = DiscreteTimeSignal(data)

    dim1 = random.randint(1, 20)
    dim2 = random.randint(3, 20)
    data = np.random.rand(dim1, dim2)

    with pytest.raises(ValueError):
        x_n = DiscreteTimeSignal(data)

@pytest.mark.parametrize('execution_id', range(EXECUTION_COUNT))
def test_DiscreteTimeSignal_conv_empty(execution_id):
    x_n = DiscreteTimeSignal()
    h_n, data_h = generate_random_dts()

    conv = x_n * h_n

    assert x_n.length() == 0

@pytest.mark.parametrize('execution_id', range(EXECUTION_COUNT))
def test_DiscreteTimeSignal_conv(execution_id):
    x_n, data_x = generate_random_dts()
    h_n, data_h = generate_random_dts()

    conv = x_n * h_n

    conv_min_idx = data_x[0][0] + data_h[0][0]
    conv_max_idx = data_x[-1][0] + data_h[-1][0]
    for n in range(conv_min_idx, conv_max_idx + 1):
        conv_sum = 0
        for k in range(data_x[0][0], data_x[-1][0] + 1):
            x_k = 0
            for i in range(np.shape(data_x)[0]):
                if data_x[i][0] == k:
                    x_k = data_x[i][1]
                    break

                if data_x[i][0] > k:
                    break

            h_n_sub_k = 0
            for i in range(np.shape(data_h)[0]):
                if data_h[i][0] == n - k:
                    h_n_sub_k = data_h[i][1]
                    break

                if data_h[i][0] > n - k:
                    break

            conv_sum += x_k * h_n_sub_k

        npt.assert_almost_equal(conv[n], conv_sum)