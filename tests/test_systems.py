import pytest
import numpy as np
import numpy.testing as npt

from DiscreteTimeLib import DiscreteTimeSystem
from DiscreteTimeLib.signals import DiscreteTimeSignal

from .utils import generate_random_system, generate_random_dts

def test_DiscreteTimeSystem_init():
    b, a = generate_random_system()
    DiscreteTimeSystem(b, a)

def test_DiscreteTimeSystem_init_error_shape():
    b, a = generate_random_system()
    with pytest.raises(ValueError):
        DiscreteTimeSystem([], a)

    b, a = generate_random_system()
    with pytest.raises(ValueError):
        DiscreteTimeSystem(b, [])

    b, a = generate_random_system()
    with pytest.raises(ValueError):
        DiscreteTimeSystem([[1, 2], [3, 4]], a)

    b, a = generate_random_system()
    with pytest.raises(ValueError):
        DiscreteTimeSystem(b, [[1, 2], [3, 4]])

@pytest.mark.parametrize(
    'b, a, z, expected_val',
    [
        [(0, 1), (1, -1), 2, 1],
        [(0, 1), (1, -1), 1 - 2j, 0.5j],
        [(1, 2, 4, 6), (1, -1, 2, -3, 5), -1, -0.25],
        [(1, 2, 4, 6), (1, -1, 2, -3, 5), -1 + 1j, (-6 - 10j) / 17],
    ]
)
def test_DiscreteTimeSystem_eval(b, a, z, expected_val):
    H = DiscreteTimeSystem(b, a)
    computed_val = H.eval(z)

    npt.assert_allclose(computed_val, expected_val)

@pytest.mark.parametrize('execution_id', range(10))
def test_DiscreteTimeSystem_filter(execution_id):
    b, a = generate_random_system()
    x_n, data_x = generate_random_dts()

    H = DiscreteTimeSystem(b, a)
    y_n = H.filter(x_n)

    for n in range(y_n.min_idx, y_n.max_idx + 1):
        y_expected = 0
        for i in range(np.shape(b)[0]):
            y_expected += b[i] * x_n[n - i]

        for i in range(1, np.shape(a)[0]):
            y_expected -= a[i] * y_n[n - i]

        y_expected = y_expected / a[0]

        npt.assert_allclose(y_n[n], y_expected)

def test_DiscreteTimeSystem_impz_error():
    b, a = generate_random_system()
    n_range = (16,)

    H = DiscreteTimeSystem(b, a)
    with pytest.raises(ValueError):
        H.impz(n_range=n_range)

@pytest.mark.parametrize(
    'b, a, h, n_range',
    [
        [(1,), (1,), (1, 0, 0, 0), (0, 4)],
        [(0, 1), (1, -2), (0, 1, 2, 4), (0, 4)],
        [(1,), (1, -2, 10), (1, 2, -6, -32), (0, 4)],
    ],
)
def test_DiscreteTimeSystem_impz(b, a, h, n_range):
    H = DiscreteTimeSystem(b, a)
    h_n_computed = H.impz(n_range=n_range)

    data = ()
    for n in range(*n_range):
        data += ((n, h[n]),)

    h_expected = DiscreteTimeSignal(data)

    assert h_n_computed == h_expected

def test_DiscreteTimeSystem_iztrans_impz():
    b, a = generate_random_system()
    n_range=(0, 10)

    H = DiscreteTimeSystem(b, a)
    h_exp, n = H.iztrans()
    h_n = H.impz(n_range=n_range)

    for i in range(*n_range):
        npt.assert_almost_equal(
            np.clongdouble(h_exp.subs(n, i)),
            np.clongdouble(h_n[i]),
        )

def test_DiscreteTimeSystem_freqz():
    b, a = generate_random_system()
    H = DiscreteTimeSystem(b, a)

    w_expected = np.linspace(-np.pi, np.pi, num=20)
    fr, w_samples = H.freqz((-np.pi, np.pi), num=20)

    npt.assert_allclose(w_samples, w_expected)