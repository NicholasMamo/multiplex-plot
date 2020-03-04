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
