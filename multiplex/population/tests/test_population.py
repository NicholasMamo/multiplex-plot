"""
Unit tests for the :class:`~population.population.Population` class.
"""

import math
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

    @MultiplexTest.temporary_plot
    def test_draw_float_rows(self):
        """
        Test that when drawing with a floating point number of rows, the function raises a TypeError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertRaises(TypeError, viz.draw_population, 5, 1.2)

    @MultiplexTest.temporary_plot
    def test_draw_negative_rows(self):
        """
        Test that when drawing with a negative number of rows, the function raises a ValueError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertRaises(ValueError, viz.draw_population, 5, -1)

    @MultiplexTest.temporary_plot
    def test_draw_zero_rows(self):
        """
        Test that when drawing with no rows, the function raises a ValueError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertRaises(ValueError, viz.draw_population, 5, 0)

    @MultiplexTest.temporary_plot
    def test_draw_float_population(self):
        """
        Test that when drawing with a floating point population, the function raises a TypeError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertRaises(TypeError, viz.draw_population, 2.4, 10)

    @MultiplexTest.temporary_plot
    def test_draw_negative_population(self):
        """
        Test that when drawing with a negative population, the function raises a ValueError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertRaises(ValueError, viz.draw_population, -5, 10)

    @MultiplexTest.temporary_plot
    def test_draw_negative_height(self):
        """
        Test that when drawing with a negative population height, the function raises a ValueError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertRaises(ValueError, viz.draw_population, 5, 10, height=-1)

    @MultiplexTest.temporary_plot
    def test_draw_zero_height(self):
        """
        Test that when drawing with a zero population height, the function raises a ValueError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertRaises(ValueError, viz.draw_population, 5, 10, height=0)

    @MultiplexTest.temporary_plot
    def test_draw_height_one(self):
        """
        Test that when drawing with a population height of 1, the function accepts it.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertTrue(viz.draw_population(5, 10, height=1))

    @MultiplexTest.temporary_plot
    def test_draw_large_height(self):
        """
        Test that when drawing with a large population height, the function raises a ValueError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertRaises(ValueError, viz.draw_population, 5, 10, height=2)

    @MultiplexTest.temporary_plot
    def test_draw_with_style(self):
        """
        Test that when drawing a population and styling the plot, the correct styling options are applied.
        """

        # check the initial style
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.grid(True)
        self.assertTrue(viz.axes.spines['left'].get_visible())
        self.assertTrue(viz.axes.xaxis._gridOnMajor)
        self.assertTrue(viz.axes.yaxis._gridOnMajor)
        self.assertFalse(viz.yaxis_inverted())

        # draw the population and let it set the new style
        self.assertTrue(viz.draw_population(5, 10, height=1, style_plot=True))
        self.assertFalse(viz.axes.spines['left'].get_visible())
        self.assertFalse(viz.axes.xaxis._gridOnMajor)
        self.assertFalse(viz.axes.yaxis._gridOnMajor)
        self.assertTrue(viz.yaxis_inverted())

    @MultiplexTest.temporary_plot
    def test_draw_without_style(self):
        """
        Test that when drawing a population without styling the plot, the style is not overwritten.
        """

        # check the initial style
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.grid(True)
        self.assertTrue(viz.axes.spines['left'].get_visible())
        self.assertTrue(viz.axes.xaxis._gridOnMajor)
        self.assertTrue(viz.axes.yaxis._gridOnMajor)
        self.assertFalse(viz.yaxis_inverted())

        # draw the population and do not let it set the new style
        self.assertTrue(viz.draw_population(5, 10, height=1, style_plot=False))
        self.assertTrue(viz.axes.spines['left'].get_visible())
        self.assertTrue(viz.axes.xaxis._gridOnMajor)
        self.assertTrue(viz.axes.yaxis._gridOnMajor)
        self.assertFalse(viz.yaxis_inverted())

    @MultiplexTest.temporary_plot
    def test_draw_with_style_multiple_times(self):
        """
        Test that when drawing multiple populations and styling the plot, the y-axes are not inverted more than once.
        """

        # check the initial style
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertFalse(viz.yaxis_inverted())

        # draw a population a first time, the y-axes should be inverted
        self.assertTrue(viz.draw_population(5, 10, height=1, style_plot=True))
        self.assertTrue(viz.yaxis_inverted())

        # draw a population a second time, the y-axes should still be inverted
        self.assertTrue(viz.draw_population(5, 10, height=1, style_plot=True))
        self.assertTrue(viz.yaxis_inverted())

    @MultiplexTest.temporary_plot
    def test_draw_zero_population(self):
        """
        Test that when drawing an empty population, the function returns an empty list of points.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertEqual([ ], viz.draw_population(0, 10))

    @MultiplexTest.temporary_plot
    def test_draw_correct_rows_square(self):
        """
        Test that when drawing a population, the number of rows in each column (except incomplete columns) is equal to the given number of rows.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        rows = 10
        drawn = viz.draw_population(30, rows)
        self.assertTrue(all( rows == len(column) for column in drawn ))

    @MultiplexTest.temporary_plot
    def test_draw_correct_rows_uneven(self):
        """
        Test that when drawing a population, the number of rows in each column is equal to the given number of rows, except for the last column when the population is not a factor of the rows.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        rows = 8
        drawn = viz.draw_population(30, rows)
        self.assertTrue(all( rows == len(column) for column in drawn[:-1] ))
        self.assertTrue(all( len(drawn[-1]) < len(column) for column in drawn[:-1] ))

    @MultiplexTest.temporary_plot
    def test_draw_equal_population(self):
        """
        Test that when drawing a population, all points are drawn.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = 30, 10
        drawn = viz.draw_population(population, rows)
        self.assertEqual(population, sum( len(column) for column in drawn ))

    @MultiplexTest.temporary_plot
    def test_draw_equal_population_uneven_columns(self):
        """
        Test that when drawing a population, the correct number of points are drawn even when the last column is incomplete.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = 25, 10
        drawn = viz.draw_population(population, rows)
        self.assertEqual(population, sum( len(column) for column in drawn ))

    @MultiplexTest.temporary_plot
    def test_draw_list_boolean(self):
        """
        Test that when providing a population as a list of booleans, the scatter points are all drawn.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = [ True, False ] * 12, 10
        drawn = viz.draw_population(population, rows)
        self.assertEqual(len(population), sum( len(column) for column in drawn ))

    @MultiplexTest.temporary_plot
    def test_draw_list_number(self):
        """
        Test that when providing a population as a list of numbers, the scatter points are all drawn.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = [ 5, 0.5 ] * 12, 10
        drawn = viz.draw_population(population, rows)
        self.assertEqual(len(population), sum( len(column) for column in drawn ))

    @MultiplexTest.temporary_plot
    def test_draw_list_dict(self):
        """
        Test that when providing a population as a list of empty dictionaries, the scatter points are all drawn.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = [ { } ] * 12, 10
        drawn = viz.draw_population(population, rows)
        self.assertEqual(len(population), sum( len(column) for column in drawn ))

    @MultiplexTest.temporary_plot
    def test_draw_list_like_number(self):
        """
        Test that when providing a population as a list, the scatter points are all drawn as if it's a normal population.
        """

        # draw a normal population
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = 25, 10
        drawn = viz.draw_population(population, rows)
        points = [ point for column in drawn for point in column ]
        bbs_1 = [ util.get_bb(viz.figure, viz.axes, point) for point in points ]

        # draw a population using a list
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = list(range(25)), 10
        drawn = viz.draw_population(population, rows)
        points = [ point for column in drawn for point in column ]
        bbs_2 = [ util.get_bb(viz.figure, viz.axes, point) for point in points ]

        # compare the bounding boxes
        self.assertTrue(all( str(bb1) == str(bb2) for bb1, bb2 in zip(bbs_1, bbs_2) ))

    @MultiplexTest.temporary_plot
    def test_draw_do_not_overlap(self):
        """
        Test that none of the drawn points in a population overlap.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        drawn = viz.draw_population(13, 3)
        points = [ point for column in drawn for point in column ]
        for i in range(0, len(points)):
            for j in range(i + 1, len(points)):
                self.assertFalse(util.overlapping(viz.figure, viz.axes, points[i], points[j]))

    @MultiplexTest.temporary_plot
    def test_draw_fits_within_height(self):
        """
        Test that the points fit within the given height.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        height = 0.5
        lim = (0.25, 0.75)
        drawn = viz.draw_population(15, 3, height=height)

        # check that all points are within the height
        points = [ point for column in drawn for point in column ]
        for point in points:
            bb = util.get_bb(viz.figure, viz.axes, point)
            self.assertTrue(lim[0] <= (bb.y0 + bb.y1)/2. <= lim[1])

        # check that the first point in each column is at the lowest point
        for column in drawn:
            bb = util.get_bb(viz.figure, viz.axes, column[0])
            self.assertEqual(lim[0], (bb.y0 + bb.y1) / 2)

        # check that the last point in each column is at the highest point
        for column in drawn:
            bb = util.get_bb(viz.figure, viz.axes, column[-1])
            self.assertEqual(lim[1], (bb.y0 + bb.y1) / 2)

    @MultiplexTest.temporary_plot
    def test_draw_rows_align(self):
        """
        Test that the drawn points align along the same row.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = 13, 3
        drawn = viz.draw_population(population, rows)

        # transpose the columns
        rows = [ [ column[row] for column in drawn if len(column) > row ] for row in range(rows) ]
        self.assertEqual(population, sum([ len(row) for row in rows ]))

        # check that each row's points have the same y0 and y1
        for row in rows:
            bb = util.get_bb(viz.figure, viz.axes, row[0])
            for point in row[1:]:
                _bb = util.get_bb(viz.figure, viz.axes, point)
                self.assertEqual(bb.y0, _bb.y0)
                self.assertEqual(bb.y1, _bb.y1)
                self.assertEqual(bb.height, _bb.height)

    @MultiplexTest.temporary_plot
    def test_draw_rows_equidistant(self):
        """
        Test that the rows are separated with the same gap.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = 10, 5
        drawn = viz.draw_population(population, rows)

        # transpose the columns
        rows = [ [ column[row] for column in drawn if len(column) > row ] for row in range(rows) ]
        self.assertEqual(population, sum([ len(row) for row in rows ]))

        # check that each row is equidistant from the next
        bb = util.get_bb(viz.figure, viz.axes, rows[0][0])
        bb_next = util.get_bb(viz.figure, viz.axes, rows[1][0])
        self.assertLess(bb.y1, bb_next.y0)
        gap = bb.y1 - bb_next.y0
        for i in range(len(rows)):
            bb = util.get_bb(viz.figure, viz.axes, rows[0][0])
            bb_next = util.get_bb(viz.figure, viz.axes, rows[1][0])
            self.assertEqual(gap, bb.y1 - bb_next.y0)

    @MultiplexTest.temporary_plot
    def test_draw_columns_align(self):
        """
        Test that the drawn points align along the same column.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = 13, 3
        drawn = viz.draw_population(population, rows)

        # check that each column's points have the same x0 and x1
        for column in drawn:
            bb = util.get_bb(viz.figure, viz.axes, column[0])
            for point in column[1:]:
                _bb = util.get_bb(viz.figure, viz.axes, point)
                self.assertEqual(bb.x0, _bb.x0)
                self.assertEqual(bb.x1, _bb.x1)
                self.assertEqual(bb.width, _bb.width)

    @MultiplexTest.temporary_plot
    def test_draw_columns_equidistant(self):
        """
        Test that the columns are separated with the same gap.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = 10, 5
        drawn = viz.draw_population(population, rows)

        # check that each columns is equidistant from the next
        bb = util.get_bb(viz.figure, viz.axes, drawn[0][0])
        bb_next = util.get_bb(viz.figure, viz.axes, drawn[1][0])
        self.assertLess(bb.x1, bb_next.x0)
        gap = bb.x1 - bb_next.x0
        for i in range(len(drawn)):
            bb = util.get_bb(viz.figure, viz.axes, drawn[0][0])
            bb_next = util.get_bb(viz.figure, viz.axes, drawn[1][0])
            self.assertEqual(gap, bb.x1 - bb_next.x0)

    @MultiplexTest.temporary_plot
    def test_draw_apply_general_style(self):
        """
        Test that when passing on keyword arguments, they are treated as the general style and applied to all points.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        color = '#F1428A'
        drawn = viz.draw_population(10, 3, color=color)
        points = [ point for column in drawn for point in column ]
        self.assertTrue(all( [241/255, 66/255, 138/255, 1] == point.get_facecolor().tolist()[0] for point in points ))

    @MultiplexTest.temporary_plot
    def test_draw_xticks_empty_population(self):
        """
        Test that no x-ticks are added when the population is empty.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        drawn = viz.draw_population(0, 3)
        self.assertEqual([ ], viz.get_xticks().tolist())

    @MultiplexTest.temporary_plot
    def test_draw_xticks_square_population(self):
        """
        Test that the correct x-ticks are added when the population is a square.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = 9, 3
        drawn = viz.draw_population(population, rows)
        self.assertEqual(list(range(1, 1 + math.ceil(population/rows))),
                         viz.get_xticks().tolist())
        self.assertEqual([ str(rows * tick) for tick in range(1, 1+ math.ceil(population/rows)) ],
                         [ label.get_text() for label in viz.get_xticklabels() ])
        self.assertEqual(int(viz.get_xticklabels()[-1].get_text()), population)

    @MultiplexTest.temporary_plot
    def test_draw_xticks_uneven_population(self):
        """
        Test that the correct x-ticks are added when the population is not an even square.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = 10, 3
        drawn = viz.draw_population(population, rows)
        self.assertEqual(list(range(1, 1 + math.ceil(population/rows))),
                         viz.get_xticks().tolist())
        self.assertEqual([ str(rows * tick) for tick in range(1, 1+ math.ceil(population/rows)) ],
                         [ label.get_text() for label in viz.get_xticklabels() ])
        self.assertGreater(int(viz.get_xticklabels()[-1].get_text()), population)

    @MultiplexTest.temporary_plot
    def test_limit_negative_height(self):
        """
        Test that when drawing with a negative population height, the function raises a ValueError.
        """

        viz = Population(drawable.Drawable)
        self.assertRaises(ValueError, viz._limit, -1)

    @MultiplexTest.temporary_plot
    def test_limit_zero_height(self):
        """
        Test that when drawing with a zero population height, the function raises a ValueError.
        """

        viz = Population(drawable.Drawable)
        self.assertRaises(ValueError, viz._limit, 0)

    @MultiplexTest.temporary_plot
    def test_limit_height_one(self):
        """
        Test that when drawing with a population height of 1, the function accepts it.
        """

        viz = Population(drawable.Drawable)
        self.assertTrue(viz._limit(1))

    @MultiplexTest.temporary_plot
    def test_limit_large_height(self):
        """
        Test that when drawing with a large population height, the function raises a ValueError.
        """

        viz = Population(drawable.Drawable)
        self.assertRaises(ValueError, viz._limit, 2)

    @MultiplexTest.temporary_plot
    def test_limit(self):
        """
        Test calculating the limit.
        """

        viz = Population(drawable.Drawable)
        self.assertEqual((0.25, 0.75), viz._limit(0.5))

    @MultiplexTest.temporary_plot
    def test_limit_order(self):
        """
        Test that the limit is a tuple in ascending order.
        """

        viz = Population(drawable.Drawable)
        limit = viz._limit(0.5)
        self.assertEqual(tuple, type(limit))
        self.assertLess(limit[0], limit[1])

    @MultiplexTest.temporary_plot
    def test_gap_size_float_rows(self):
        """
        Test that when getting the gap size and the number of rows is a float, the function raises a TypeError.
        """

        viz = Population(drawable.Drawable)
        self.assertRaises(TypeError, viz._gap_size, (0, 1), 1.2)

    @MultiplexTest.temporary_plot
    def test_gap_size_negative_rows(self):
        """
        Test that when getting the gap size and the number of rows is a negative integer, the function raises a ValueError.
        """

        viz = Population(drawable.Drawable)
        self.assertRaises(ValueError, viz._gap_size, (0, 1), -1)

    @MultiplexTest.temporary_plot
    def test_gap_size_zero_rows(self):
        """
        Test that when getting the gap size and the number of rows is zero, the function raises a ValueError.
        """

        viz = Population(drawable.Drawable)
        self.assertRaises(ValueError, viz._gap_size, (0, 1), 0)

    @MultiplexTest.temporary_plot
    def test_gap_size_one_row(self):
        """
        Test that that the gap size of one row is 0.
        """

        viz = Population(drawable.Drawable)
        self.assertEqual(0, viz._gap_size((0, 1), 1))

    @MultiplexTest.temporary_plot
    def test_gap_size_two_rows(self):
        """
        Test that that the gap size of two rows is equivalent to the gap between the limits.
        """

        viz = Population(drawable.Drawable)

        lim = (0, 1)
        self.assertEqual(lim[1] - lim[0], viz._gap_size(lim, 2))

        lim = (0.2, 0.8)
        self.assertEqual(lim[1] - lim[0], viz._gap_size(lim, 2))

    @MultiplexTest.temporary_plot
    def test_gap_size_multiple_rows(self):
        """
        Test that that the gap size of multiple rows fills the space between the limits.
        """

        viz = Population(drawable.Drawable)

        lim, rows = (0, 1), 4
        self.assertEqual(lim[1], lim[0] + viz._gap_size(lim, rows) * (rows - 1))

        lim, rows = (0.2, 0.8), 5
        self.assertEqual(lim[1], lim[0] + viz._gap_size(lim, rows) * (rows - 1))
