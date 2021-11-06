import pytest
import numpy as np
import numpy.testing as npt
from DiscreteTimeLib import DiscreteTimeSignal, DiscreteTimeSystem

from .utils import generate_random_system, generate_random_dts

def test_DiscreteTimeSystem_init():
    b, a = generate_random_system()
    H = DiscreteTimeSystem(b, a)

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