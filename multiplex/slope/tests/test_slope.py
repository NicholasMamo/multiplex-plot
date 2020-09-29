"""
Unit tests for the :class:`~slope.slope.Slope` class.
"""

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import os
import numpy as np
import sys

path = os.path.join(os.path.dirname(__file__), '..', '..')
if path not in sys.path:
    sys.path.insert(1, path)

from tests.test import MultiplexTest
from slope.slope import Slope
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
        self.assertEqual(list, type(viz.draw_slope(5, 5)))

    @MultiplexTest.temporary_plot
    def test_draw_int(self):
        """
        Test that slope graphs can be drawn using integers as the start and end points.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertTrue(viz.draw_slope(5, 5))

    @MultiplexTest.temporary_plot
    def test_draw_float(self):
        """
        Test that slope graphs can be drawn using floats as the start and end points.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertTrue(viz.draw_slope(4.5, 4.5))

    @MultiplexTest.temporary_plot
    def test_draw_number(self):
        """
        Test that slope graphs can be drawn using other types of numbers as the start and end points.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertTrue(viz.draw_slope(np.float64(3.14159), np.float64(3.14159)))

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

    @MultiplexTest.temporary_plot
    def test_draw_style_plot(self):
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
        self.assertEqual(list, type(result))
        self.assertTrue(len(result))
        self.assertEqual(Line2D, type(result[0]))

    @MultiplexTest.temporary_plot
    def test_draw_correct_points(self):
        """
        Test that when drawing a slope graph, the lines start and end at the correct points.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        y1, y2 = 1, 5
        result = viz.draw_slope(y1, y2, style_plot=False)
        line = result[0]
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
        line = result[0]
        self.assertEqual(2, len(line.get_path().vertices))
        self.assertEqual((0, y1[0]), tuple(line.get_path().vertices[0]))
        self.assertEqual((1, y2[0]), tuple(line.get_path().vertices[1]))

        result = viz.draw_slope(y1[1], y2[1], style_plot=False)
        self.assertEqual(2, len(line.get_path().vertices)) # re-check the first line
        self.assertEqual((0, y1[0]), tuple(line.get_path().vertices[0]))
        self.assertEqual((1, y2[0]), tuple(line.get_path().vertices[1]))
        line = result[0] # check the second line
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
        lines = viz.draw_slope(y1, y2)
        self.assertEqual(5, len(lines))

    @MultiplexTest.temporary_plot
    def test_draw_list_correct_positions(self):
        """
        Test that when providing a list of slopes, the correct positions are drawn.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        y1, y2 = range(0, 5), range(5, 0, -1)
        lines = viz.draw_slope(y1, y2)
        self.assertEqual(5, len(lines))
        for line, (_y1, _y2) in zip(lines, zip(y1, y2)):
            self.assertEqual((0, _y1), tuple(line.get_path().vertices[0]))
            self.assertEqual((1, _y2), tuple(line.get_path().vertices[1]))

    @MultiplexTest.temporary_plot
    def test_draw_list_correct_start(self):
        """
        Test that when providing a list of slopes, all of them start at the same position.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        y1, y2 = range(0, 5), range(5, 0, -1)
        lines = viz.draw_slope(y1, y2)
        self.assertTrue(all( line.get_path().vertices[0][0] == 0 for line in lines ))

    @MultiplexTest.temporary_plot
    def test_draw_list_correct_end(self):
        """
        Test that when providing a list of slopes, all of them end at the same position.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        y1, y2 = range(0, 5), range(5, 0, -1)
        lines = viz.draw_slope(y1, y2)
        self.assertTrue(all( line.get_path().vertices[1][0] == 1 for line in lines ))

    @MultiplexTest.temporary_plot
    def test_draw_max_ylim_primary(self):
        """
        Test that when drawing a slope graph, the maximum y-limits are copied properly when the primary axes has a higher y-limit.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 0, 10 ], [ 0, 1 ])
        self.assertEqual(viz.axes.get_ylim(), viz.secondary.get_ylim())
        self.assertEqual(10.5, viz.axes.get_ylim()[1])
        self.assertEqual(10.5, viz.secondary.get_ylim()[1])

    @MultiplexTest.temporary_plot
    def test_draw_max_ylim_secondary(self):
        """
        Test that when drawing a slope graph, the maximum y-limits are copied properly when the secondary axes has a higher y-limit.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 0, 1 ], [ 0, 10 ])
        self.assertEqual(viz.axes.get_ylim(), viz.secondary.get_ylim())
        self.assertEqual(10.5, viz.axes.get_ylim()[1])
        self.assertEqual(10.5, viz.secondary.get_ylim()[1])

    @MultiplexTest.temporary_plot
    def test_draw_min_ylim_primary(self):
        """
        Test that when drawing a slope graph, the minimum y-limits are copied properly when the primary axes has a higher y-limit.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ -10, 0 ], [ 0, 1 ])
        self.assertEqual(viz.axes.get_ylim(), viz.secondary.get_ylim())
        self.assertEqual(-10.55, viz.axes.get_ylim()[0])
        self.assertEqual(-10.55, viz.secondary.get_ylim()[0])

    @MultiplexTest.temporary_plot
    def test_draw_min_ylim_secondary(self):
        """
        Test that when drawing a slope graph, the minimum y-limits are copied properly when the secondary axes has a higher y-limit.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 0, 1 ], [ -10, 0 ])
        self.assertEqual(viz.axes.get_ylim(), viz.secondary.get_ylim())
        self.assertEqual(-10.55, viz.axes.get_ylim()[0])
        self.assertEqual(-10.55, viz.secondary.get_ylim()[0])

    @MultiplexTest.temporary_plot
    def test_draw_y1_ticks_None(self):
        """
        Test that when drawing ticks and setting the start ticks to ``None``, the start values are used as ticks.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 0, 5 ], [ -10, 3 ], y1_ticks=None)
        self.assertEqual([ 0, 5 ], list(viz.axes.get_yticks()))

    @MultiplexTest.temporary_plot
    def test_draw_y2_ticks_None(self):
        """
        Test that when drawing ticks and setting the end ticks to ``None``, the end values are used as ticks.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 0, 5 ], [ -10, 3 ], y2_ticks=None)
        self.assertEqual([ -10, 3 ], list(viz.secondary.get_yticks()))

    @MultiplexTest.temporary_plot
    def test_draw_y1_ticks_empty(self):
        """
        Test that when drawing ticks and setting the start ticks to an empty string, no ticks are added.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 0, 5 ], [ -10, 3 ], y1_ticks='')
        self.assertEqual([ ], list(viz.axes.get_yticks()))

    @MultiplexTest.temporary_plot
    def test_draw_y2_ticks_empty(self):
        """
        Test that when drawing ticks and setting the end ticks to an empty string, no ticks are added.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 0, 5 ], [ -10, 3 ], y2_ticks='')
        self.assertEqual([ ], list(viz.secondary.get_yticks()))

    @MultiplexTest.temporary_plot
    def test_draw_y1_ticks_unequal(self):
        """
        Test that when the number of start ticks is not equal to the number of slopes, the function raises a ValueError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertRaises(ValueError, viz.draw_slope, [ 0, 5 ], [ -10, 3 ], y1_ticks=[ 'label' ])

    @MultiplexTest.temporary_plot
    def test_draw_y2_ticks_unequal(self):
        """
        Test that when the number of end ticks is not equal to the number of slopes, the function raises a ValueError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertRaises(ValueError, viz.draw_slope, [ 0, 5 ], [ -10, 3 ], y1_ticks=[ 'label' ])

    @MultiplexTest.temporary_plot
    def test_draw_y1_ticks_string(self):
        """
        Test that when using a string for the start tick of one slope, it is added as a tick label.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope(5, 6, y1_ticks='label')
        self.assertEqual([ 'label' ], [ label.get_text() for label in viz.axes.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y2_ticks_string(self):
        """
        Test that when using a string for the end tick of one slope, it is added as a tick label.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope(5, 6, y2_ticks='label')
        self.assertEqual([ 'label' ], [ label.get_text() for label in viz.secondary.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y1_ticks_number(self):
        """
        Test that when using a number for the start tick of one slope, it is added as a label.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope(5, 6, y1_ticks=20)
        self.assertEqual([ '20' ], [ label.get_text() for label in viz.axes.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y2_ticks_number(self):
        """
        Test that when using a number for the end tick of one slope, it is added as a label.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope(5, 6, y2_ticks=20)
        self.assertEqual([ '20' ], [ label.get_text() for label in viz.secondary.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y1_ticks_list_of_string(self):
        """
        Test that when using a list of strings for the start tick of one slope, they are all added as tick labels.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y2_ticks=[ 'label 1', 'label 2' ])
        self.assertEqual([ 'label 1', 'label 2' ], [ label.get_text() for label in viz.secondary.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y2_ticks_list_of_string(self):
        """
        Test that when using a list of strings for the end tick of one slope, they are all added as tick labels.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y1_ticks=[ 'label 1', 'label 2' ])
        self.assertEqual([ 'label 1', 'label 2' ], [ label.get_text() for label in viz.axes.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y1_list_of_None(self):
        """
        Test that when drawing a slope graph and providing a list made up of `None` for the start ticks, the ticks become the values.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y1_ticks=[ None, None ])
        self.assertEqual([ f"{ tick }" for tick in viz.axes.get_yticks() ], [ label.get_text() for label in viz.axes.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y2_list_of_None(self):
        """
        Test that when drawing a slope graph and providing a list made up of `None` for the end ticks, the ticks become the values.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y2_ticks=[ None, None ])
        self.assertEqual([ f"{ tick }" for tick in viz.secondary.get_yticks() ], [ label.get_text() for label in viz.secondary.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y1_list_with_None(self):
        """
        Test that when drawing a slope graph and providing a list with a `None` value for the start ticks, it is replaced with the tick value.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y1_ticks=[ 'label', None ])
        self.assertEqual([ 'label', '5' ], [ label.get_text() for label in viz.axes.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y2_list_with_None(self):
        """
        Test that when drawing a slope graph and providing a list with a `None` value for the start ticks, it is replaced with the tick value.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y2_ticks=[ 'label', None ])
        self.assertEqual([ 'label', '4' ], [ label.get_text() for label in viz.secondary.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y1_None_overrides_tick(self):
        """
        Test that when drawing a slope graph and providing a list with a `None` value for the start ticks, it replaces any existing ticks.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y1_ticks=[ 'label', None ])
        self.assertEqual([ 'label', '5' ], [ label.get_text() for label in viz.axes.get_yticklabels() ])

        viz.draw_slope([ 3, 7 ], [ 2, 4 ], y1_ticks=[ None, None ])
        self.assertEqual([ '3', '5', '7' ], [ label.get_text() for label in viz.axes.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y2_None_overrides_tick(self):
        """
        Test that when drawing a slope graph and providing a list with a `None` value for the end ticks, it replaces any existing ticks.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y2_ticks=[ 'label', None ])
        self.assertEqual([ 'label', '4' ], [ label.get_text() for label in viz.secondary.get_yticklabels() ])

        viz.draw_slope([ 3, 7 ], [ 2, 6 ], y2_ticks=[ None, None ])
        self.assertEqual([ '2', '4', '6' ], [ label.get_text() for label in viz.secondary.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y1_list_of_empty_string(self):
        """
        Test that when drawing a slope graph and providing a list made up of empty strings for the start ticks, no ticks are added.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y1_ticks=[ '', '' ])
        self.assertEqual([ ], list(viz.axes.get_yticks()))
        self.assertEqual([ ], [ label.get_text() for label in viz.axes.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y2_list_of_empty_string(self):
        """
        Test that when drawing a slope graph and providing a list made up of empty strings for the end ticks, no ticks are added.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y2_ticks=[ '', '' ])
        self.assertEqual([ ], list(viz.secondary.get_yticks()))
        self.assertEqual([ ], [ label.get_text() for label in viz.secondary.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y1_list_with_empty_string(self):
        """
        Test that when drawing a slope graph and providing a list with an empty string value for the start ticks, no tick is added there.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y1_ticks=[ None, '' ])
        self.assertEqual([ 3 ], list(viz.axes.get_yticks()))
        self.assertEqual([ '3' ], [ label.get_text() for label in viz.axes.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y2_list_with_empty_string(self):
        """
        Test that when drawing a slope graph and providing a list with an empty string value for the end ticks, no tick is added there.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y2_ticks=[ None, '' ])
        self.assertEqual([ 2 ], list(viz.secondary.get_yticks()))
        self.assertEqual([ '2' ], [ label.get_text() for label in viz.secondary.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y1_empty_string_does_not_override_tick(self):
        """
        Test that when drawing a slope graph and providing a list with an empty string value for the start ticks, it does not replace any existing ticks.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y1_ticks=[ 'label', None ])
        self.assertEqual([ 'label', '5' ], [ label.get_text() for label in viz.axes.get_yticklabels() ])

        viz.draw_slope([ 3, 7 ], [ 2, 4 ], y1_ticks=[ '', None ])
        self.assertEqual([ 'label', '5', '7' ], [ label.get_text() for label in viz.axes.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y2_empty_string_does_not_override_tick(self):
        """
        Test that when drawing a slope graph and providing a list with an empty string value for the end ticks, it does not replace any existing ticks.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y2_ticks=[ 'label', None ])
        self.assertEqual([ 'label', '4' ], [ label.get_text() for label in viz.secondary.get_yticklabels() ])

        viz.draw_slope([ 3, 7 ], [ 2, 6 ], y2_ticks=[ '', None ])
        self.assertEqual([ 'label', '4', '6' ], [ label.get_text() for label in viz.secondary.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y1_tick_labels_at_ticks(self):
        """
        Test that the tick labels at the start of the slope are added to the correct position.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 5, 3 ], [ 2, 4 ], y1_ticks=[ 'label 1', 'label 2' ])
        self.assertEqual([ 3, 5 ], list(viz.axes.get_yticks()))
        self.assertEqual([ 'label 2', 'label 1' ], [ label.get_text() for label in viz.axes.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y2_tick_labels_at_ticks(self):
        """
        Test that the tick labels at the end of the slope are added to the correct position.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 5, 3 ], [ 4, 2 ], y2_ticks=[ 'label 1', 'label 2' ])
        self.assertEqual([ 2, 4 ], list(viz.secondary.get_yticks()))
        self.assertEqual([ 'label 2', 'label 1' ], [ label.get_text() for label in viz.secondary.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_adds_ticks(self):
        """
        Test that when drawing multiple slopes, the function adds more ticks and does not remove old ones.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope(3, 10)
        self.assertEqual([ 3 ], list(viz.axes.get_yticks()))
        self.assertEqual([ 10 ], list(viz.secondary.get_yticks()))

        viz.draw_slope(5, 8)
        self.assertEqual([ 3, 5 ], list(viz.axes.get_yticks()))
        self.assertEqual([ 8, 10 ], list(viz.secondary.get_yticks()))

    @MultiplexTest.temporary_plot
    def test_draw_same_ticks(self):
        """
        Test that when drawing multiple slopes, and there is overlap in ticks, the function keeps only one.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope(3, 10)
        self.assertEqual([ 3 ], list(viz.axes.get_yticks()))
        self.assertEqual([ 10 ], list(viz.secondary.get_yticks()))

        viz.draw_slope(3, 8)
        self.assertEqual([ 3 ], list(viz.axes.get_yticks()))
        self.assertEqual([ 8, 10 ], list(viz.secondary.get_yticks()))

    @MultiplexTest.temporary_plot
    def test_draw_overwrite_y1_tick_labels(self):
        """
        Test that when drawing multiple slopes with overlapping starting ticks, the function overwrites the tick labels.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 10, 15 ], y1_ticks=[ 'A', 'C' ])
        self.assertEqual([ 3, 5 ], list(viz.axes.get_yticks()))
        self.assertEqual([ 'A', 'C' ], [ label.get_text() for label in viz.axes.get_yticklabels() ])

        viz.draw_slope(3, 7, y1_ticks='B')
        self.assertEqual([ 3, 5 ], list(viz.axes.get_yticks()))
        self.assertEqual([ 'B', 'C' ], [ label.get_text() for label in viz.axes.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_overwrite_y2_tick_labels(self):
        """
        Test that when drawing multiple slopes with overlapping ending ticks, the function overwrites the tick labels.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 6, 5 ], [ 10, 15 ], y2_ticks=[ 'A', 'C' ])
        self.assertEqual([ 10, 15 ], list(viz.secondary.get_yticks()))
        self.assertEqual([ 'A', 'C' ], [ label.get_text() for label in viz.secondary.get_yticklabels() ])

        viz.draw_slope(3, 10, y2_ticks='B')
        self.assertEqual([ 10, 15 ], list(viz.secondary.get_yticks()))
        self.assertEqual([ 'B', 'C' ], [ label.get_text() for label in viz.secondary.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_add_ticks_unknown_where(self):
        """
        Test that when the ``where`` parameter is not 'left' or 'right', the function raises a ValueError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        self.assertRaises(ValueError, slope._add_ticks, range(0, 5), None, where='lef')

    @MultiplexTest.temporary_plot
    def test_add_ticks_where_case_insensitive(self):
        """
        Test that the ``where`` parameter is case insensitive.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        self.assertEqual(None, slope._add_ticks(range(0, 5), None, where='LEFT'))
        self.assertEqual(None, slope._add_ticks(range(0, 5), None, where='RIGHT'))
