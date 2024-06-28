"""
Module to Convert Cartesian Coordinates to Spherical Coordinates and vice versa,
This module provides functionality to transform Cartesian coordinates into spherical coordinates.
"""

import numpy as np


def _cartesian2polar(points_2d: np.ndarray) -> np.ndarray:
    """
    Convert 2D Cartesian coordinates to polar coordinates.
    Convert the inputs in Cartesian in the form (x, y) to the Polar form of (r, θ).

    :param: points_2d (np.ndarray): An array of shape (number_of_points, 2).
                             Each row represents a point in 2D space (x, y).
    :return: np.ndarray: An array of shape (number_of_points, 2).
                  Each row contains the polar coordinates (r, theta) corresponding
                  to the input Cartesian coordinates.
    """
    # Check whether the inputs are an array of points.
    if len(points_2d.shape) != 2:
        raise ValueError(f"Expected input shape: (number_of_points, 2). Got {points_2d.shape} instead.")

    # Check whether the inputs are 2D points.
    if points_2d.shape[1] != 2:
        raise ValueError(f"Points must be 2D: (number_of_points, 2). Got {points_2d.shape[1]}D instead.")

    r = np.linalg.norm(points_2d, axis=1)
    theta = np.arctan2(points_2d[:, 1], points_2d[:, 0])
    return np.column_stack((r, theta))


def _cartesian2spherical_arrayed(points: np.ndarray) -> np.ndarray:
    """
    Convert Cartesian coordinates to spherical coordinates in a numpy array of points.
    Convert the inputs in Cartesian in the form (x1, x2, ..., x_n) to (r, θ1, θ2, ..., θ_(n-2), φ).
    The formula is the same as Wikipedia: https://en.wikipedia.org/wiki/N-sphere#Spherical_coordinates

    :param: points (np.ndarray): An array of shape (number_of_points, points_dimension).
                           Each row represents a point in 2D, 3D, 4D to upper spaces.
    :return: np.ndarray: An array of shape (number_of_points, points_dimension) where each row
                  represents the spherical coordinates of the corresponding point from the input.
    :raise: valueError: If the input isn't a 2D array.
    """

    # Check whether the inputs are an array of points.
    if len(points.shape) != 2:
        raise ValueError(f"Expected input shape: (number_of_points, points_dimension). Got {points.shape} instead.")

    # Handles 2D Cartesian coordinates to Polar coordinates in a different function.
    if points.shape[1] == 2:
        return _cartesian2polar(points)

    # Special handling for 3D Cartesian coordinates to reorder the columns for standard representation.
    if points.shape[1] == 3:
        points = points[:, [2, 0, 1]]

    # Radial distance
    r = np.linalg.norm(points, axis=1)

    # Calculate the rooted value of the cumulative sum array. In simple words, it is doing sqrt(x^2 + y^2 + z^2 + ....)
    rooted_sum_array = np.sqrt(np.cumsum((points ** 2)[:, ::-1], axis=1))[:, ::-1]

    # Update the last element to its actual value to handle negatives, since sqrt{x^2} yields |x|.
    rooted_sum_array[:, -1] = points[:, -1]

    # Remove the first value from `rooted_sum_array` and the last from `points` as they're unnecessary.
    rooted_sum_array = rooted_sum_array[:, 1:]
    shifted_points = points[:, :-1]

    # Add the second-last value of rooted_sum_array to the last column of shifted_points. Its standard formula for φ.
    shifted_points[:, -1] += rooted_sum_array[:, -2]

    spherical_point = np.arctan2(rooted_sum_array, shifted_points)
    spherical_point[:, -1] *= 2

    return np.column_stack((r, spherical_point))


def cartesian2spherical(points: np.ndarray) -> np.ndarray:
    """
    A more general function compared to `_cartesian2spherical_arrayed`.
    Handles different shape of the input. For more information on the function see `_cartesian2spherical_arrayed`.

    :param points: A singe or an array of shape (number_of_points, points_dimension).
                           Each row represents a point in 2D, 3D, 4D to upper spaces.
    :return: np.ndarray: Single point or an array of shape (number_of_points, points_dimension) where each row
                  represents the spherical coordinates of the corresponding point from the input.
    """
    points_float64 = points.astype(np.float64)

    if len(points.shape) == 1:
        if points.shape[0] < 2:
            raise ValueError(f"Got {points.shape} shape input, with the value {points}. Input should not be a number.")
        return _cartesian2spherical_arrayed(points_float64[np.newaxis, :])[0]
    elif len(points.shape) == 2:
        return _cartesian2spherical_arrayed(points_float64)
    else:
        raise ValueError(f"Got {points.shape} shape input. This input shape is not supported.")


def _spherical2cartesian_arrayed(points: np.ndarray) -> np.ndarray:
    """
    Convert spherical coordinates to Cartesian coordinates in a numpy array of points.
    Convert the inputs in Cartesian in the form (r, θ1, θ2, ..., θ_(n-2), φ) to (x1, x2, ..., x_n).
    The formula is the same as Wikipedia: https://en.wikipedia.org/wiki/N-sphere#Spherical_coordinates

    :param: points (np.ndarray): An array of shape (number_of_points, points_dimension).
                           Each row represents a point in 2D, 3D, 4D to upper spaces.
    :return: np.ndarray: An array of shape (number_of_points, points_dimension) where each row
                  represents the spherical coordinates of the corresponding point from the input.
    :raise: valueError: If the input isn't a 2D array.
    """

    # Check whether the inputs are an array of points.
    if len(points.shape) != 2:
        raise ValueError(f"Expected input shape: (number_of_points, points_dimension). Got {points.shape} instead.")

    dimension = points.shape[1]  # dimension of the points.
    r = points[:, 0]  # r = radius = distans of points from center.
    sin_vectors = np.sin(points[:, 1:])
    cos_vectors = np.cos(points[:, 1:])

    # Initialize a matrix to hold sine values for all angles. This matrix will be "lower triangular" in the next line.
    trig_transformed_matrix = np.tile(sin_vectors[:, np.newaxis, :], (1, dimension, 1))  # trig = triangular

    # Modify the upper triangle of the matrix to have ones, and keep the sine values in the lower triangle.
    trig_transformed_matrix = np.tril(trig_transformed_matrix) + np.triu(np.ones((dimension, dimension - 1)))

    # Replace the diagonal of the matrix with cosine values.
    diagonal_idx = np.arange(dimension - 1)
    trig_transformed_matrix[:, diagonal_idx, diagonal_idx] = cos_vectors

    # Compute the Cartesian coordinates by multiplying "r" and row-wise values.
    cartesian_points = np.prod(trig_transformed_matrix, axis=2) * r[:, np.newaxis]

    # Special handling for 3D Cartesian coordinates to reorder the columns for standard representation.
    if dimension == 3:
        cartesian_points = cartesian_points[:, [1, 2, 0]]

    return cartesian_points


def spherical2cartesian(points: np.ndarray) -> np.ndarray:
    """
    Handles different shape of the input. For more information on the function see `_spherical2cartesian_arrayed`.

    :param points: A singe or an array of shape (number_of_points, points_dimension).
                           Each row represents a point in 2D, 3D, 4D to upper spaces.
    :return: np.ndarray: Single point or an array of shape (number_of_points, points_dimension) where each row
                  represents the spherical coordinates of the corresponding point from the input.
    """
    points_float64 = points.astype(np.float64)

    if len(points.shape) == 1:
        if points.shape[0] < 2:
            raise ValueError(f"Got {points.shape} shape input, with the value {points}. Input should not be a number.")
        return _spherical2cartesian_arrayed(points_float64[np.newaxis, :])[0]
    elif len(points.shape) == 2:
        return _spherical2cartesian_arrayed(points_float64)
    else:
        raise ValueError(f"Got {points.shape} shape input. This input shape is not supported.")
