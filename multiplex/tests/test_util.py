"""
Unit tests for the :mod:`~util` module.
"""

from matplotlib import lines
import matplotlib.pyplot as plt
import os
import string
import sys

path = os.path.join(os.path.dirname(__file__), '..')
if path not in sys.path:
    sys.path.insert(1, path)

from .test import MultiplexTest
import drawable
import util

class TestUtil(MultiplexTest):
    """
    Unit tests for the :mod:`~util` module.
    """

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

    @MultiplexTest.temporary_plot
    def test_get_wordspacing(self):
        """
        Test that the wordspacing is based on the width of a letter.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
        figure, axes = viz.figure, viz.axes
        wordspacing = util.get_wordspacing(figure, axes)

        token = axes.text(0, 0, '—')
        bb = util.get_bb(figure, axes, token)
        self.assertEqual(wordspacing, bb.width / 4.)

    @MultiplexTest.temporary_plot
    def test_get_wordspacing_with_style(self):
        """
        Test that the wordspacing considers the style of the token.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
        figure, axes = viz.figure, viz.axes
        w1 = util.get_wordspacing(figure, axes)

        style = { 'fontsize': 'larger' }
        w2 = util.get_wordspacing(figure, axes, **style)
        token = axes.text(0, 0, '—', **style)
        bb = util.get_bb(figure, axes, token)
        self.assertEqual(w2, bb.width / 4.)

        self.assertGreater(w2, w1)

    @MultiplexTest.temporary_plot
    def test_get_wordspacing_with_bbox_style(self):
        """
        Test that the wordspacing considers the style of the token's bounding box.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
        figure, axes = viz.figure, viz.axes

        style = { 'pad': 0.5 }
        wordspacing = util.get_wordspacing(figure, axes, **style)
        token = axes.text(0, 0, '—', bbox=style)
        bb = util.get_bb(figure, axes, token)
        self.assertEqual(wordspacing, bb.width / 4.)
