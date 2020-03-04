"""
Unit tests for the :class:`~legend.Legend` class.
"""

import matplotlib.pyplot as plt
import os
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
		self.assertEqual(annotation.get_virtual_bb().x1, viz.legend._get_offset())
