"""
Unit tests for the :class:`~Drawable` class.
"""

import matplotlib.pyplot as plt
import os
import sys

path = os.path.join(os.path.dirname(__file__), '..')
if path not in sys.path:
    sys.path.insert(1, path)

from .test import MultiplexTest
import drawable, text, util

class TestDrawable(MultiplexTest):
    """
    Unit tests for the :class:`~Drawable` class.
    """

    @MultiplexTest.temporary_plot
    def test_init_secondary_copy(self):
        """
        Test that by default, the secondary axes is a copy of the primary axes.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
        self.assertEqual(viz.axes, viz.secondary)

    @MultiplexTest.temporary_plot
    def test_caption(self):
        """
        Test that the caption is set correctly.
        """

        text = 'caption.'

        viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
        caption = viz.set_caption(text)
        self.assertEqual(text, str(caption))

    @MultiplexTest.temporary_plot
    def test_caption_removes_multiple_spaces(self):
        """
        Test that the caption preprocessing removes multiple consecutive spaces.
        """

        text = """
            This is a multi-level   caption.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
        caption = viz.set_caption(text)
        self.assertEqual('This is a multi-level caption.', str(caption))

    @MultiplexTest.temporary_plot
    def test_caption_removes_tabs(self):
        """
        Test that the caption preprocessing removes tabs.
        """

        text = """
            This is a multi-level    caption.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
        caption = viz.set_caption(text)
        self.assertEqual('This is a multi-level caption.', str(caption))

    @MultiplexTest.temporary_plot
    def test_redraw_bottom_xaxes(self):
        """
        Test that when the x-axis label is at the bottom, the caption is at y=1.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
        caption = viz.set_caption("sample caption")
        caption_bb = caption.get_virtual_bb(transform=viz.axes.transAxes)
        self.assertEqual(1.1, round(caption_bb.y0, 10))

    @MultiplexTest.temporary_plot
    def test_redraw_top_xaxes(self):
        """
        Test that when the x-axis label is at the top, the caption moves up.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
        caption = viz.set_caption("sample caption")
        caption_bb = caption.get_virtual_bb(transform=viz.axes.transAxes)
        self.assertFalse(util.overlapping_bb(caption_bb, viz._get_xlabel(transform=viz.axes.transAxes)))

        """
        Move the x-axis label and ticks to the top.
        """
        viz.axes.xaxis.set_label_position('top')
        viz.axes.xaxis.tick_top()
        viz.axes.spines['top'].set_visible(True)
        viz.axes.spines['bottom'].set_visible(False)

        """
        After adding a label, the caption should move up.
        """
        viz.set_xlabel('label')
        viz.redraw()
        self.assertLess(caption_bb.y0, viz.caption.get_virtual_bb(transform=viz.axes.transAxes).y0)

    @MultiplexTest.temporary_plot
    def test_annotate_returns_annotation(self):
        """
        Test that the annotate function returns an annotation.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
        annotation = viz.annotate('Text', 0, 0)
        self.assertEqual(text.annotation.Annotation, type(annotation))

    @MultiplexTest.temporary_plot
    def test_annotate_marker_copy(self):
        """
        Test that when drawing a marker and a marker style is given as a dictionary, it is not overwritten.
        """

        marker = { }
        annotation_style = { 'color': 'blue' }

        viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
        viz.annotate('Text', (0, 0), 0, marker=marker, **annotation_style)
        viz.redraw()
        self.assertEqual({ }, marker)

    @MultiplexTest.temporary_plot
    def test_annotate_redraws(self):
        """
        Test that the drawable draws the canvas before creating an annotation.
        """

        annotation_style = { 'color': 'blue' }

        viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
        viz.draw_time_series(range(0, 10), range(0, 10)) # draw a time series to cramp the area
        annotation = viz.annotate('Text with multiple words', (0, 0), 0, **annotation_style)
        viz.redraw()
        tokens = [ token for line in annotation.lines
                         for token in line ]
        self.assertTrue(tokens)
        for i, t1 in enumerate(tokens):
            for j, t2 in enumerate(tokens[(i + 1):]):
                self.assertFalse(util.overlapping(viz.figure, viz.axes, t1, t2))
