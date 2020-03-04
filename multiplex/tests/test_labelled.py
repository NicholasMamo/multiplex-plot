"""
Unit tests for the :class:`~labelled.LabelledVisualization` class.
"""

import matplotlib.pyplot as plt
import os
import sys

path = os.path.join(os.path.dirname(__file__), '..')
if path not in sys.path:
	sys.path.insert(1, path)

from .test import MultiplexTest
from labelled import LabelledVisualization
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

		viz = LabelledVisualization(drawable.Drawable(plt.figure(figsize=(10, 10))))
		label = viz.draw_label('A', 4, 10)
		self.assertEqual(4, label.get_virtual_bb().x0)
		self.assertEqual(10, (label.get_virtual_bb().y0 + label.get_virtual_bb().y1)/2.)

	@MultiplexTest.temporary_plot
	def test_overlapping_labels(self):
		"""
		Test that when two labels overlap, they are distributed vertically.
		"""

		viz = LabelledVisualization(drawable.Drawable(plt.figure(figsize=(10, 10))))
		label1 = viz.draw_label('A', 4, 10)
		label2 = viz.draw_label('B', 4, 10)

		self.assertEqual(label1.get_virtual_bb().x0, label2.get_virtual_bb().x0)
		self.assertFalse(util.overlapping_bb(label1.get_virtual_bb(), label2.get_virtual_bb()))
