"""
Unit tests for the :class:`~slope.slope.Slope` class.
"""

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import os
import numpy as np
import pandas as pd
import sys

path = os.path.join(os.path.dirname(__file__), '..', '..')
if path not in sys.path:
    sys.path.insert(1, path)

from tests.test import MultiplexTest
from slope.slope import Slope
from text.annotation import Annotation
import drawable
import util

class TestSlope(MultiplexTest):
    """
    Unit tests for the :class:`~slope.slope.Slope` class.
    """

    @MultiplexTest.temporary_plot
    def test_init_empty_slopes(self):
        """
        That that when creating a new slope graph, the visualization creates an empty list of slopes.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        self.assertEqual([ ], slope.slopes)

    @MultiplexTest.temporary_plot
    def test_init_empty_labels(self):
        """
        That that when creating a new slope graph, the visualization creates an empty list of labels on both sides.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        self.assertEqual([ ], slope.llabels)
        self.assertEqual([ ], slope.rlabels)

    @MultiplexTest.temporary_plot
    def test_draw_returns_tuple(self):
        """
        Test that when drawing a slope graph, it always returns a tuple.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertEqual(tuple, type(viz.draw_slope(5, 5)))

    @MultiplexTest.temporary_plot
    def test_draw_saves_slopes(self):
        """
        Test that when drawing, the slopes are saved in the ``slopes`` variable.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        self.assertEqual([ ], slope.slopes)

        slopes, _, _ = slope.draw(5, 5)
        self.assertEqual(slopes, slope.slopes)

    @MultiplexTest.temporary_plot
    def test_draw_saves_multiple_slopes(self):
        """
        Test that when drawing multiple slopes at a time, the slopes are saved in the ``slopes`` variable.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        self.assertEqual([ ], slope.slopes)

        slopes, _, _ = slope.draw([ 0, 5 ], [ 5, 0 ])
        self.assertEqual(2, len(slopes))
        self.assertEqual(slopes, slope.slopes)

    @MultiplexTest.temporary_plot
    def test_draw_repeated_saves_slopes(self):
        """
        Test that when drawing slopes several times, they are all saved in the ``slopes`` variable.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        self.assertEqual([ ], slope.slopes)

        slopes, _, _ = slope.draw([ 0, 5 ], [ 5, 0 ])
        self.assertEqual(2, len(slopes))
        self.assertEqual(slopes, slope.slopes)

        # draw more slopes
        new_slopes, _, _ = slope.draw([ 2, 3 ], [ 3, 2 ])
        self.assertEqual(2, len(new_slopes))
        self.assertEqual(slopes + new_slopes, slope.slopes)

    @MultiplexTest.temporary_plot
    def test_draw_saves_labels(self):
        """
        Test that when drawing, the slopes are saved in the ``llabels`` and ``rlabels`` variables.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        self.assertEqual([ ], slope.slopes)

        _, llabels, rlabels = slope.draw(5, 5, label='A')
        self.assertEqual(1, len(slope.llabels))
        self.assertEqual(1, len(slope.rlabels))
        self.assertEqual(llabels, slope.llabels)
        self.assertEqual(rlabels, slope.rlabels)

    @MultiplexTest.temporary_plot
    def test_draw_saves_multiple_labels(self):
        """
        Test that when drawing multiple slopes at a time, the slopes are saved in the ``llabels`` and ``rlabels`` variables.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        self.assertEqual([ ], slope.slopes)

        _, llabels, rlabels = slope.draw([ 0, 5 ], [ 5, 0 ], label=[ 'A', 'B' ])
        self.assertEqual(2, len(slope.llabels))
        self.assertEqual(2, len(slope.llabels))
        self.assertEqual(llabels, slope.llabels)
        self.assertEqual(rlabels, slope.rlabels)

    @MultiplexTest.temporary_plot
    def test_draw_repeated_saves_labels(self):
        """
        Test that when drawing slopes several times, they are all saved in the ``llabels`` and ``rlabels`` variables.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        self.assertEqual([ ], slope.slopes)

        _, llabels, rlabels = slope.draw([ 0, 5 ], [ 5, 0 ], label=[ 'A', 'B' ])
        self.assertEqual(2, len(llabels))
        self.assertEqual(2, len(rlabels))
        self.assertEqual(llabels, slope.llabels)
        self.assertEqual(rlabels, slope.rlabels)

        # draw more slopes
        _, new_llabels, new_rlabels = slope.draw([ 2, 3 ], [ 3, 2 ], label=[ 'C', 'D' ])
        self.assertEqual(2, len(new_llabels))
        self.assertEqual(2, len(new_rlabels))
        self.assertEqual(llabels + new_llabels, slope.llabels)
        self.assertEqual(rlabels + new_rlabels, slope.rlabels)

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
        self.assertEqual(-0.1, round(viz.get_xlim()[0], 1)) # round because of the fitting
        self.assertEqual(1.1, round(viz.get_xlim()[1], 1)) # round because of the fitting
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
        self.assertEqual(-0.1, round(viz.get_xlim()[0], 1)) # round because of the fitting
        self.assertEqual(1.1, round(viz.get_xlim()[1], 1)) # round because of the fitting
        self.assertEqual([ 0, 1 ], list(viz.get_xticks()))

    @MultiplexTest.temporary_plot
    def test_draw_style_plot_first_time_only(self):
        """
        Test that the default style is set only the first time.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.set_xlim((-10, 10))
        viz.draw_slope(0, 0, style_plot=True)
        self.assertEqual(-0.1, round(viz.get_xlim()[0], 1)) # round because of the fitting
        self.assertEqual(1.1, round(viz.get_xlim()[1], 1)) # round because of the fitting

        viz.set_xlim((-10, 10))
        viz.draw_slope(1, 1, style_plot=True)
        self.assertEqual((-10, 10), viz.get_xlim()) # the second time, the x-limit should not change

    @MultiplexTest.temporary_plot
    def test_draw_return_list_Line2D(self):
        """
        Test that when drawing a slope graph, the first return object is a list of Line2D.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        result = viz.draw_slope(0, 0, style_plot=False)[0]
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
        result = viz.draw_slope(y1, y2, style_plot=False)[0]
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
        result = viz.draw_slope(y1[0], y2[0], style_plot=False)[0]
        line = result[0]
        self.assertEqual(2, len(line.get_path().vertices))
        self.assertEqual((0, y1[0]), tuple(line.get_path().vertices[0]))
        self.assertEqual((1, y2[0]), tuple(line.get_path().vertices[1]))

        result = viz.draw_slope(y1[1], y2[1], style_plot=False)[0]
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

    @MultiplexTest.temporary_plot
    def test_draw_list_correct_start(self):
        """
        Test that when providing a list of slopes, all of them start at the same position.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        y1, y2 = range(0, 5), range(5, 0, -1)
        lines = viz.draw_slope(y1, y2)[0]
        self.assertTrue(all( line.get_path().vertices[0][0] == 0 for line in lines ))

    @MultiplexTest.temporary_plot
    def test_draw_list_correct_end(self):
        """
        Test that when providing a list of slopes, all of them end at the same position.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        y1, y2 = range(0, 5), range(5, 0, -1)
        lines = viz.draw_slope(y1, y2)[0]
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
    def test_draw_y1_tick_None(self):
        """
        Test that when drawing ticks and setting the start ticks to ``None``, the start values are used as ticks.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 0, 5 ], [ -10, 3 ], y1_tick=None)
        self.assertEqual([ 0, 5 ], list(viz.axes.get_yticks()))

    @MultiplexTest.temporary_plot
    def test_draw_y2_tick_None(self):
        """
        Test that when drawing ticks and setting the end ticks to ``None``, the end values are used as ticks.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 0, 5 ], [ -10, 3 ], y2_tick=None)
        self.assertEqual([ -10, 3 ], list(viz.secondary.get_yticks()))

    @MultiplexTest.temporary_plot
    def test_draw_y1_tick_empty(self):
        """
        Test that when drawing ticks and setting the start ticks to an empty string, no ticks are added.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 0, 5 ], [ -10, 3 ], y1_tick='')
        self.assertEqual([ ], list(viz.axes.get_yticks()))

    @MultiplexTest.temporary_plot
    def test_draw_y2_tick_empty(self):
        """
        Test that when drawing ticks and setting the end ticks to an empty string, no ticks are added.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 0, 5 ], [ -10, 3 ], y2_tick='')
        self.assertEqual([ ], list(viz.secondary.get_yticks()))

    @MultiplexTest.temporary_plot
    def test_draw_y1_tick_unequal(self):
        """
        Test that when the number of start ticks is not equal to the number of slopes, the function raises a ValueError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertRaises(ValueError, viz.draw_slope, [ 0, 5 ], [ -10, 3 ], y1_tick=[ 'label' ])

    @MultiplexTest.temporary_plot
    def test_draw_y2_tick_unequal(self):
        """
        Test that when the number of end ticks is not equal to the number of slopes, the function raises a ValueError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertRaises(ValueError, viz.draw_slope, [ 0, 5 ], [ -10, 3 ], y1_tick=[ 'label' ])

    @MultiplexTest.temporary_plot
    def test_draw_y1_tick_string(self):
        """
        Test that when using a string for the start tick of one slope, it is added as a tick label.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope(5, 6, y1_tick='label')
        self.assertEqual([ 'label' ], [ label.get_text() for label in viz.axes.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y2_tick_string(self):
        """
        Test that when using a string for the end tick of one slope, it is added as a tick label.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope(5, 6, y2_tick='label')
        self.assertEqual([ 'label' ], [ label.get_text() for label in viz.secondary.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y1_tick_number(self):
        """
        Test that when using a number for the start tick of one slope, it is added as a label.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope(5, 6, y1_tick=20)
        self.assertEqual([ '20' ], [ label.get_text() for label in viz.axes.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y2_tick_number(self):
        """
        Test that when using a number for the end tick of one slope, it is added as a label.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope(5, 6, y2_tick=20)
        self.assertEqual([ '20' ], [ label.get_text() for label in viz.secondary.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y1_tick_list_of_string(self):
        """
        Test that when using a list of strings for the start tick of one slope, they are all added as tick labels.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y1_tick=[ 'label 1', 'label 2' ])
        self.assertEqual([ 'label 1', 'label 2' ], [ label.get_text() for label in viz.axes.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y2_tick_list_of_string(self):
        """
        Test that when using a list of strings for the end tick of one slope, they are all added as tick labels.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y2_tick=[ 'label 1', 'label 2' ])
        self.assertEqual([ 'label 1', 'label 2' ], [ label.get_text() for label in viz.secondary.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y1_tick_series(self):
        """
        Test that when using a list of strings for the start tick of one slope, they are all added as tick labels.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y1_tick=pd.Series([ 'label 1', 'label 2' ]))
        self.assertEqual([ 'label 1', 'label 2' ], [ label.get_text() for label in viz.axes.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y2_tick_series(self):
        """
        Test that when using a list of strings for the end tick of one slope, they are all added as tick labels.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y2_tick=pd.Series([ 'label 1', 'label 2' ]))
        self.assertEqual([ 'label 1', 'label 2' ], [ label.get_text() for label in viz.secondary.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y1_list_of_None(self):
        """
        Test that when drawing a slope graph and providing a list made up of `None` for the start ticks, the ticks become the values.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y1_tick=[ None, None ])
        self.assertEqual([ f"{ tick }" for tick in viz.axes.get_yticks() ], [ label.get_text() for label in viz.axes.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y2_list_of_None(self):
        """
        Test that when drawing a slope graph and providing a list made up of `None` for the end ticks, the ticks become the values.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y2_tick=[ None, None ])
        self.assertEqual([ f"{ tick }" for tick in viz.secondary.get_yticks() ], [ label.get_text() for label in viz.secondary.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y1_list_with_None(self):
        """
        Test that when drawing a slope graph and providing a list with a `None` value for the start ticks, it is replaced with the tick value.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y1_tick=[ 'label', None ])
        self.assertEqual([ 'label', '5' ], [ label.get_text() for label in viz.axes.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y2_list_with_None(self):
        """
        Test that when drawing a slope graph and providing a list with a `None` value for the start ticks, it is replaced with the tick value.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y2_tick=[ 'label', None ])
        self.assertEqual([ 'label', '4' ], [ label.get_text() for label in viz.secondary.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y1_None_overrides_tick(self):
        """
        Test that when drawing a slope graph and providing a list with a `None` value for the start ticks, it replaces any existing ticks.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y1_tick=[ 'label', None ])
        self.assertEqual([ 'label', '5' ], [ label.get_text() for label in viz.axes.get_yticklabels() ])

        viz.draw_slope([ 3, 7 ], [ 2, 4 ], y1_tick=[ None, None ])
        self.assertEqual([ '3', '5', '7' ], [ label.get_text() for label in viz.axes.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y2_None_overrides_tick(self):
        """
        Test that when drawing a slope graph and providing a list with a `None` value for the end ticks, it replaces any existing ticks.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y2_tick=[ 'label', None ])
        self.assertEqual([ 'label', '4' ], [ label.get_text() for label in viz.secondary.get_yticklabels() ])

        viz.draw_slope([ 3, 7 ], [ 2, 6 ], y2_tick=[ None, None ])
        self.assertEqual([ '2', '4', '6' ], [ label.get_text() for label in viz.secondary.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y1_list_of_empty_string(self):
        """
        Test that when drawing a slope graph and providing a list made up of empty strings for the start ticks, no ticks are added.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y1_tick=[ '', '' ])
        self.assertEqual([ ], list(viz.axes.get_yticks()))
        self.assertEqual([ ], [ label.get_text() for label in viz.axes.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y2_list_of_empty_string(self):
        """
        Test that when drawing a slope graph and providing a list made up of empty strings for the end ticks, no ticks are added.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y2_tick=[ '', '' ])
        self.assertEqual([ ], list(viz.secondary.get_yticks()))
        self.assertEqual([ ], [ label.get_text() for label in viz.secondary.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y1_list_with_empty_string(self):
        """
        Test that when drawing a slope graph and providing a list with an empty string value for the start ticks, no tick is added there.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y1_tick=[ None, '' ])
        self.assertEqual([ 3 ], list(viz.axes.get_yticks()))
        self.assertEqual([ '3' ], [ label.get_text() for label in viz.axes.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y2_list_with_empty_string(self):
        """
        Test that when drawing a slope graph and providing a list with an empty string value for the end ticks, no tick is added there.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y2_tick=[ None, '' ])
        self.assertEqual([ 2 ], list(viz.secondary.get_yticks()))
        self.assertEqual([ '2' ], [ label.get_text() for label in viz.secondary.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y1_empty_string_does_not_override_tick(self):
        """
        Test that when drawing a slope graph and providing a list with an empty string value for the start ticks, it does not replace any existing ticks.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y1_tick=[ 'label', None ])
        self.assertEqual([ 'label', '5' ], [ label.get_text() for label in viz.axes.get_yticklabels() ])

        viz.draw_slope([ 3, 7 ], [ 2, 4 ], y1_tick=[ '', None ])
        self.assertEqual([ 'label', '5', '7' ], [ label.get_text() for label in viz.axes.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y2_empty_string_does_not_override_tick(self):
        """
        Test that when drawing a slope graph and providing a list with an empty string value for the end ticks, it does not replace any existing ticks.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 3, 5 ], [ 2, 4 ], y2_tick=[ 'label', None ])
        self.assertEqual([ 'label', '4' ], [ label.get_text() for label in viz.secondary.get_yticklabels() ])

        viz.draw_slope([ 3, 7 ], [ 2, 6 ], y2_tick=[ '', None ])
        self.assertEqual([ 'label', '4', '6' ], [ label.get_text() for label in viz.secondary.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y1_tick_labels_at_ticks(self):
        """
        Test that the tick labels at the start of the slope are added to the correct position.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 5, 3 ], [ 2, 4 ], y1_tick=[ 'label 1', 'label 2' ])
        self.assertEqual([ 3, 5 ], list(viz.axes.get_yticks()))
        self.assertEqual([ 'label 2', 'label 1' ], [ label.get_text() for label in viz.axes.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_y2_tick_labels_at_ticks(self):
        """
        Test that the tick labels at the end of the slope are added to the correct position.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 5, 3 ], [ 4, 2 ], y2_tick=[ 'label 1', 'label 2' ])
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
        viz.draw_slope([ 3, 5 ], [ 10, 15 ], y1_tick=[ 'A', 'C' ])
        self.assertEqual([ 3, 5 ], list(viz.axes.get_yticks()))
        self.assertEqual([ 'A', 'C' ], [ label.get_text() for label in viz.axes.get_yticklabels() ])

        viz.draw_slope(3, 7, y1_tick='B')
        self.assertEqual([ 3, 5 ], list(viz.axes.get_yticks()))
        self.assertEqual([ 'B', 'C' ], [ label.get_text() for label in viz.axes.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_overwrite_y2_tick_labels(self):
        """
        Test that when drawing multiple slopes with overlapping ending ticks, the function overwrites the tick labels.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 6, 5 ], [ 10, 15 ], y2_tick=[ 'A', 'C' ])
        self.assertEqual([ 10, 15 ], list(viz.secondary.get_yticks()))
        self.assertEqual([ 'A', 'C' ], [ label.get_text() for label in viz.secondary.get_yticklabels() ])

        viz.draw_slope(3, 10, y2_tick='B')
        self.assertEqual([ 10, 15 ], list(viz.secondary.get_yticks()))
        self.assertEqual([ 'B', 'C' ], [ label.get_text() for label in viz.secondary.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_labels_none(self):
        """
        Test that when providing ``None`` as the labels, the visualization adds no labels.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 6, 5 ], [ 10, 15 ], label=None)
        self.assertEqual([ ], viz.slope.labels)

    @MultiplexTest.temporary_plot
    def test_draw_labels_empty(self):
        """
        Test that when providing an empty string as the labels, the visualization adds no labels.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 6, 5 ], [ 10, 15 ], label='')
        self.assertEqual([ ], viz.slope.labels)

    @MultiplexTest.temporary_plot
    def test_draw_labels_none(self):
        """
        Test that when providing ``None`` as the labels, the visualization adds no labels.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_slope([ 6, 5 ], [ 10, 15 ], label=None)
        self.assertEqual([ ], viz.slope.labels)

    @MultiplexTest.temporary_plot
    def test_draw_labels_unequal(self):
        """
        Test that when providing an unequal number of slopes and labels, the function raises a ValueError
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertRaises(ValueError, viz.draw_slope, [ 6, 5 ], [ 10, 15 ], label=[ ])
        self.assertRaises(ValueError, viz.draw_slope, [ 6, 5 ], [ 10, 15 ], label=[ 'A' ])
        self.assertTrue(viz.draw_slope([ 6, 5 ], [ 10, 15 ], label=[ 'A', 'B' ]))

    @MultiplexTest.temporary_plot
    def test_draw_return_all_labels(self):
        """
        Test that when drawing a plot, all labels are returned.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        _, llabels, rlabels = viz.draw_slope([ 6, 5 ], [ 10, 15 ], label=[ 'A', 'B' ])
        self.assertEqual(list, type(llabels))
        self.assertEqual(2, len(llabels))
        self.assertEqual(list, type(rlabels))
        self.assertEqual(2, len(rlabels))
        self.assertTrue(all( type(label) is Annotation for label in llabels ))
        self.assertTrue(all( type(label) is Annotation for label in rlabels ))

    @MultiplexTest.temporary_plot
    def test_draw_no_labels(self):
        """
        Test that when drawing a plot without labels, an empty list is returned.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        _, llabels, rlabels = viz.draw_slope([ 6, 5 ], [ 10, 15 ])
        self.assertEqual(list, type(llabels))
        self.assertEqual(list, type(rlabels))
        self.assertEqual(0, len(llabels))
        self.assertEqual(0, len(rlabels))

    @MultiplexTest.temporary_plot
    def test_draw_left_labels_correct_position(self):
        """
        Test that when drawing a plot the labels on the left are at the correct position.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        _, llabels, rlabels = viz.draw_slope([ 6, 1 ], [ 10, 15 ], label=[ 'A', 'B' ])
        self.assertEqual(2, len(llabels))

        self.assertEqual(6, llabels[0].y)
        self.assertEqual('A', llabels[0].annotation)
        self.assertEqual(1, llabels[1].y)
        self.assertEqual('B', llabels[1].annotation)

    @MultiplexTest.temporary_plot
    def test_draw_right_labels_correct_position(self):
        """
        Test that when drawing a plot the labels on the left are at the correct position.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        _, llabels, rlabels = viz.draw_slope([ 6, 1 ], [ 10, 15 ], label=[ 'A', 'B' ])
        self.assertEqual(2, len(llabels))
        self.assertEqual(2, len(rlabels))

        self.assertEqual(10, rlabels[0].y)
        self.assertEqual('A', rlabels[0].annotation)
        self.assertEqual(15, rlabels[1].y)
        self.assertEqual('B', rlabels[1].annotation)

    @MultiplexTest.temporary_plot
    def test_draw_labels_both_sides(self):
        """
        Test that when drawing labels on both sides, the labels actually tally up (there is one on the left and one on the right).
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        _, llabels, rlabels = viz.draw_slope([ 6, 1 ], [ 10, 15 ], label=[ 'A', 'B' ])
        self.assertEqual(2, len(llabels))
        self.assertEqual(2, len(rlabels))

        # left side
        self.assertEqual(6, llabels[0].y)
        self.assertEqual('A', llabels[0].annotation)
        self.assertEqual(1, llabels[1].y)
        self.assertEqual('B', llabels[1].annotation)

        # right side
        self.assertEqual(10, rlabels[0].y)
        self.assertEqual('A', rlabels[0].annotation)
        self.assertEqual(15, rlabels[1].y)
        self.assertEqual('B', rlabels[1].annotation)

        # x-position
        self.assertTrue(all( max(label.x) < 0 for label in llabels ))
        self.assertTrue(all( min(label.x) > 1 for label in rlabels ))

    @MultiplexTest.temporary_plot
    def test_draw_labels_with_none(self):
        """
        Test that when drawing labels and some of them have a value of None, they are not drawn.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        _, llabels, rlabels = viz.draw_slope([ 6, 1, 4, 7 ], [ 10, 15, 5, 8 ], label=[ 'A', None, 'C', None ])
        self.assertEqual(2, len(llabels))
        self.assertEqual(2, len(rlabels))
        self.assertEqual({ 'A', 'C' }, set( label.annotation for label in llabels ))
        self.assertEqual({ 'A', 'C' }, set( label.annotation for label in rlabels ))

    @MultiplexTest.temporary_plot
    def test_draw_labels_with_empty_string(self):
        """
        Test that when drawing labels and some of them have an empty string, they are not drawn.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        _, llabels, rlabels = viz.draw_slope([ 6, 1, 4, 7 ], [ 10, 15, 5, 8 ], label=[ 'A', '', 'C', '' ])
        self.assertEqual(2, len(llabels))
        self.assertEqual(2, len(rlabels))
        self.assertEqual({ 'A', 'C' }, set( label.annotation for label in llabels ))
        self.assertEqual({ 'A', 'C' }, set( label.annotation for label in rlabels ))

    @MultiplexTest.temporary_plot
    def test_draw_labels_with_style(self):
        """
        Test that when providing a style for the labels, it is used.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        _, llabels, rlabels = viz.draw_slope([ 6, 1, 4, 7 ], [ 10, 15, 5, 8 ],
                                             label=[ 'A', 'B', 'C', 'D' ], label_style={ 'color': 'red' })
        self.assertTrue(all( label.style.get('color') == 'red' for label in llabels + rlabels ))

    @MultiplexTest.temporary_plot
    def test_draw_labels_override_align(self):
        """
        Test that when providing a style for the labels with a custom alignment, it is used.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        _, llabels, rlabels = viz.draw_slope([ 6, 1, 4, 7 ], [ 10, 15, 5, 8 ],
                                             label=[ 'A', 'B', 'C', 'D' ], label_style={ 'align': 'center' })
        self.assertTrue(all( label.style.get('align') == 'center' for label in llabels + rlabels ))

    @MultiplexTest.temporary_plot
    def test_draw_labels_default_alignment(self):
        """
        Test that when no alignment is provided, the default alignment is right for the left axes and left for the right axes.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        _, llabels, rlabels = viz.draw_slope([ 6, 1, 4, 7 ], [ 10, 15, 5, 8 ],
                                             label=[ 'A', 'B', 'C', 'D' ])
        self.assertTrue(all( label.style.get('align') == 'right' for label in llabels ))
        self.assertTrue(all( label.style.get('align') == 'left' for label in rlabels ))

    @MultiplexTest.temporary_plot
    def test_draw_fit_axes_border_left_axes_no_labels(self):
        """
        Test that when drawing slope graphs without labels, the ticks on the left do not exceed the left axes.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        slope.draw(range(1, 11), range(1, 11))

        # make sure that the left axes do not exceed the plot
        ticks = viz.axes.get_yticklabels()
        self.assertEqual(10, len(ticks))
        self.assertEqual(0, min( util.get_bb(viz.figure, viz.axes, tick, transform=viz.axes.transAxes).x0 for tick in ticks ))
        self.assertTrue(all( util.get_bb(viz.figure, viz.axes, tick, transform=viz.axes.transAxes).x0 >= 0 for tick in ticks ))

    @MultiplexTest.temporary_plot
    def test_draw_fit_axes_border_left_axes_no_left_labels(self):
        """
        Test that when drawing slope graphs with labels only on the right, the ticks on the left do not exceed the left axes.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        slope.draw(range(1, 11), range(1, 11), label=[ f"{ i }" for i in range(1, 11) ], where='right')

        # make sure that the left axes do not exceed the plot
        ticks = viz.axes.get_yticklabels()
        self.assertEqual(10, len(ticks))
        self.assertEqual(0, round(min( util.get_bb(viz.figure, viz.axes, tick, transform=viz.axes.transAxes).x0 for tick in ticks ), 10))
        self.assertTrue(all( round(util.get_bb(viz.figure, viz.axes, tick, transform=viz.axes.transAxes).x0, 10) >= 0 for tick in ticks ))

    @MultiplexTest.temporary_plot
    def test_draw_fit_axes_border_right_axes_no_labels(self):
        """
        Test that when drawing slope graphs without labels, the ticks on the right do not exceed the right axes.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        slope.draw(range(1, 11), range(1, 11))

        # make sure that the right axes do not exceed the plot
        ticks = viz.secondary.get_yticklabels()
        self.assertEqual(10, len(ticks))
        self.assertEqual(1, max( util.get_bb(viz.figure, viz.secondary, tick, transform=viz.secondary.transAxes).x1 for tick in ticks ))
        self.assertTrue(all( util.get_bb(viz.figure, viz.secondary, tick, transform=viz.axes.transAxes).x1 <= 1 for tick in ticks ))

    @MultiplexTest.temporary_plot
    def test_draw_fit_axes_border_right_axes_no_right_labels(self):
        """
        Test that when drawing slope graphs with labels only on the left, the ticks on the right do not exceed the right axes.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        slope.draw(range(1, 11), range(1, 11), label=[ f"{ i }" for i in range(1, 11) ], where='left')

        # make sure that the left axes do not exceed the plot
        ticks = viz.secondary.get_yticklabels()
        self.assertEqual(10, len(ticks))
        self.assertEqual(1, round(max( util.get_bb(viz.figure, viz.secondary, tick, transform=viz.secondary.transAxes).x1 for tick in ticks ), 10))
        self.assertTrue(all( round(util.get_bb(viz.figure, viz.secondary, tick, transform=viz.secondary.transAxes).x1, 10) <= 1 for tick in ticks ))

    @MultiplexTest.temporary_plot
    def test_draw_fit_axes_labels_border_left_axes(self):
        """
        Test that when drawing slope graphs, the labels on the left do not exceed the left axes.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        slope.draw(range(1, 11), range(1, 11), label=[ f"label { i }" for i in range(1, 11) ])

        # make sure that the left axes do not exceed the plot
        ticks = viz.axes.get_yticklabels()
        self.assertEqual(10, len(ticks))
        self.assertTrue(all( util.get_bb(viz.figure, viz.axes, tick, transform=viz.axes.transAxes).x0 >= 0 for tick in ticks ))

        # make sure that the left labels do not exceed the plot
        self.assertEqual(10, len(slope.llabels))
        self.assertEqual(0, round(min( label.get_virtual_bb(transform=viz.axes.transAxes).x0 for label in slope.llabels), 10))
        self.assertTrue(all( label.get_virtual_bb(transform=viz.axes.transAxes).x0 >= 0 for label in slope.llabels ))

    @MultiplexTest.temporary_plot
    def test_draw_fit_axes_border_right_axes(self):
        """
        Test that when drawing slope graphs, the ticks on the right do not exceed the right axes.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        slope.draw(range(1, 11), range(1, 11), label=[ f"label { i }" for i in range(1, 11) ])

        # make sure that the right axes do not exceed the plot
        ticks = viz.secondary.get_yticklabels()
        self.assertEqual(10, len(ticks))
        self.assertTrue(all( util.get_bb(viz.figure, viz.secondary, tick, transform=viz.secondary.transAxes).x1 <= 1 for tick in ticks ))

        # make sure that the right labels do not exceed the plot
        self.assertEqual(10, len(slope.rlabels))
        self.assertEqual(1, round(max( label.get_virtual_bb(transform=viz.secondary.transAxes).x1 for label in slope.rlabels), 10))
        self.assertTrue(all( label.get_virtual_bb(transform=viz.secondary.transAxes).x1 <= 1 for label in slope.rlabels ))

    @MultiplexTest.temporary_plot
    def test_draw_fit_axes_labels_max_width(self):
        """
        Test that when drawing slope graphs, the max width of labels is 1.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        slope.draw(range(1, 11), range(1, 11), label=[ f"a " * 10 for i in range(1, 11) ])
        self.assertGreaterEqual(1, max( label.get_virtual_bb().width for label in slope.llabels ))

    @MultiplexTest.temporary_plot
    def test_draw_fit_axes_labels_ticks_overlap(self):
        """
        Test that when drawing slope graphs the ticks do not overlap with the y-ticks.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        slope.draw(range(1, 11), range(1, 11), label=[ f"label { i }" for i in range(1, 11) ])

        # get the bounding boxes of the y-tick labels
        ticks = viz.secondary.get_yticklabels()
        self.assertEqual(10, len(ticks))
        tick_bbs = [ util.get_bb(viz.figure, viz.axes, tick) for tick in ticks ]

        # get all the labels and their bounding boxes
        labels = slope.llabels + slope.rlabels
        self.assertEqual(20, len(labels))
        label_bbs = [ label.get_virtual_bb() for label in labels ]

        # make sure that none of the bounding boxes overlap.
        for bbt in tick_bbs:
            for bbl in label_bbs:
                self.assertFalse(util.overlapping_bb(bbt, bbl))

    @MultiplexTest.temporary_plot
    def test_draw_fit_axes_no_left_ticks(self):
        """
        Test that when drawing slope graphs without any left-ticks, the left axes default to -0.1.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        slope.draw(range(1, 11), range(1, 11), y1_tick='')

        # ensure that there are no ticks on the left and that the x-limit starts at -0.1
        ticks = viz.axes.get_yticklabels()
        self.assertEqual(0, len(ticks))
        self.assertEqual(-0.1, viz.axes.get_xlim()[0])

    @MultiplexTest.temporary_plot
    def test_draw_fit_axes_no_right_ticks(self):
        """
        Test that when drawing slope graphs without any right-ticks, the right axes default to 1.1.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        slope.draw(range(1, 11), range(1, 11), y2_tick='')

        # ensure that there are no ticks on the left and that the x-limit starts at 1.1
        ticks = viz.secondary.get_yticklabels()
        self.assertEqual(0, len(ticks))
        self.assertEqual(1.1, viz.secondary.get_xlim()[1])

    @MultiplexTest.temporary_plot
    def test_draw_labels_left(self):
        """
        Test that when drawing labels on the left, they really are drawn only on the left.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        slope.draw(range(1, 11), range(1, 11), label=[ f"label { i }" for i in range(1, 11) ], where='left')

        self.assertEqual(10, len(slope.llabels))
        self.assertEqual(0, len(slope.rlabels))

    @MultiplexTest.temporary_plot
    def test_draw_labels_right(self):
        """
        Test that when drawing labels on the right, they really are drawn only on the right.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        slope.draw(range(1, 11), range(1, 11), label=[ f"label { i }" for i in range(1, 11) ], where='right')

        self.assertEqual(10, len(slope.rlabels))
        self.assertEqual(0, len(slope.llabels))

    @MultiplexTest.temporary_plot
    def test_draw_labels_both(self):
        """
        Test that when drawing labels on both sides, they really are drawn only on both sides.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        slope.draw(range(1, 11), range(1, 11), label=[ f"label { i }" for i in range(1, 11) ], where='both')

        self.assertEqual(10, len(slope.rlabels))
        self.assertEqual(10, len(slope.llabels))

    @MultiplexTest.temporary_plot
    def test_draw_labels_mix_list(self):
        """
        Test that when drawing labels with a mix of sides, the correct sides are used.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        slope.draw(range(1, 11), range(1, 11), label=[ f"{ i }" for i in range(1, 11) ], where=[ 'left', 'right' ] * 5)

        self.assertEqual(5, len(slope.rlabels))
        self.assertEqual(5, len(slope.llabels))
        self.assertTrue(all( int(label.annotation) % 2 for label in slope.llabels )) # odd numbers are on the left
        self.assertTrue(all( not int(label.annotation) % 2 for label in slope.rlabels )) # even numbers are on the right

    @MultiplexTest.temporary_plot
    def test_add_ticks_unknown_where(self):
        """
        Test that when the ticks' ``where`` parameter is not 'left' or 'right', the function raises a ValueError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        self.assertRaises(ValueError, slope._add_ticks, range(0, 5), None, where='lef')

    @MultiplexTest.temporary_plot
    def test_add_ticks_where_case_insensitive(self):
        """
        Test that the ticks' ``where`` parameter is case insensitive.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        self.assertEqual(None, slope._add_ticks(range(0, 5), None, where='left'))
        self.assertEqual(None, slope._add_ticks(range(0, 5), None, where='Left'))
        self.assertEqual(None, slope._add_ticks(range(0, 5), None, where='LEFT'))
        self.assertEqual(None, slope._add_ticks(range(0, 5), None, where='right'))
        self.assertEqual(None, slope._add_ticks(range(0, 5), None, where='Right'))
        self.assertEqual(None, slope._add_ticks(range(0, 5), None, where='RIGHT'))

    @MultiplexTest.temporary_plot
    def test_add_labels_unknown_where(self):
        """
        Test that when the labels' ``where`` parameter is not 'left', 'right' or 'both', the function raises a ValueError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        self.assertRaises(ValueError, slope._add_labels, range(0, 5), range(0, 5), range(0, 5), where='lef')

    @MultiplexTest.temporary_plot
    def test_add_labels_where_case_insensitive(self):
        """
        Test that the labels' ``where`` parameter is case insensitive.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        self.assertTrue(slope._add_labels(range(0, 5), range(0, 5), range(0, 5), where='left'))
        self.assertTrue(slope._add_labels(range(0, 5), range(0, 5), range(0, 5), where='Left'))
        self.assertTrue(slope._add_labels(range(0, 5), range(0, 5), range(0, 5), where='LEFT'))
        self.assertTrue(slope._add_labels(range(0, 5), range(0, 5), range(0, 5), where='right'))
        self.assertTrue(slope._add_labels(range(0, 5), range(0, 5), range(0, 5), where='Right'))
        self.assertTrue(slope._add_labels(range(0, 5), range(0, 5), range(0, 5), where='RIGHT'))
        self.assertTrue(slope._add_labels(range(0, 5), range(0, 5), range(0, 5), where='both'))
        self.assertTrue(slope._add_labels(range(0, 5), range(0, 5), range(0, 5), where='Both'))
        self.assertTrue(slope._add_labels(range(0, 5), range(0, 5), range(0, 5), where='BOTH'))

    @MultiplexTest.temporary_plot
    def test_add_labels_unknown_where_list(self):
        """
        Test that when the labels' ``where`` parameter is a list with items that are not 'left', 'right' or 'both', the function raises a ValueError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        self.assertRaises(ValueError, slope._add_labels, range(0, 5), range(0, 5), range(0, 5), where=[ 'lef' ] * 5)

    @MultiplexTest.temporary_plot
    def test_add_labels_where_list_case_insensitive(self):
        """
        Test that the labels' ``where`` parameter is case insensitive when providing a list.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        slope = Slope(viz)
        self.assertTrue(slope._add_labels(range(0, 5), range(0, 5), range(0, 5), where=[ 'left' ] * 5))
        self.assertTrue(slope._add_labels(range(0, 5), range(0, 5), range(0, 5), where=[ 'Left' ] * 5))
        self.assertTrue(slope._add_labels(range(0, 5), range(0, 5), range(0, 5), where=[ 'LEFT' ] * 5))
        self.assertTrue(slope._add_labels(range(0, 5), range(0, 5), range(0, 5), where=[ 'right' ] * 5))
        self.assertTrue(slope._add_labels(range(0, 5), range(0, 5), range(0, 5), where=[ 'Right' ] * 5))
        self.assertTrue(slope._add_labels(range(0, 5), range(0, 5), range(0, 5), where=[ 'RIGHT' ] * 5))
        self.assertTrue(slope._add_labels(range(0, 5), range(0, 5), range(0, 5), where=[ 'both' ] * 5))
        self.assertTrue(slope._add_labels(range(0, 5), range(0, 5), range(0, 5), where=[ 'Both' ] * 5))
        self.assertTrue(slope._add_labels(range(0, 5), range(0, 5), range(0, 5), where=[ 'BOTH' ] * 5))
