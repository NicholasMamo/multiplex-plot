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
			This is a multi-level	caption.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		caption = viz.set_caption(text)
		self.assertEqual('This is a multi-level caption.', str(caption))

	@MultiplexTest.temporary_plot
	def test_redraw_bottom_xaxis(self):
		"""
		Test that when the x-axis label is at the bottom, the caption is at y=1.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		caption = viz.set_caption("sample caption")
		caption_bb = caption.get_virtual_bb(transform=viz.axis.transAxes)
		self.assertEqual(1, caption_bb.y0)

	@MultiplexTest.temporary_plot
	def test_redraw_top_xaxis(self):
		"""
		Test that when the x-axis label is at the top, the caption moves up.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		caption = viz.set_caption("sample caption")
		caption_bb = caption.get_virtual_bb(transform=viz.axis.transAxes)
		self.assertFalse(util.overlapping_bb(caption_bb, viz._get_xlabel(transform=viz.axis.transAxes)))

		"""
		Move the x-axis label and ticks to the top.
		"""
		viz.axis.xaxis.set_label_position('top')
		viz.axis.xaxis.tick_top()
		viz.axis.spines['top'].set_visible(True)
		viz.axis.spines['bottom'].set_visible(False)

		"""
		After adding a label, the caption should move up.
		"""
		viz.set_xlabel('label')
		viz.redraw()
		self.assertLess(caption_bb.y0, viz.caption.get_virtual_bb(transform=viz.axis.transAxes).y0)

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
		self.assertEqual({ }, marker)
