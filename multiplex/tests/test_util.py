"""
Unit tests for the :mod:`~util` module.
"""

from matplotlib import lines
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
import os
import string
import sys

path = os.path.join(os.path.dirname(__file__), '..')
if path not in sys.path:
    sys.path.insert(1, path)

from .test import MultiplexTest
import drawable, util

class TestUtil(MultiplexTest):
    """
    Unit tests for the :mod:`~util` module.
    """

    @MultiplexTest.temporary_plot
    def test_overlapping_non_overlapping(self):
        """
        Test that when two bounding boxes do not overlap at all, they do not overlap.
        """

        bb1, bb2 = Bbox(((0, 0), (1, 1))), Bbox(((2, 2), (3, 3)))
        self.assertFalse(util.overlapping_bb(bb1, bb2))

    @MultiplexTest.temporary_plot
    def test_overlapping_corner_top_left(self):
        """
        Test that when a bounding box is at the top-left corner of another bounding box, the two do not overlap.
        """

        bb1, bb2 = Bbox(((0, 0), (1, 1))), Bbox(((-1, 1), (0, 2)))
        self.assertFalse(util.overlapping_bb(bb1, bb2))

    @MultiplexTest.temporary_plot
    def test_overlapping_corner_top_right(self):
        """
        Test that when a bounding box is at the top-right corner of another bounding box, the two do not overlap.
        """

        bb1, bb2 = Bbox(((0, 0), (1, 1))), Bbox(((1, 1), (2, 2)))
        self.assertFalse(util.overlapping_bb(bb1, bb2))

    @MultiplexTest.temporary_plot
    def test_overlapping_corner_bottom_left(self):
        """
        Test that when a bounding box is at the bottom-left corner of another bounding box, the two do not overlap.
        """

        bb1, bb2 = Bbox(((0, 0), (1, 1))), Bbox(((-1, -1), (0, 0)))
        self.assertFalse(util.overlapping_bb(bb1, bb2))

    @MultiplexTest.temporary_plot
    def test_overlapping_corner_bottom_right(self):
        """
        Test that when a bounding box is at the bottom-right corner of another bounding box, the two do not overlap.
        """

        bb1, bb2 = Bbox(((0, 0), (1, 1))), Bbox(((1, -1), (2, 0)))
        self.assertFalse(util.overlapping_bb(bb1, bb2))

    @MultiplexTest.temporary_plot
    def test_overlapping_top_border(self):
        """
        Test that when a bounding box is at the top of another bounding box, the two do not overlap.
        """

        bb1, bb2 = Bbox(((0, 0), (1, 1))), Bbox(((0, 1), (1, 2)))
        self.assertFalse(util.overlapping_bb(bb1, bb2))

    @MultiplexTest.temporary_plot
    def test_overlapping_right_border(self):
        """
        Test that when a bounding box is at the right of another bounding box, the two do not overlap.
        """

        bb1, bb2 = Bbox(((0, 0), (1, 1))), Bbox(((1, 0), (2, 1)))
        self.assertFalse(util.overlapping_bb(bb1, bb2))

    @MultiplexTest.temporary_plot
    def test_overlapping_bottom_border(self):
        """
        Test that when a bounding box is at the bottom of another bounding box, the two do not overlap.
        """

        bb1, bb2 = Bbox(((0, 0), (1, 1))), Bbox(((0, -1), (1, -2)))
        self.assertFalse(util.overlapping_bb(bb1, bb2))

    @MultiplexTest.temporary_plot
    def test_overlapping_left_border(self):
        """
        Test that when a bounding box is at the left of another bounding box, the two do not overlap.
        """

        bb1, bb2 = Bbox(((0, 0), (1, 1))), Bbox(((-1, 0), (0, 1)))
        self.assertFalse(util.overlapping_bb(bb1, bb2))

    @MultiplexTest.temporary_plot
    def test_overlapping_top(self):
        """
        Test that when a bounding box overlaps at the top of another bounding box, the function returns true.
        """

        bb1, bb2 = Bbox(((0, 0), (1, 1))), Bbox(((0, 0.5), (1, 1.5)))
        self.assertTrue(util.overlapping_bb(bb1, bb2))

    @MultiplexTest.temporary_plot
    def test_overlapping_top_left(self):
        """
        Test that when a bounding box overlaps at the top-left of another bounding box, the function returns true.
        """

        bb1, bb2 = Bbox(((0, 0), (1, 1))), Bbox(((-0.5, 0.5), (0.5, 1.5)))
        self.assertTrue(util.overlapping_bb(bb1, bb2))

    @MultiplexTest.temporary_plot
    def test_overlapping_top_right(self):
        """
        Test that when a bounding box overlaps at the top-right of another bounding box, the function returns true.
        """

        bb1, bb2 = Bbox(((0, 0), (1, 1))), Bbox(((0.5, 0.5), (1.5, 1.5)))
        self.assertTrue(util.overlapping_bb(bb1, bb2))

    @MultiplexTest.temporary_plot
    def test_overlapping_bottom_right(self):
        """
        Test that when a bounding box overlaps at the bottom-right of another bounding box, the function returns true.
        """

        bb1, bb2 = Bbox(((0, 0), (1, 1))), Bbox(((0.5, -0.5), (1.5, 0.5)))
        self.assertTrue(util.overlapping_bb(bb1, bb2))

    @MultiplexTest.temporary_plot
    def no_test_overlapping_bottom_left(self):
        """
        Test that when a bounding box overlaps at the bottom-left of another bounding box, the function returns true.
        """

        bb1, bb2 = Bbox(((0, 0), (1, 1))), Bbox(((-0.5, -0.5), (0.5, 0.5)))
        self.assertTrue(util.overlapping_bb(bb1, bb2))

    @MultiplexTest.temporary_plot
    def test_overlapping_right(self):
        """
        Test that when a bounding box overlaps at the right of another bounding box, the function returns true.
        """

        bb1, bb2 = Bbox(((0, 0), (1, 1))), Bbox(((0.5, 0), (1.5, 1)))
        self.assertTrue(util.overlapping_bb(bb1, bb2))

    @MultiplexTest.temporary_plot
    def test_overlapping_bottom(self):
        """
        Test that when a bounding box overlaps at the bottom of another bounding box, the function returns true.
        """

        bb1, bb2 = Bbox(((0, 0), (1, 1))), Bbox(((0, -0.5), (1, 0.5)))
        self.assertTrue(util.overlapping_bb(bb1, bb2))

    @MultiplexTest.temporary_plot
    def test_overlapping_left(self):
        """
        Test that when a bounding box overlaps at the left of another bounding box, the function returns true.
        """

        bb1, bb2 = Bbox(((0, 0), (1, 1))), Bbox(((-0.5, 0), (0.5, 1)))
        self.assertTrue(util.overlapping_bb(bb1, bb2))

    @MultiplexTest.temporary_plot
    def test_overlapping_exact(self):
        """
        Test that when two bounding boxes are the same, they overlap.
        """

        bb1, bb2 = Bbox(((0, 0), (1, 1))), Bbox(((0, 0), (1, 1)))
        self.assertTrue(util.overlapping_bb(bb1, bb2))

    @MultiplexTest.temporary_plot
    def test_overlapping_contains(self):
        """
        Test that when a bounding box contains the other, they overlap.
        """

        bb1, bb2 = Bbox(((0, 0), (1, 1))), Bbox(((-1, -1), (2, 2)))
        self.assertTrue(util.overlapping_bb(bb1, bb2))

    @MultiplexTest.temporary_plot
    def test_overlapping_within(self):
        """
        Test that when a bounding box is within the other, they overlap.
        """

        bb1, bb2 = Bbox(((0, 0), (1, 1))), Bbox(((0.25, 0.25), (0.75, 0.75)))
        self.assertTrue(util.overlapping_bb(bb1, bb2))

    @MultiplexTest.temporary_plot
    def test_get_bb_scatter(self):
        """
        Test that when getting the bounding box with a scatter point, the get_scatter_bb function is called.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
        figure, axes = viz.figure, viz.axes
        point = viz.scatter(0, 0, s=10)

        bb1 = util.get_scatter_bb(figure, axes, point, transform=axes.transData)
        bb2 = util.get_bb(figure, axes, point, transform=axes.transData)
        self.assertEqual(bb1.x0, bb2.x0)
        self.assertEqual(bb1.y0, bb2.y0)
        self.assertEqual(bb1.x1, bb2.x1)
        self.assertEqual(bb1.y1, bb2.y1)

    @MultiplexTest.temporary_plot
    def test_get_scatter_bb_middle_x(self):
        """
        Test that the bounding box of a scatter point is centered at the scatter point's offset.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
        figure, axes = viz.figure, viz.axes

        point = viz.scatter(0, 0, s=10)
        bb = util.get_scatter_bb(figure, axes, point, transform=axes.transData)
        self.assertEqual(0, (bb.x0 + bb.x1) / 2)

        point = viz.scatter(1, 0, s=10)
        bb = util.get_scatter_bb(figure, axes, point, transform=axes.transData)
        self.assertEqual(1, (bb.x0 + bb.x1) / 2)

    @MultiplexTest.temporary_plot
    def test_get_scatter_bb_middle_y(self):
        """
        Test that the bounding box of a scatter point is centered at the scatter point's offset.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
        figure, axes = viz.figure, viz.axes

        point = viz.scatter(0, 0, s=10)
        bb = util.get_scatter_bb(figure, axes, point, transform=axes.transData)
        self.assertEqual(0, (bb.y0 + bb.y1) / 2)

        point = viz.scatter(0, 1, s=10)
        bb = util.get_scatter_bb(figure, axes, point, transform=axes.transData)
        self.assertEqual(1, (bb.y0 + bb.y1) / 2)


    @MultiplexTest.temporary_plot
    def test_get_scatter_bb_radius_x(self):
        """
        Test that the bounding box radius of a scatter point is equal to its radius.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
        figure, axes = viz.figure, viz.axes

        s = 100
        point = viz.scatter(0, 1, s=s)
        origin = axes.transData.inverted().transform((0, 0))
        radius = (axes.transData.inverted().transform((s ** 0.5, 0))[0] - origin[0])/2.

        bb = util.get_scatter_bb(figure, axes, point, transform=axes.transData)
        self.assertEqual(round(radius, 10), round(bb.width / 2, 10))

    @MultiplexTest.temporary_plot
    def test_get_scatter_bb_radius_y(self):
        """
        Test that the bounding box radius of a scatter point is equal to its radius.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
        figure, axes = viz.figure, viz.axes

        s = 100
        point = viz.scatter(0, 1, s=s)
        origin = axes.transData.inverted().transform((0, 0))
        radius = (axes.transData.inverted().transform((0, s ** 0.5))[1] - origin[1])/2.

        bb = util.get_scatter_bb(figure, axes, point, transform=axes.transData)
        self.assertEqual(round(radius, 10), round(bb.height / 2, 10))
