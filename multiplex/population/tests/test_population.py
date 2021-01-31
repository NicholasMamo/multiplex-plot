"""
Unit tests for the :class:`~population.population.Population` class.
"""

import matplotlib
import matplotlib.pyplot as plt
import os
import sys

path = os.path.join(os.path.dirname(__file__), '..', '..')
if path not in sys.path:
    sys.path.insert(1, path)

from tests.test import MultiplexTest
from population.population import Population
import drawable
import util

class TestPopulation(MultiplexTest):
    """
    Unit tests for the :class:`~population.population.Population` class.
    """

    def test_draw_float_rows(self):
        """
        Test that when drawing with a floating point number of rows, the function raises a TypeError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertRaises(TypeError, viz.draw_population, 5, 1.2)

    def test_draw_negative_rows(self):
        """
        Test that when drawing with a negative number of rows, the function raises a ValueError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertRaises(ValueError, viz.draw_population, 5, -1)

    def test_draw_zero_rows(self):
        """
        Test that when drawing with no rows, the function raises a ValueError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertRaises(ValueError, viz.draw_population, 5, 0)

    def test_draw_float_population(self):
        """
        Test that when drawing with a floating point population, the function raises a TypeError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertRaises(TypeError, viz.draw_population, 2.4, 10)

    def test_draw_negative_population(self):
        """
        Test that when drawing with a negative population, the function raises a ValueError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertRaises(ValueError, viz.draw_population, -5, 10)

    def test_draw_zero_population(self):
        """
        Test that when drawing an empty population, the function returns an empty list of points.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertEqual([ ], viz.draw_population(0, 10))

    def test_gap_size_float_rows(self):
        """
        Test that when getting the gap size and the number of rows is a float, the function raises a TypeError.
        """

        viz = Population(drawable.Drawable)
        self.assertRaises(TypeError, viz._gap_size, (0, 1), 1.2)

    def test_gap_size_negative_rows(self):
        """
        Test that when getting the gap size and the number of rows is a negative integer, the function raises a ValueError.
        """

        viz = Population(drawable.Drawable)
        self.assertRaises(ValueError, viz._gap_size, (0, 1), -1)

    def test_gap_size_zero_rows(self):
        """
        Test that when getting the gap size and the number of rows is zero, the function raises a ValueError.
        """

        viz = Population(drawable.Drawable)
        self.assertRaises(ValueError, viz._gap_size, (0, 1), 0)

    def test_gap_size_one_row(self):
        """
        Test that that the gap size of one row is 0.
        """

        viz = Population(drawable.Drawable)
        self.assertEqual(0, viz._gap_size((0, 1), 1))

    def test_gap_size_two_rows(self):
        """
        Test that that the gap size of two rows is equivalent to the gap between the limits.
        """

        viz = Population(drawable.Drawable)

        lim = (0, 1)
        self.assertEqual(lim[1] - lim[0], viz._gap_size(lim, 2))

        lim = (0.2, 0.8)
        self.assertEqual(lim[1] - lim[0], viz._gap_size(lim, 2))

    def test_gap_size_multiple_rows(self):
        """
        Test that that the gap size of multiple rows fills the space between the limits.
        """

        viz = Population(drawable.Drawable)

        lim, rows = (0, 1), 4
        self.assertEqual(lim[1], lim[0] + viz._gap_size(lim, rows) * (rows - 1))

        lim, rows = (0.2, 0.8), 5
        self.assertEqual(lim[1], lim[0] + viz._gap_size(lim, rows) * (rows - 1))
