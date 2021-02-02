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
    def test_init_save_drawable(self):
        """
        Test that when creating the population, the drawable is saved.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        popviz = Population(viz)
        self.assertEqual(viz, popviz.drawable)

    @MultiplexTest.temporary_plot
    def test_init_empty_start_labels(self):
        """
        Test that when creating the population, the drawable creates an empty list for start labels.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        popviz = Population(viz)
        self.assertEqual([ ], popviz.start_labels)

    @MultiplexTest.temporary_plot
    def test_init_empty_populations(self):
        """
        Test that when creating the population, the drawable creates an empty list for populations.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        popviz = Population(viz)
        self.assertEqual([ ], popviz.populations)

    @MultiplexTest.temporary_plot
    def test_init_none_rows(self):
        """
        Test that when creating the population, the drawable initializes the number of rows to ``None``.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        popviz = Population(viz)
        self.assertEqual(None, popviz.rows)

    @MultiplexTest.temporary_plot
    def test_draw_float_rows(self):
        """
        Test that when drawing with a floating point number of rows, the function raises a TypeError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertRaises(TypeError, viz.draw_population, 5, 1.2, '')

    @MultiplexTest.temporary_plot
    def test_draw_negative_rows(self):
        """
        Test that when drawing with a negative number of rows, the function raises a ValueError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertRaises(ValueError, viz.draw_population, 5, -1, '')

    @MultiplexTest.temporary_plot
    def test_draw_zero_rows(self):
        """
        Test that when drawing with no rows, the function raises a ValueError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertRaises(ValueError, viz.draw_population, 5, 0, '')

    @MultiplexTest.temporary_plot
    def test_draw_float_population(self):
        """
        Test that when drawing with a floating point population, the function raises a TypeError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertRaises(TypeError, viz.draw_population, 2.4, 10, '')

    @MultiplexTest.temporary_plot
    def test_draw_negative_population(self):
        """
        Test that when drawing with a negative population, the function raises a ValueError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertRaises(ValueError, viz.draw_population, -5, 10, '')

    @MultiplexTest.temporary_plot
    def test_draw_negative_height(self):
        """
        Test that when drawing with a negative population height, the function raises a ValueError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertRaises(ValueError, viz.draw_population, 5, 10, '', height=-1)

    @MultiplexTest.temporary_plot
    def test_draw_zero_height(self):
        """
        Test that when drawing with a zero population height, the function raises a ValueError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertRaises(ValueError, viz.draw_population, 5, 10, '', height=0)

    @MultiplexTest.temporary_plot
    def test_draw_height_one(self):
        """
        Test that when drawing with a population height of 1, the function accepts it.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertTrue(viz.draw_population(5, 10, '', height=1))

    @MultiplexTest.temporary_plot
    def test_draw_large_height(self):
        """
        Test that when drawing with a large population height, the function raises a ValueError.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertRaises(ValueError, viz.draw_population, 5, 10, '', height=2)

    @MultiplexTest.temporary_plot
    def test_draw_save_rows_first_time(self):
        """
        Test that when drawing a population the first time, the number of rows are saved in the class.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        rows = 10
        pop = viz.draw_population(5, rows, '', height=1)
        self.assertEqual(rows, viz.population.rows)

    @MultiplexTest.temporary_plot
    def test_draw_save_rows_second_time(self):
        """
        Test that when drawing a population the second time, the number of rows are unchanged in the class.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        rows = 10

        # draw the first population
        pop = viz.draw_population(5, rows, '', height=1)
        self.assertEqual(rows, viz.population.rows)

        # draw the second population
        pop = viz.draw_population(5, rows, '', height=1)
        self.assertEqual(rows, viz.population.rows)

    @MultiplexTest.temporary_plot
    def test_draw_save_rows_different(self):
        """
        Test that when drawing a population with a different number of rows than before, the class raises a warning.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        rows = 10

        # draw the first population
        pop = viz.draw_population(5, rows, '', height=1)
        self.assertEqual(rows, viz.population.rows)

        # draw the second population
        with self.assertWarns(Warning):
            pop = viz.draw_population(5, rows - 1, '', height=1)

    @MultiplexTest.temporary_plot
    def test_draw_save_rows_different_update(self):
        """
        Test that when drawing a population with a different number of rows than before, the class saves the new number of rows after raising a warning.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        rows = 10

        # draw the first population
        pop = viz.draw_population(5, rows, '', height=1)
        self.assertEqual(rows, viz.population.rows)

        # draw the second population
        with self.assertWarns(Warning):
            pop = viz.draw_population(5, rows - 1, '', height=1)
            self.assertEqual(rows - 1, viz.population.rows)

    @MultiplexTest.temporary_plot
    def test_draw_save_population(self):
        """
        Test that when drawing a population, it is saved in the class too.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        pop = viz.draw_population(5, 10, '', height=1)
        self.assertEqual([ pop ], viz.population.populations)

    @MultiplexTest.temporary_plot
    def test_draw_save_multiple_population(self):
        """
        Test that when drawing multiple populations, all of them are saved in the class.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        pop1 = viz.draw_population(5, 10, '', height=1)
        self.assertEqual([ pop1 ], viz.population.populations)

        pop2 = viz.draw_population(5, 10, '', height=1)
        self.assertEqual([ pop1, pop2 ], viz.population.populations)

    @MultiplexTest.temporary_plot
    def test_draw_with_style(self):
        """
        Test that when drawing a population and styling the plot, the correct styling options are applied.
        """

        # test the initial style
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.grid(True)
        self.assertTrue(viz.axes.spines['left'].get_visible())
        self.assertTrue(viz.axes.xaxis._gridOnMajor)
        self.assertTrue(viz.axes.yaxis._gridOnMajor)
        self.assertFalse(viz.yaxis_inverted())

        # draw the population and let it set the new style
        self.assertTrue(viz.draw_population(5, 10, '', height=1, style_plot=True))
        self.assertFalse(viz.axes.spines['left'].get_visible())
        self.assertFalse(viz.axes.xaxis._gridOnMajor)
        self.assertFalse(viz.axes.yaxis._gridOnMajor)
        self.assertTrue(viz.yaxis_inverted())

    @MultiplexTest.temporary_plot
    def test_draw_without_style(self):
        """
        Test that when drawing a population without styling the plot, the style is not overwritten.
        """

        # test the initial style
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.grid(True)
        self.assertTrue(viz.axes.spines['left'].get_visible())
        self.assertTrue(viz.axes.xaxis._gridOnMajor)
        self.assertTrue(viz.axes.yaxis._gridOnMajor)
        self.assertFalse(viz.yaxis_inverted())

        # draw the population and do not let it set the new style
        self.assertTrue(viz.draw_population(5, 10, '', height=1, style_plot=False))
        self.assertTrue(viz.axes.spines['left'].get_visible())
        self.assertTrue(viz.axes.xaxis._gridOnMajor)
        self.assertTrue(viz.axes.yaxis._gridOnMajor)
        self.assertFalse(viz.yaxis_inverted())

    @MultiplexTest.temporary_plot
    def test_draw_with_style_multiple_times(self):
        """
        Test that when drawing multiple populations and styling the plot, the y-axes are not inverted more than once.
        """

        # test the initial style
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertFalse(viz.yaxis_inverted())

        # draw a population a first time, the y-axes should be inverted
        self.assertTrue(viz.draw_population(5, 10, '', height=1, style_plot=True))
        self.assertTrue(viz.yaxis_inverted())

        # draw a population a second time, the y-axes should still be inverted
        self.assertTrue(viz.draw_population(5, 10, '', height=1, style_plot=True))
        self.assertTrue(viz.yaxis_inverted())

    @MultiplexTest.temporary_plot
    def test_draw_zero_population(self):
        """
        Test that when drawing an empty population, the function returns an empty list of points.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        self.assertEqual([ ], viz.draw_population(0, 10, ''))

    @MultiplexTest.temporary_plot
    def test_draw_correct_rows_square(self):
        """
        Test that when drawing a population, the number of rows in each column (except incomplete columns) is equal to the given number of rows.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        rows = 10
        drawn = viz.draw_population(30, rows, '')
        self.assertTrue(all( rows == len(column) for column in drawn ))

    @MultiplexTest.temporary_plot
    def test_draw_correct_rows_uneven(self):
        """
        Test that when drawing a population, the number of rows in each column is equal to the given number of rows, except for the last column when the population is not a factor of the rows.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        rows = 8
        drawn = viz.draw_population(30, rows, '')
        self.assertTrue(all( rows == len(column) for column in drawn[:-1] ))
        self.assertTrue(all( len(drawn[-1]) < len(column) for column in drawn[:-1] ))

    @MultiplexTest.temporary_plot
    def test_draw_equal_population(self):
        """
        Test that when drawing a population, all points are drawn.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = 30, 10
        drawn = viz.draw_population(population, rows, '')
        self.assertEqual(population, sum( len(column) for column in drawn ))

    @MultiplexTest.temporary_plot
    def test_draw_equal_population_uneven_columns(self):
        """
        Test that when drawing a population, the correct number of points are drawn even when the last column is incomplete.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = 25, 10
        drawn = viz.draw_population(population, rows, '')
        self.assertEqual(population, sum( len(column) for column in drawn ))

    @MultiplexTest.temporary_plot
    def test_draw_list_boolean(self):
        """
        Test that when providing a population as a list of booleans, the scatter points are all drawn.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = [ True, False ] * 12, 10
        drawn = viz.draw_population(population, rows, '')
        self.assertEqual(len(population), sum( len(column) for column in drawn ))

    @MultiplexTest.temporary_plot
    def test_draw_list_number(self):
        """
        Test that when providing a population as a list of numbers, the scatter points are all drawn.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = [ 5, 0.5 ] * 12, 10
        drawn = viz.draw_population(population, rows, '')
        self.assertEqual(len(population), sum( len(column) for column in drawn ))

    @MultiplexTest.temporary_plot
    def test_draw_list_dict(self):
        """
        Test that when providing a population as a list of empty dictionaries, the scatter points are all drawn.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = [ { } ] * 12, 10
        drawn = viz.draw_population(population, rows, '')
        self.assertEqual(len(population), sum( len(column) for column in drawn ))

    @MultiplexTest.temporary_plot
    def test_draw_list_like_number(self):
        """
        Test that when providing a population as a list, the scatter points are all drawn as if it's a normal population.
        """

        # draw a normal population
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = 25, 10
        drawn = viz.draw_population(population, rows, '')
        points = [ point for column in drawn for point in column ]
        bbs_1 = [ util.get_bb(viz.figure, viz.axes, point) for point in points ]

        # draw a population using a list
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = list(range(25)), 10
        drawn = viz.draw_population(population, rows, '')
        points = [ point for column in drawn for point in column ]
        bbs_2 = [ util.get_bb(viz.figure, viz.axes, point) for point in points ]

        # compare the bounding boxes
        self.assertTrue(all( str(bb1) == str(bb2) for bb1, bb2 in zip(bbs_1, bbs_2) ))

    @MultiplexTest.temporary_plot
    def test_draw_centered(self):
        """
        Test that the drawn population is centered along the y-axis position.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = 25, 5
        drawn = viz.draw_population(population, rows, '')
        for column in drawn:
            bb_top = util.get_bb(viz.figure, viz.axes, column[0])
            bb_bottom = util.get_bb(viz.figure, viz.axes, column[-1])
            self.assertEqual(0.5, (bb_top.y1 + bb_bottom.y0) / 2)

    @MultiplexTest.temporary_plot
    def test_draw_centered_uneven(self):
        """
        Test that the drawn population is centered along the y-axis position unless the column is uneven.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = 22, 5
        drawn = viz.draw_population(population, rows, '')
        for column in drawn:
            if len(column) < rows:
                continue

            bb_top = util.get_bb(viz.figure, viz.axes, column[0])
            bb_bottom = util.get_bb(viz.figure, viz.axes, column[-1])
            self.assertEqual(0.5, (bb_top.y1 + bb_bottom.y0) / 2)

    @MultiplexTest.temporary_plot
    def test_draw_do_not_overlap(self):
        """
        Test that none of the drawn points in a population overlap.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        drawn = viz.draw_population(13, 3, '')
        points = [ point for column in drawn for point in column ]
        for i in range(0, len(points)):
            for j in range(i + 1, len(points)):
                self.assertFalse(util.overlapping(viz.figure, viz.axes, points[i], points[j]))

    @MultiplexTest.temporary_plot
    def test_draw_populations_do_not_overlap(self):
        """
        Test that none of the drawn points across two populations overlap.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))

        # draw the first population
        drawn = viz.draw_population(13, 3, '')
        p1 = [ point for column in drawn for point in column ]

        # draw the second population
        drawn = viz.draw_population(13, 3, '')
        p2 = [ point for column in drawn for point in column ]

        for _p1 in p1:
            for _p2 in p2:
                self.assertFalse(util.overlapping(viz.figure, viz.axes, _p1, _p2))

    @MultiplexTest.temporary_plot
    def test_draw_fits_within_height(self):
        """
        Test that the points fit within the given height.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        height = 0.5
        lim = (0.25, 0.75)
        drawn = viz.draw_population(15, 3, '', height=height)

        # test that all points are within the height
        points = [ point for column in drawn for point in column ]
        for point in points:
            bb = util.get_bb(viz.figure, viz.axes, point)
            self.assertTrue(lim[0] <= (bb.y0 + bb.y1)/2. <= lim[1])

        # test that the first point in each column is at the lowest point
        for column in drawn:
            bb = util.get_bb(viz.figure, viz.axes, column[0])
            self.assertEqual(lim[0], (bb.y0 + bb.y1) / 2)

        # test that the last point in each column is at the highest point
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
        drawn = viz.draw_population(population, rows, '')

        # transpose the columns
        rows = [ [ column[row] for column in drawn if len(column) > row ] for row in range(rows) ]
        self.assertEqual(population, sum([ len(row) for row in rows ]))

        # test that each row's points have the same y0 and y1
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
        drawn = viz.draw_population(population, rows, '')

        # transpose the columns
        rows = [ [ column[row] for column in drawn if len(column) > row ] for row in range(rows) ]
        self.assertEqual(population, sum([ len(row) for row in rows ]))

        # test that each row is equidistant from the next
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
        drawn = viz.draw_population(population, rows, '')

        # test that each column's points have the same x0 and x1
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
        drawn = viz.draw_population(population, rows, '')

        # test that each columns is equidistant from the next
        bb = util.get_bb(viz.figure, viz.axes, drawn[0][0])
        bb_next = util.get_bb(viz.figure, viz.axes, drawn[1][0])
        self.assertLess(bb.x1, bb_next.x0)
        gap = bb.x1 - bb_next.x0
        for i in range(len(drawn)):
            bb = util.get_bb(viz.figure, viz.axes, drawn[0][0])
            bb_next = util.get_bb(viz.figure, viz.axes, drawn[1][0])
            self.assertEqual(gap, bb.x1 - bb_next.x0)

    @MultiplexTest.temporary_plot
    def test_draw_style_general(self):
        """
        Test that when passing on keyword arguments, they are treated as the general style and applied to all points.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        color = '#F1428A'
        drawn = viz.draw_population(10, 3, '', color=color)
        points = [ point for column in drawn for point in column ]
        self.assertTrue(all( [241/255, 66/255, 138/255, 1] == point.get_facecolor().tolist()[0] for point in points ))

    @MultiplexTest.temporary_plot
    def test_draw_style_no_specific_style(self):
        """
        Test that when the population is made up of empty dictionaries, the items inherit the general style.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        color = '#F1428A'
        population, rows = 10, 3
        drawn = viz.draw_population([ { } ] * population, rows, '', color=color)
        points = [ point for column in drawn for point in column ]
        self.assertEqual(population, len(points))
        self.assertTrue(all( [241/255, 66/255, 138/255, 1] == point.get_facecolor().tolist()[0] for point in points ))

    @MultiplexTest.temporary_plot
    def test_draw_style_no_general_style(self):
        """
        Test that when the population has no general style, but the specific style is given for each item, all items have the same specific style.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = 10, 3
        drawn = viz.draw_population([ { 'color': '#F1428A' } ] * population, rows, '')
        points = [ point for column in drawn for point in column ]
        self.assertEqual(population, len(points))
        self.assertTrue(all( [241/255, 66/255, 138/255, 1] == point.get_facecolor().tolist()[0] for point in points ))

    @MultiplexTest.temporary_plot
    def test_draw_style_spcific_per_item(self):
        """
        Test that when some population items have a specific style, it is only applied to them, not to the others.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = [ { } ] * 10, 3
        population[2] = { 'color': '#F1428A' }
        drawn = viz.draw_population(population, rows, '')
        points = [ point for column in drawn for point in column ]

        # test the styled point's color
        self.assertEqual([241/255, 66/255, 138/255, 1], points[2].get_facecolor().tolist()[0])

        # test that the rest of the points do not have the same color as the styled point
        self.assertTrue(all( [241/255, 66/255, 138/255, 1] != point.get_facecolor().tolist()[0]
                             for i, point in enumerate(points) if i != 2 ))

    @MultiplexTest.temporary_plot
    def test_draw_style_spcific_overrides_general(self):
        """
        Test that the specific style overrides the general style.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        color = '#F18A42'
        population, rows = [ { } ] * 10, 3
        population[2] = { 'color': '#F1428A' }
        drawn = viz.draw_population(population, rows, '', color=color)
        points = [ point for column in drawn for point in column ]

        # test the styled point's color
        self.assertEqual([241/255, 66/255, 138/255, 1], points[2].get_facecolor().tolist()[0])

        # test that the rest of the points do not have the same color as the styled point
        self.assertTrue(all( [241/255, 138/255, 66/255, 1] == point.get_facecolor().tolist()[0]
                             for i, point in enumerate(points) if i != 2 ))

    @MultiplexTest.temporary_plot
    def test_draw_style_spcific_retains_general(self):
        """
        Test that the specific style does not override the general style in parameters it does not have.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        color, edgecolor = '#F18A42', '#8A42F1'
        population, rows = [ { } ] * 10, 3
        population[2] = { 'color': '#F1428A' }
        drawn = viz.draw_population(population, rows, '', color=color, edgecolor=edgecolor)
        points = [ point for column in drawn for point in column ]

        # test the styled point's color
        self.assertEqual([241/255, 66/255, 138/255, 1], points[2].get_facecolor().tolist()[0])

        # test that the rest of the points do not have the same color as the styled point
        self.assertTrue(all( [241/255, 138/255, 66/255, 1] == point.get_facecolor().tolist()[0]
                             for i, point in enumerate(points) if i != 2 ))

        # test that the edge color is the same in all cases
        self.assertTrue(all( [138/255, 66/255, 241/255, 1] == point.get_edgecolor().tolist()[0] for point in points ))

    @MultiplexTest.temporary_plot
    def test_draw_xticks_empty_population(self):
        """
        Test that no x-ticks are added when the population is empty.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        drawn = viz.draw_population(0, 3, '')
        self.assertEqual([ ], viz.get_xticks().tolist())

    @MultiplexTest.temporary_plot
    def test_draw_xticks_square_population(self):
        """
        Test that the correct x-ticks are added when the population is a square.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = 9, 3
        drawn = viz.draw_population(population, rows, '')
        self.assertEqual(list(range(1, 1 + math.ceil(population/rows))),
                         viz.get_xticks().tolist())
        self.assertEqual([ str(rows * tick) for tick in range(1, 1 + math.ceil(population/rows)) ],
                         [ label.get_text() for label in viz.get_xticklabels() ])
        self.assertEqual(int(viz.get_xticklabels()[-1].get_text()), population)

    @MultiplexTest.temporary_plot
    def test_draw_xticks_uneven_population(self):
        """
        Test that the correct x-ticks are added when the population is not an even square.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = 10, 3
        drawn = viz.draw_population(population, rows, '')
        self.assertEqual(list(range(1, 1 + math.ceil(population/rows))),
                         viz.get_xticks().tolist())
        self.assertEqual([ str(rows * tick) for tick in range(1, 1 + math.ceil(population/rows)) ],
                         [ label.get_text() for label in viz.get_xticklabels() ])
        self.assertGreater(int(viz.get_xticklabels()[-1].get_text()), population)

    @MultiplexTest.temporary_plot
    def test_draw_xticks_larger_population(self):
        """
        Test that the correct x-ticks are added when a larger population is added.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))

        # draw the first population
        population, rows = 10, 3
        drawn = viz.draw_population(population, rows, '')
        self.assertEqual(list(range(1, 1 + math.ceil(population/rows))),
                         viz.get_xticks().tolist())
        self.assertEqual([ str(rows * tick) for tick in range(1, 1 + math.ceil(population/rows)) ],
                         [ label.get_text() for label in viz.get_xticklabels() ])
        self.assertEqual(int(viz.get_xticklabels()[-1].get_text()), population + rows - population % rows)

        # draw a larger population
        population, rows = 20, 3
        drawn = viz.draw_population(population, rows, '')
        self.assertEqual(list(range(1, 1 + math.ceil(population/rows))),
                         viz.get_xticks().tolist())
        self.assertEqual([ str(rows * tick) for tick in range(1, 1 + math.ceil(population/rows)) ],
                         [ label.get_text() for label in viz.get_xticklabels() ])
        self.assertEqual(int(viz.get_xticklabels()[-1].get_text()), population + rows - population % rows)

    @MultiplexTest.temporary_plot
    def test_draw_xticks_smaller_population(self):
        """
        Test that the x-ticks are not updated when adding a smaller population.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))

        # draw the first population
        population, rows = 10, 3
        drawn = viz.draw_population(population, rows, '')
        self.assertEqual(list(range(1, 1 + math.ceil(population/rows))),
                         viz.get_xticks().tolist())
        self.assertEqual([ str(rows * tick) for tick in range(1, 1 + math.ceil(population/rows)) ],
                         [ label.get_text() for label in viz.get_xticklabels() ])
        self.assertEqual(int(viz.get_xticklabels()[-1].get_text()), population + rows - population % rows)
        og_ticks = list(viz.get_xticks().tolist())
        og_ticklabels = list(viz.get_xticklabels())

        # draw a smaller population
        population, rows = 7, 3
        drawn = viz.draw_population(population, rows, '')
        self.assertEqual(viz.get_xticks().tolist(), og_ticks)
        self.assertEqual(viz.get_xticklabels(), og_ticklabels)

    @MultiplexTest.temporary_plot
    def test_draw_spine_bounds_start_at_1(self):
        """
        Test that the spine bounds always start from 1.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = 12, 3
        drawn = viz.draw_population(population, rows, '')
        self.assertEqual(1, viz.axes.spines['bottom'].get_bounds()[0])

    @MultiplexTest.temporary_plot
    def test_draw_spine_bounds_start_at_1_multiple_populations(self):
        """
        Test that the spine bounds always start from 1 even when adding multiple populations.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = 12, 3

        # draw the first population
        drawn = viz.draw_population(population, rows, '')
        self.assertEqual(1, viz.axes.spines['bottom'].get_bounds()[0])

        # draw the second population
        drawn = viz.draw_population(population, rows, '')
        self.assertEqual(1, viz.axes.spines['bottom'].get_bounds()[0])

    @MultiplexTest.temporary_plot
    def test_draw_spine_bounds_start_at_1_larger_population(self):
        """
        Test that the spine bounds start from 1 and end at the largest population when adding a larger population.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))

        # draw the first population
        population, rows = 14, 3
        drawn = viz.draw_population(population, rows, '', color='#000000')
        self.assertEqual(1, viz.axes.spines['bottom'].get_bounds()[0])
        self.assertEqual(math.ceil(population / rows), viz.axes.spines['bottom'].get_bounds()[1])

        # draw a larger population
        population, rows = 20, 3
        drawn = viz.draw_population(population, rows, '')
        self.assertEqual(1, viz.axes.spines['bottom'].get_bounds()[0])
        self.assertEqual(math.ceil(population / rows), viz.axes.spines['bottom'].get_bounds()[1])

    @MultiplexTest.temporary_plot
    def test_draw_spine_bounds_start_at_1_smaller_population(self):
        """
        Test that the spine bounds start from 1 and end at the largest population even when adding a smaller population.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))

        # draw the first population
        population, rows = 14, 3
        drawn = viz.draw_population(population, rows, '', color='#000000')
        self.assertEqual(1, viz.axes.spines['bottom'].get_bounds()[0])
        self.assertEqual(math.ceil(population / rows), viz.axes.spines['bottom'].get_bounds()[1])
        og = tuple(viz.axes.spines['bottom'].get_bounds())

        # draw a smaller population
        population, rows = 7, 3
        drawn = viz.draw_population(population, rows, '')
        self.assertEqual(og, viz.axes.spines['bottom'].get_bounds())

    @MultiplexTest.temporary_plot
    def test_draw_spine_bounds_square(self):
        """
        Test that the correct spine bounds are added when the population is a square.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = 12, 3
        drawn = viz.draw_population(population, rows, '')
        self.assertEqual((1, population / rows), viz.axes.spines['bottom'].get_bounds())

    @MultiplexTest.temporary_plot
    def test_draw_spine_bounds_uneven(self):
        """
        Test that the correct spine bounds are added when the population has uneven columns.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        population, rows = 10, 3
        drawn = viz.draw_population(population, rows, '')
        self.assertEqual((1, math.ceil(population / rows)), viz.axes.spines['bottom'].get_bounds())

    @MultiplexTest.temporary_plot
    def test_draw_ytick(self):
        """
        Test that when drawing a population, the correct y-tick is added.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        name = 'New population'
        drawn = viz.draw_population(10, 5, name)
        self.assertEqual([ name ], [ label.get_text() for label in viz.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_ytick_multiple_populations(self):
        """
        Test that when drawing multiple populations, the correct y-ticks are added.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        names = [ 'Population 1', 'Population 2' ]

        # draw the first population
        drawn = viz.draw_population(10, 5, names[0])
        self.assertEqual(names[:1], [ label.get_text() for label in viz.get_yticklabels() ])

        # draw the second population
        drawn = viz.draw_population(10, 5, names[1])
        self.assertEqual(names, [ label.get_text() for label in viz.get_yticklabels() ])

    @MultiplexTest.temporary_plot
    def test_draw_ytick_center(self):
        """
        Test that when drawing a population, the y-tick is centered along the population.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        name = 'New population'
        drawn = viz.draw_population(10, 5, name)
        self.assertEqual([ 0.5 ], [ tick for tick in viz.get_yticks() ])

    @MultiplexTest.temporary_plot
    def test_draw_start_label_none(self):
        """
        Test that when the start label is not set, it is not drawn.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        drawn = viz.draw_population(10, 5, '')
        self.assertEqual([ ], viz.population.start_labels)

    @MultiplexTest.temporary_plot
    def test_draw_start_label_saved(self):
        """
        Test that the start label is saved in the population class.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        drawn = viz.draw_population(10, 5, '', show_start=True)
        self.assertEqual(1, len(viz.population.start_labels))

    @MultiplexTest.temporary_plot
    def test_draw_start_multiple_labels_saved(self):
        """
        Test that the start labels are all saved in the population class when drawing multiple populations.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))

        # draw the first population
        drawn = viz.draw_population(10, 5, '', show_start=True)
        self.assertEqual(1, len(viz.population.start_labels))

        # draw the second population
        drawn = viz.draw_population(10, 5, '', show_start=True)
        self.assertEqual(2, len(viz.population.start_labels))

    @MultiplexTest.temporary_plot
    def test_draw_start_label_style(self):
        """
        Test that the start label has the same style as the ticks.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        drawn = viz.draw_population(10, 5, '', show_start=True)
        self.assertEqual(1, len(viz.population.start_labels))

        # test that the style mirrors the tick style
        label = viz.population.start_labels[0]
        self.assertEqual(plt.rcParams['xtick.color'], label.style['color'])
        self.assertEqual(plt.rcParams['xtick.labelsize'], label.style['size'])

    @MultiplexTest.temporary_plot
    def test_draw_start_label_position(self):
        """
        Test that the start label is drawn next to the very first point.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        drawn = viz.draw_population(10, 5, '', show_start=True)
        self.assertEqual(1, len(viz.population.start_labels))

        # compare the position of the label with the position of the first point
        label = viz.population.start_labels[0]
        point = drawn[0][0] # first column, first point
        bb = util.get_bb(viz.figure, viz.axes, point)
        self.assertEqual(round((bb.y0 + bb.y1) / 2, 10), label.y)

    @MultiplexTest.temporary_plot
    def test_draw_start_label_positions(self):
        """
        Test that the start labels are drawn next to the very first point of their corresponding population.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))

        # draw the first population
        drawn = viz.draw_population(10, 5, '', show_start=True)
        self.assertEqual(1, len(viz.population.start_labels))

        # draw the second population
        drawn = viz.draw_population(10, 5, '', show_start=True)
        self.assertEqual(2, len(viz.population.start_labels))

        # go through each population and compare the position of the label with the position of the first point
        for label, population in zip(viz.population.start_labels, viz.population.populations):
            point = population[0][0] # first column, first point
            bb = util.get_bb(viz.figure, viz.axes, point)
            self.assertEqual(round((bb.y0 + bb.y1) / 2, 10), label.y)

    @MultiplexTest.temporary_plot
    def test_draw_legend_no_general_label(self):
        """
        Test that when no general label is given, no legend is added.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        drawn = viz.draw_population(10, 5, '', label='')
        self.assertEqual([ ], viz.legend.lines[0])

        drawn = viz.draw_population(10, 5, '', label=None)
        self.assertEqual([ ], viz.legend.lines[0])

    @MultiplexTest.temporary_plot
    def test_draw_legend_general_label(self):
        """
        Test that the general label is written correctly in the legend.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))

        label = 'Label'
        drawn = viz.draw_population(10, 5, '', label=label)
        self.assertEqual(1, len(viz.legend.lines[0]))
        point, legend = viz.legend.lines[0][0]
        self.assertEqual(label, str(legend))

    @MultiplexTest.temporary_plot
    def test_draw_legend_general_style_general_label(self):
        """
        Test that when a general style is given, it is used for the general label.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        label, color = 'Label', '#F1428A'
        drawn = viz.draw_population(10, 5, '', label=label, color=color)
        self.assertEqual(1, len(viz.legend.lines[0]))
        point, legend = viz.legend.lines[0][0]
        self.assertEqual(label, str(legend))
        self.assertEqual([241/255, 66/255, 138/255, 1], point.get_facecolor().tolist()[0])

    @MultiplexTest.temporary_plot
    def test_draw_legend_label_style_general_label(self):
        """
        Test that the label style is applied to the general label.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        label, color = 'Label', '#F1428A'
        drawn = viz.draw_population(10, 5, '', label=label, label_style={ 'color': color })
        self.assertEqual(1, len(viz.legend.lines[0]))
        _, legend = viz.legend.lines[0][0]
        self.assertEqual(label, str(legend))
        self.assertEqual(color, legend.style['color'])

    @MultiplexTest.temporary_plot
    def test_draw_legend_specific_label(self):
        """
        Test that the specific label is written correctly in the legend.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))

        labels = [ 'Label 1', 'Label 2' ]
        drawn = viz.draw_population([ { 'label': labels[0] }, { 'label': labels[1] } ], 5, '')
        self.assertEqual(2, len(viz.legend.lines[0]))

        # test the first label
        point, legend = viz.legend.lines[0][0]
        self.assertEqual(labels[0], str(legend))

        # test the second label
        point, legend = viz.legend.lines[0][1]
        self.assertEqual(labels[1], str(legend))

    @MultiplexTest.temporary_plot
    def test_draw_legend_specific_label_style(self):
        """
        Test that the specific label has the same style as its point.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))

        labels, color = [ 'Label 1', 'Label 2' ], '#F1428A'
        drawn = viz.draw_population([ { 'label': labels[0], 'color': '#FF0000' },
                                      { 'label': labels[1] } ], 5, '', color=color)
        self.assertEqual(2, len(viz.legend.lines[0]))

        # test the first label
        point, legend = viz.legend.lines[0][0]
        self.assertEqual(labels[0], str(legend))
        self.assertEqual([1, 0, 0, 1], point.get_facecolor().tolist()[0])

        # test the second label
        point, legend = viz.legend.lines[0][1]
        self.assertEqual(labels[1], str(legend))
        self.assertEqual([241/255, 66/255, 138/255, 1], point.get_facecolor().tolist()[0])

    @MultiplexTest.temporary_plot
    def test_draw_legend_specific_label_label_style(self):
        """
        Test that the label style is applied to the specific labels too.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        label, color = 'Label', '#F1428A'
        drawn = viz.draw_population([ { 'label': label }], 5, '', label_style={ 'color': color })
        self.assertEqual(1, len(viz.legend.lines[0]))
        _, legend = viz.legend.lines[0][0]
        self.assertEqual(label, str(legend))
        self.assertEqual(color, legend.style['color'])

    @MultiplexTest.temporary_plot
    def test_draw_legend_specific_label_after_general_label(self):
        """
        Test that the specific labels are drawn after the general labels.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        general, specific = 'General', 'Specific'
        drawn = viz.draw_population([ { 'label': specific }], 5, '', label=general)
        self.assertEqual(2, len(viz.legend.lines[0]))

        # test that the first label is the general label
        _, legend = viz.legend.lines[0][0]
        self.assertEqual(general, str(legend))

        # test that the second label is the specific label
        _, legend = viz.legend.lines[0][1]
        self.assertEqual(specific, str(legend))

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
        self.assertEqual((-0.75, -0.25), viz._limit(0.5))

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
