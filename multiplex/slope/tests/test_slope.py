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
        - Hides the y-axis,
        - Moves the y-axis position, and
        - Adds two x-ticks.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope(5, 5, style_plot=True)
        self.assertFalse(viz.axes.spines['top'].get_visible())
        self.assertFalse(viz.axes.spines['right'].get_visible())
        self.assertEqual(('data', 1.1), viz.axes.spines['right'].get_position())
        self.assertTrue(viz.axes.spines['bottom'].get_visible())
        self.assertEqual((0, 1), viz.axes.spines['bottom'].get_bounds())
        self.assertFalse(viz.axes.spines['left'].get_visible())
        self.assertEqual(('data', -0.1), viz.axes.spines['left'].get_position())
        self.assertEqual((-0.1, 1.1), viz.get_xlim())
        self.assertEqual([ 0, 1 ], list(viz.get_xticks()))
        self.assertEqual([ ], list(viz.get_yticks()))

    @MultiplexTest.temporary_plot
    def test_draw_style_plot_plot(self):
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
    def test_draw_style_plot_secondary_axes(self):
        """
        Test that when drawing a slope graph, the visualization's secondary axes is created.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertEqual(viz.axes, viz.secondary)
        viz.draw_slope(0, 0, style_plot=True)
        self.assertFalse(viz.axes == viz.secondary)

    @MultiplexTest.temporary_plot
    def test_draw_style_plot_secondary_axes_too(self):
        """
        Test that when setting the style, the following changes are made to the secondary axes:

        - Removes the grid,
        - Hides the x-axis
        - Hides the y-axis,
        - Moves the y-axis position, and
        - Adds two x-ticks.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope(5, 5, style_plot=True)
        self.assertFalse(viz.secondary.spines['top'].get_visible())
        self.assertFalse(viz.secondary.spines['right'].get_visible())
        self.assertEqual(('data', 1.1), viz.secondary.spines['right'].get_position())
        self.assertTrue(viz.secondary.spines['bottom'].get_visible())
        self.assertEqual((0, 1), viz.secondary.spines['bottom'].get_bounds())
        self.assertFalse(viz.secondary.spines['left'].get_visible())
        self.assertEqual(('data', -0.1), viz.secondary.spines['left'].get_position())
        self.assertEqual((-0.1, 1.1), viz.get_xlim())
        self.assertEqual([ 0, 1 ], list(viz.get_xticks()))
        self.assertEqual([ ], list(viz.get_yticks()))

    @MultiplexTest.temporary_plot
    def test_draw_style_plot_first_time_only(self):
        """
        Test that the default style is set only the first time.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.set_xlim((-10, 10))
        viz.draw_slope(0, 0, style_plot=True)
        self.assertEqual((-0.1, 1.1), viz.get_xlim()) # the first time, the x-limit should change

        viz.set_xlim((-10, 10))
        viz.draw_slope(1, 1, style_plot=True)
        self.assertEqual((-10, 10), viz.get_xlim()) # the second time, the x-limit should not change

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

    @MultiplexTest.temporary_plot
    def test_draw_unequal_y1_y2(self):
        """
        Test that when ``y1`` and ``y2`` are lists of unequal length, the function raises a ValueError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertRaises(ValueError, viz.draw_slope, [ 0, 1 ], [ 1 ])

    @MultiplexTest.temporary_plot
    def test_draw_unequal_y1_y2_different_types(self):
        """
        Test that when ``y1`` and ``y2`` have unequal lengths, but they have different types, the function raises a ValueError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertRaises(ValueError, viz.draw_slope, [ 0, 1 ], 1)
        self.assertRaises(ValueError, viz.draw_slope, 1, [ 0, 1 ])

    @MultiplexTest.temporary_plot
    def test_draw_list_return_all(self):
        """
        Test that when providing a list of slopes, all of them are returned.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        y1, y2 = range(0, 5), range(5, 0, -1)
        lines = viz.draw_slope(y1, y2)[0]
        self.assertEqual(5, len(lines))

    @MultiplexTest.temporary_plot
    def test_draw_list_correct_positions(self):
        """
        Test that when providing a list of slopes, the correct positions are drawn.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        y1, y2 = range(0, 5), range(5, 0, -1)
        lines = viz.draw_slope(y1, y2)[0]
        self.assertEqual(5, len(lines))
        for line, (_y1, _y2) in zip(lines, zip(y1, y2)):
            self.assertEqual((0, _y1), tuple(line.get_path().vertices[0]))
            self.assertEqual((1, _y2), tuple(line.get_path().vertices[1]))
