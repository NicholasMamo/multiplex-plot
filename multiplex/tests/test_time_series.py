"""
Unit tests for the :class:`~timeseries.timeseries.TimeSeries` class.
"""

import matplotlib.pyplot as plt
import os
import sys
import unittest

path = os.path.join(os.path.dirname(__file__), '..')
if path not in sys.path:
	sys.path.insert(1, path)

import drawable
import util

class TestTimeSeries(unittest.TestCase):
	"""
	Unit tests for the :class:`~timeseries.timeseries.TimeSeries` class.
	"""

	def test_unequal_points(self):
		"""
		Test that the number of x-coordinates and y-coordinates must always be the same.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		self.assertRaises(ValueError, viz.draw_time_series, [ 1 ] * 5, [ 1 ] * 4)

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		self.assertRaises(ValueError, viz.draw_time_series, [ 1 ] * 4, [ 1 ] * 5)

	def test_minimum_number_of_points(self):
		"""
		Test that the number of x-coordinates and y-coordinates must not be zero.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		self.assertRaises(ValueError, viz.draw_time_series, [ ], [ ])
