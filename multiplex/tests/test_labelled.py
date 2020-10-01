"""
Unit tests for the :class:`~labelled.LabelledVisualization` class.
"""

import matplotlib.pyplot as plt
import os
import string
import sys
import time

path = os.path.join(os.path.dirname(__file__), '..')
if path not in sys.path:
    sys.path.insert(1, path)

from .test import MultiplexTest
from labelled import DummyLabelledVisualization
import drawable
import util

class TestLabelledVisualization(MultiplexTest):
    """
    Unit tests for the :class:`~labelled.LabelledVisualization` class.
    """

    @MultiplexTest.temporary_plot
    def test_label(self):
        """
        Test that when a label is drawn with normal alignment, it is drawn at the given position.
        """

        viz = DummyLabelledVisualization(drawable.Drawable(plt.figure(figsize=(10, 10))))
        label = viz.draw_label('A', 4, 10)
        self.assertEqual(4, label.get_virtual_bb().x0)
        self.assertEqual(10, (label.get_virtual_bb().y0 + label.get_virtual_bb().y1)/2.)

    @MultiplexTest.temporary_plot
    def test_overlapping_labels(self):
        """
        Test that when two labels overlap, they are distributed vertically.
        """

        viz = DummyLabelledVisualization(drawable.Drawable(plt.figure(figsize=(10, 10))))
        label1 = viz.draw_label('A', 4, 10)
        label2 = viz.draw_label('B', 4, 10)

        self.assertEqual(label1.get_virtual_bb().x0, label2.get_virtual_bb().x0)
        self.assertFalse(util.overlapping_bb(label1.get_virtual_bb(), label2.get_virtual_bb()))

    @MultiplexTest.temporary_plot
    def test_overlapping_labels_efficiency(self):
        """
        Test that when adding many labels such that they do not overlap, the function does not waste time arranging them.
        To test this, the check for the first label should approximately take as long as the check for the last label.
        """

        viz = DummyLabelledVisualization(drawable.Drawable(plt.figure(figsize=(10, 10))))

        # Add the first letter
        label = viz.draw_label(string.ascii_letters[0], 0, 0)
        # Add the second letter (for some reason the first one takes longer)
        t0 = time.time()
        label = viz.draw_label(string.ascii_letters[1], label.get_virtual_bb().x1, 0)
        t0 = time.time() - t0

        # Add all the other letters except the last one
        for letter in string.ascii_letters[2:-1]:
            label = viz.draw_label(letter, label.get_virtual_bb().x1, 0)

        # Add the last letter
        t1 = time.time()
        label = viz.draw_label(string.ascii_letters[-1], 0, 0)
        t1 = time.time() - t1
        self.assertLess(t1, t0 * 10)

    @MultiplexTest.temporary_plot
    def test_overlapping_labels_all(self):
        """
        Test that when all labels are set to overlap, at the end none of them overlap.
        """

        viz = DummyLabelledVisualization(drawable.Drawable(plt.figure(figsize=(10, 10))))

        for letter in string.ascii_letters[:10]:
            viz.draw_label(letter, 0, 0)

        for i, l1 in enumerate(viz.labels):
            for l2 in viz.labels[(i + 1):]:
                bb1, bb2 = l1.get_virtual_bb(), l2.get_virtual_bb()
                self.assertFalse(util.overlapping_bb(bb1, bb2))

    @MultiplexTest.temporary_plot
    def test_redraw_unchanged_axes(self):
        """
        Test that when redrawing without changing the axes, the labels do not move.
        """

        viz = DummyLabelledVisualization(drawable.Drawable(plt.figure(figsize=(10, 10))))
        l1 = viz.draw_label('Label 1', (0 , 1), 0)
        l2 = viz.draw_label('Label 2', (0 , 1), 1)
        pre_bb1, pre_bb2 = l1.get_virtual_bb(), l2.get_virtual_bb()
        self.assertFalse(util.overlapping_bb(pre_bb1, pre_bb2))

        # redraw and make sure that the labels did not move
        viz.redraw()
        post_bb1, post_bb2 = l1.get_virtual_bb(), l2.get_virtual_bb()
        self.assertFalse(util.overlapping_bb(post_bb1, post_bb2))

        self.assertEqual(pre_bb1.x0, post_bb1.x0)
        self.assertEqual(pre_bb1.y0, post_bb1.y0)
        self.assertEqual(pre_bb1.x1, post_bb1.x1)
        self.assertEqual(pre_bb1.y1, post_bb1.y1)

        self.assertEqual(pre_bb2.x0, post_bb2.x0)
        self.assertEqual(pre_bb2.y0, post_bb2.y0)
        self.assertEqual(pre_bb2.x1, post_bb2.x1)
        self.assertEqual(pre_bb2.y1, post_bb2.y1)

    @MultiplexTest.temporary_plot
    def test_redraw_overlapping(self):
        """
        Test that when labels that overlapped no longer overlap after redrawing.
        """

        viz = DummyLabelledVisualization(drawable.Drawable(plt.figure(figsize=(10, 10))))
        l1 = viz.draw_label('Label 1', (0 , 1), 0)
        l2 = viz.draw_label('Label 2', (0 , 1), 1)
        pre_bb1, pre_bb2 = l1.get_virtual_bb(), l2.get_virtual_bb()
        self.assertFalse(util.overlapping_bb(pre_bb1, pre_bb2))

        # increase the size of the y-axis so that the labels overlap
        viz.drawable.set_ylim((0, 100))
        post_bb1, post_bb2 = l1.get_virtual_bb(), l2.get_virtual_bb()
        self.assertTrue(util.overlapping_bb(post_bb1, post_bb2))

        # redraw and make sure that the labels did not move
        viz.redraw()
        post_bb1, post_bb2 = l1.get_virtual_bb(), l2.get_virtual_bb()
        self.assertFalse(util.overlapping_bb(post_bb1, post_bb2))
