import numpy as np
import random

from DiscreteTimeLib import DiscreteTimeSignal

def generate_random_scalar(
    values_range=(-100, 100),
):
    return random.uniform(*values_range)

def generate_random_dts(
    num_values_range=(10, 100),
    start_idx_range=(-100, 100),
    values_range=(-1000.0, 1000.0),
    gap_probability=0.3,
):
    num_values = random.randint(*num_values_range)
    start_idx = random.randint(*start_idx_range)

    data = ()
    for n in range(start_idx, start_idx + num_values):
        if random.random() > gap_probability:
            data += ((n, np.float64(random.uniform(*values_range))),)

    x_n = DiscreteTimeSignal(data)

    return x_n, data

def generate_random_system(
    b_len_range=(2, 5),
    a_len_range=(2, 5),
    values_range=(-100, 100),
):
    b_len = random.randint(*b_len_range)
    a_len = random.randint(*a_len_range)

    b = np.random.rand(b_len) * (values_range[1] - values_range[0])
    b += values_range[0]
    a = np.random.rand(a_len) * (values_range[1] - values_range[0])
    a += values_range[0]

    return b, a