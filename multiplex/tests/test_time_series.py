"""
Unit tests for the :class:`~timeseries.timeseries.TimeSeries` class.
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

class TestTimeSeries(MultiplexTest):
	"""
	Unit tests for the :class:`~timeseries.timeseries.TimeSeries` class.
	"""

	@MultiplexTest.temporary_plot
	def test_unequal_points(self):
		"""
		Test that the number of x-coordinates and y-coordinates must always be the same.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		self.assertRaises(ValueError, viz.draw_time_series, [ 1 ] * 5, [ 1 ] * 4)

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		self.assertRaises(ValueError, viz.draw_time_series, [ 1 ] * 4, [ 1 ] * 5)

	@MultiplexTest.temporary_plot
	def test_minimum_number_of_points(self):
		"""
		Test that the number of x-coordinates and y-coordinates must not be zero.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		self.assertRaises(ValueError, viz.draw_time_series, [ ], [ ])
