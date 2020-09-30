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
import drawable, text_util, util

class TestUtil(MultiplexTest):
    """
    Unit tests for the :mod:`~text_util` module.
    """

    @MultiplexTest.temporary_plot
    def test_get_wordspacing(self):
        """
        Test that the wordspacing is based on the width of a letter.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
        figure, axes = viz.figure, viz.axes
        wordspacing = text_util.get_wordspacing(figure, axes)

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
        w1 = text_util.get_wordspacing(figure, axes)

        style = { 'fontsize': 'larger' }
        w2 = text_util.get_wordspacing(figure, axes, **style)
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
        wordspacing = text_util.get_wordspacing(figure, axes, **style)
        token = axes.text(0, 0, '—', bbox=style)
        bb = util.get_bb(figure, axes, token)
        self.assertEqual(wordspacing, bb.width / 4.)
