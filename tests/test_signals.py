import pytest
import numpy as np
import numpy.testing as npt
import random

from .utils import generate_random_scalar, generate_random_dts
from DiscreteTimeLib import DiscreteTimeSignal

def test_DiscreteTimeSignal_init():
    x_n, data = generate_random_dts()

    assert len(x_n) == np.shape(data)[0]

    assert x_n[data[0][0] - 1] == 0

    for i in range(np.shape(data)[0]):
        npt.assert_almost_equal(x_n[data[i][0]], data[i][1])

def test_DiscreteTimeSignal_init_error_shape():
    dim1 = random.randint(1, 20)
    data = np.random.rand(dim1)

    with pytest.raises(ValueError):
        DiscreteTimeSignal(data)

    dim1 = random.randint(1, 20)
    dim2 = random.randint(3, 20)
    data = np.random.rand(dim1, dim2)

    with pytest.raises(ValueError):
        DiscreteTimeSignal(data)

def test_DiscreteTimeSignal_keys_values():
    x_n, data = generate_random_dts()

    keys = x_n.keys()
    values = x_n.values()

    n_keys = 0
    n_data = 0

    while n_keys < np.shape(keys)[0] and n_data < np.shape(data)[0]:
        if data[n_data][0] == keys[n_keys]:
            npt.assert_almost_equal(data[n_data][1], values[n_keys])
            n_data += 1

        n_keys += 1

    assert n_data == np.shape(data)[0]

def test_DiscreteTimeSignal_equality():
    x_n = DiscreteTimeSignal()
    y_n = DiscreteTimeSignal()

    assert x_n == y_n
    assert not x_n != y_n
    assert y_n == x_n
    assert not y_n != x_n

    _, data = generate_random_dts()

    x_n = DiscreteTimeSignal(data)
    y_n = DiscreteTimeSignal(data)

    assert x_n == y_n
    assert not x_n != y_n
    assert y_n == x_n
    assert not y_n != x_n

def test_DiscreteTimeSignal_inequality():
    _, data_y = generate_random_dts()

    x_n = DiscreteTimeSignal()
    y_n = DiscreteTimeSignal(data_y)

    assert x_n != y_n
    assert not x_n == y_n
    assert y_n != x_n
    assert not y_n == x_n

    _, data_x = generate_random_dts()
    data_y = data_x + data_y

    x_n = DiscreteTimeSignal(data_x)

    assert x_n != y_n
    assert not x_n == y_n
    assert y_n != x_n
    assert not y_n == x_n

def test_DiscreteTimeSignal_sum_empty():
    x_n = DiscreteTimeSignal()
    y_n, data_y = generate_random_dts()

    sum_signal = x_n + y_n
    assert sum_signal == y_n

    sum_signal = y_n + x_n
    assert sum_signal == y_n

    y_n = DiscreteTimeSignal()

    sum_signal = x_n + y_n
    assert len(sum_signal) == 0

@pytest.mark.parametrize('execution_id', range(10))
def test_DiscreteTimeSignal_sum(execution_id):
    x_n, data_x = generate_random_dts()
    y_n, data_y = generate_random_dts()

    sum_signal = x_n + y_n

    sum_min_idx = min(data_x[0][0], data_y[0][0])
    sum_max_idx = max(data_x[-1][0], data_y[-1][0])
    for n in range(sum_min_idx, sum_max_idx + 1):
        x_k = 0.0
        for i in range(np.shape(data_x)[0]):
            if data_x[i][0] == n:
                x_k = data_x[i][1]
                break

        y_k = 0.0
        for i in range(np.shape(data_y)[0]):
            if data_y[i][0] == n:
                y_k = data_y[i][1]
                break

        npt.assert_almost_equal(sum_signal[n], x_k + y_k)

def test_DiscreteTimeSignal_sub_empty():
    x_n = DiscreteTimeSignal()
    y_n, data_y = generate_random_dts()

    sub_signal = x_n - y_n
    assert sub_signal == -1 * y_n

    sub_signal = y_n - x_n
    assert sub_signal == y_n

    y_n = DiscreteTimeSignal()

    sub_signal = x_n - y_n
    assert len(sub_signal) == 0

@pytest.mark.parametrize('execution_id', range(10))
def test_DiscreteTimeSignal_sub(execution_id):
    x_n, data_x = generate_random_dts()
    y_n, data_y = generate_random_dts()

    sum_signal = x_n - y_n

    sum_min_idx = min(data_x[0][0], data_y[0][0])
    sum_max_idx = max(data_x[-1][0], data_y[-1][0])
    for n in range(sum_min_idx, sum_max_idx + 1):
        x_k = 0.0
        for i in range(np.shape(data_x)[0]):
            if data_x[i][0] == n:
                x_k = data_x[i][1]
                break

        y_k = 0.0
        for i in range(np.shape(data_y)[0]):
            if data_y[i][0] == n:
                y_k = data_y[i][1]
                break

        npt.assert_almost_equal(sum_signal[n], x_k - y_k)

def test_DiscreteTimeSignal_mul_error_type():
    x_n, data_x = generate_random_dts()
    multiplier = np.zeros((4, 4))

    with pytest.raises(TypeError):
        x_n * multiplier

@pytest.mark.parametrize('execution_id', range(10))
def test_DiscreteTimeSignal_scalar_mul(execution_id):
    x_n, data_x = generate_random_dts()
    scalar = generate_random_scalar()

    scaled_signal = x_n * scalar

    for n in range(data_x[0][0], data_x[-1][0] + 1):
        npt.assert_almost_equal(scaled_signal[n], x_n[n] * scalar)

    scaled_signal = scalar * x_n

    for n in range(data_x[0][0], data_x[-1][0] + 1):
        npt.assert_almost_equal(scaled_signal[n], x_n[n] * scalar)

def test_DiscreteTimeSignal_conv_empty():
    x_n = DiscreteTimeSignal()
    h_n, data_h = generate_random_dts()

    conv = x_n * h_n

    assert len(conv) == 0

@pytest.mark.parametrize('execution_id', range(10))
def test_DiscreteTimeSignal_conv(execution_id):
    x_n, data_x = generate_random_dts()
    h_n, data_h = generate_random_dts()

    conv_signal = x_n * h_n

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

        npt.assert_almost_equal(conv_signal[n], conv_sum)