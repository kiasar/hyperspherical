<div align="center">
  <img src="/Logo.png" alt="Hyperspherical Python Package" width="250"/>
</div>

# Hyperspherical
[![Downloads](https://static.pepy.tech/badge/Hyperspherical)](https://pepy.tech/project/Hyperspherical)
[![Downloads](https://static.pepy.tech/badge/Hyperspherical/month)](https://pepy.tech/project/Hyperspherical)

Hyperspherical is a Python package for converting between Cartesian and hyper-spherical (n-sphere) coordinates in any number of dimensions.
It also works for 2D cartesian and polar coordinates.

## Installation

You can install Hyperspherical using pip:

```
pip install hyperspherical
```

## Usage

Here's a basic example of how to use Hyperspherical:

```python
import numpy as np
from hyperspherical import cartesian2spherical, spherical2cartesian

# Convert Cartesian to spherical
cartesian_points = np.array([[1, 1, 1], [0, 1, 0], [1, 0, 0]])
spherical_points = cartesian2spherical(cartesian_points)
print(spherical_points)

# Convert spherical to Cartesian
cartesian_points_back = spherical2cartesian(spherical_points)
print(cartesian_points_back)
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
