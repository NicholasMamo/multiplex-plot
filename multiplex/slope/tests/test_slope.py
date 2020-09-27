"""
Unit tests for the :class:`~slope.slope.Slope` class.
"""

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
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
        self.assertEqual(tuple, type(viz.draw_slope(5, 5, )))

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
        viz.draw_slope(5, 5, style_plot=True)
        self.assertFalse(viz.axes.spines['top'].get_visible())
        self.assertFalse(viz.axes.spines['right'].get_visible())
        self.assertTrue(viz.axes.spines['bottom'].get_visible())
        self.assertEqual((0, 1), viz.axes.spines['bottom'].get_bounds())
        self.assertFalse(viz.axes.spines['left'].get_visible())
        self.assertEqual((-1, 2), viz.get_xlim())
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
        viz.draw_slope(0, 0, style_plot=False)
        self.assertTrue(viz.axes.spines['top'].get_visible())
        self.assertTrue(viz.axes.spines['right'].get_visible())
        self.assertTrue(viz.axes.spines['bottom'].get_visible())
        self.assertTrue(viz.axes.spines['left'].get_visible())
        self.assertEqual((-0.05, 1.05), viz.get_xlim())
        self.assertEqual([ -1/5, 0, 1/5, 2/5, 3/5, 4/5, 1, 6/5 ], [ round(tick, 2) for tick in viz.get_xticks() ])
        self.assertEqual([ -6/100, -4/100, -2/100, 0, 2/100, 4/100, 6/100 ], [ round(tick, 2) for tick in viz.get_yticks() ])

    @MultiplexTest.temporary_plot
    def test_draw_return_list_Line2D(self):
        """
        Test that when drawing a slope graph, the first return object is a list of Line2D.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        result = viz.draw_slope(0, 0, style_plot=False)
        self.assertEqual(tuple, type(result))
        self.assertTrue(len(result))
        self.assertEqual(list, type(result[0]))
        self.assertEqual(Line2D, type(result[0][0]))

    @MultiplexTest.temporary_plot
    def test_draw_correct_points(self):
        """
        Test that when drawing a slope graph, the lines start and end at the correct points.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        y1, y2 = 1, 5
        result = viz.draw_slope(y1, y2, style_plot=False)
        line = result[0][0]
        self.assertEqual(2, len(line.get_path().vertices))
        self.assertEqual((0, y1), tuple(line.get_path().vertices[0]))
        self.assertEqual((1, y2), tuple(line.get_path().vertices[1]))

    @MultiplexTest.temporary_plot
    def test_draw_points_unchanged(self):
        """
        Test that when drawing multiple slopes on the graph, all lines start and end at the correct points.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        y1, y2 = [ 1, 3 ], [ 5, 4 ]
        result = viz.draw_slope(y1[0], y2[0], style_plot=False)
        line = result[0][0]
        self.assertEqual(2, len(line.get_path().vertices))
        self.assertEqual((0, y1[0]), tuple(line.get_path().vertices[0]))
        self.assertEqual((1, y2[0]), tuple(line.get_path().vertices[1]))

        result = viz.draw_slope(y1[1], y2[1], style_plot=False)
        self.assertEqual(2, len(line.get_path().vertices)) # re-check the first line
        self.assertEqual((0, y1[0]), tuple(line.get_path().vertices[0]))
        self.assertEqual((1, y2[0]), tuple(line.get_path().vertices[1]))
        line = result[0][0] # check the second line
        self.assertEqual(2, len(line.get_path().vertices))
        self.assertEqual((0, y1[1]), tuple(line.get_path().vertices[0]))
        self.assertEqual((1, y2[1]), tuple(line.get_path().vertices[1]))
