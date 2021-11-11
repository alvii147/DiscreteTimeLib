import pytest
import numpy as np
import numpy.testing as npt
from DiscreteTimeLib import DiscreteTimeSystem

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