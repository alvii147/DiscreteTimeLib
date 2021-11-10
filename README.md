# DiscreteTimeLib

**DiscreteTimeLib** is a Python library for the analysis of discrete-time signals and systems.

## Getting Started

Model a discrete-time signal:

```python
from DiscreteTimeLib import DiscreteTimeSignal

if __name__ == '__main__':
    data = (
        (-2, 1),
        (-1, 1.5),
        (0, 2),
        (1, 5),
    )
    sig = DiscreteTimeSignal(data)

    print(sig)
```

```
    x[n]
-2   1.0
-1   1.5
 0   2.0
 1   5.0
```

