"""
Unit tests for the :class:`~legend.Legend` class.
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

class TestLegend(MultiplexTest):
	"""
	Unit tests for the :class:`~legend.Legend` class.
	"""

	@MultiplexTest.temporary_plot
	def test_visual_annotation_do_not_overlap(self):
		"""
		Test that when drawing a legend, the visual and the annotation do not overlap.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		line, annotation = viz.legend.draw_line('A')
		linebb = util.get_bb(viz.figure, viz.axis, line)
		self.assertFalse(util.overlapping_bb(linebb, annotation.get_virtual_bb()))

	@MultiplexTest.temporary_plot
	def test_offset_new_legend(self):
		"""
		Test that when getting the offset of an empty legend, the offset returned is 0.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		self.assertEqual(0, viz.legend._get_offset())

	@MultiplexTest.temporary_plot
	def test_offset_legend(self):
		"""
		Test that when getting the offset of a legend with one component, the offset returned is beyond that component.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		line, annotation = viz.legend.draw_line('A')
		self.assertEqual(annotation.get_virtual_bb().x1, viz.legend._get_offset(pad=0))

	@MultiplexTest.temporary_plot
	def test_offset_pad_new_legend(self):
		"""
		Test that when getting the offset of an empty legend, the offset returned has no padding applied to it.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		self.assertEqual(0, viz.legend._get_offset())

	@MultiplexTest.temporary_plot
	def test_offset_pad_legend(self):
		"""
		Test that when getting the offset of a legend with one component, the offset returned has padding applied to it.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		line, annotation = viz.legend.draw_line('A')
		self.assertEqual(annotation.get_virtual_bb().x1 + 0.025, viz.legend._get_offset(pad=0.025))

	@MultiplexTest.temporary_plot
	def test_new_line(self):
		"""
		Test that when creating a new line, the legend starts at x-coordinate 0.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		line, annotation = viz.legend.draw_line('A')

		new_line = lines.Line2D([ 0.95, 1], [ 1, 1 ])
		new_annotation = viz.legend.draw_annotation('B', 1, 1)
		viz.legend._newline(new_line, new_annotation, new_annotation.get_virtual_bb().height)
		self.assertEqual(0, new_line.get_xdata()[0])

	@MultiplexTest.temporary_plot
	def test_new_line_overlap(self):
		"""
		Test that when creating a new line, the lines do not overlap.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		for label in string.ascii_uppercase:
			line, annotation = viz.legend.draw_line(label)
		self.assertGreaterEqual(len(viz.legend.lines), 2)

		"""
		Compare the top annotation with the one beneath it.
		"""
		for i in range(len(viz.legend.lines) -1):
			top = viz.legend.lines[i][0][1]
			bottom = viz.legend.lines[i + 1][0][1]
			self.assertLessEqual(bottom.get_virtual_bb().y1, top.get_virtual_bb().y0)
