"""
Unit tests for the :class:`~slope.slope.Slope` class.
"""

import matplotlib.pyplot as plt
import os
import pandas as pd
import sys

path = os.path.join(os.path.dirname(__file__), '..', '..')
if path not in sys.path:
    sys.path.insert(1, path)

from tests.test import MultiplexTest
import drawable
import util

class TestSlope(MultiplexTest):
    """
    Unit tests for the :class:`~slope.slope.Slope` class.
    """

    @MultiplexTest.temporary_plot
    def test_draw_returns_tuple(self):
        """
        Test that when drawing a slope graph, it always returns a tuple.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertEqual(tuple, type(viz.draw_slope()))

    @MultiplexTest.temporary_plot
    def test_draw_with_style_plot(self):
        """
        Test that when setting the style, the following changes are made:

        - Removes the grid,
        - Hides the x-axis
        - Hides the y-axis, and
        - Adds two x-ticks.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope(style_plot=True)
        self.assertFalse(viz.axes.spines['top'].get_visible())
        self.assertFalse(viz.axes.spines['right'].get_visible())
        self.assertFalse(viz.axes.spines['bottom'].get_visible())
        self.assertFalse(viz.axes.spines['left'].get_visible())
        self.assertEqual((-0.5, 1), viz.get_xlim())
        self.assertEqual([ 0, 1 ], list(viz.get_xticks()))
        self.assertEqual([ ], list(viz.get_yticks()))

    @MultiplexTest.temporary_plot
    def test_draw_default_style_plot(self):
        """
        Test that when not setting the style, none of the the following changes are made:

        - Removes the grid,
        - Hides the x-axis
        - Hides the y-axis, and
        - Adds two x-ticks.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope(style_plot=False)
        self.assertTrue(viz.axes.spines['top'].get_visible())
        self.assertTrue(viz.axes.spines['right'].get_visible())
        self.assertTrue(viz.axes.spines['bottom'].get_visible())
        self.assertTrue(viz.axes.spines['left'].get_visible())
        self.assertEqual((0, 1), viz.get_xlim())
        self.assertEqual([ 0, 1/5, 2/5, 3/5, 4/5, 1 ], [ round(tick, 1) for tick in viz.get_xticks() ])
        self.assertEqual([ 0, 1/5, 2/5, 3/5, 4/5, 1 ], [ round(tick, 1) for tick in viz.get_yticks() ])
