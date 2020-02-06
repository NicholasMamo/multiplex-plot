"""
Unit tests for the :class:`timeseries.timeseries.TimeSeries` class.
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
	Unit tests for the :class:`timeseries.timeseries.TimeSeries` class.
	"""

	def test_invalid_annotations(self):
		"""
		Test that the number of annotations must always be the same as the number of points.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		self.assertRaises(ValueError, viz.draw_time_series, [ 1 ] * 5, [ 1 ] * 5, annotations=[ 'a' ] * 4)

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

	def test_label(self):
		"""
		Test that when a label is provided to the time series, it is added at the end.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		(line, label, _) = viz.draw_time_series([ x for x in range(0, 4) ],
												[ y for y in range(5, 9) ], 'A')
		self.assertLessEqual(3, label.get_position()[0])
		self.assertEqual(8, label.get_position()[1])

	def test_default_label_color(self):
		"""
		Test that when a label is provided to the time series without a style, the default color is the same as the line's.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		(line, label, _) = viz.draw_time_series([ x for x in range(0, 4) ],
												[ y for y in range(5, 9) ], 'A')
		self.assertEqual(line[0].get_color(), label.get_color())

	def test_label_color(self):
		"""
		Test that when a label color is provided, it is used instead of the line' color.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		(line, label, _) = viz.draw_time_series([ x for x in range(0, 4) ],
												[ y for y in range(5, 9) ],
												'A', label_style={ 'color': '#FF4477' })
		self.assertEqual('#FF4477', label.get_color())

	def test_overlapping_labels(self):
		"""
		Test that when two labels overlap, the time series distributes them.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		(line, label_1, _) = viz.draw_time_series([ x for x in range(0, 4) ],
												[ y for y in range(5, 9) ], 'A')
		(line, label_2, _) = viz.draw_time_series([ x for x in range(0, 4) ],
												[ y for y in range(5, 9) ], 'A')
		self.assertEqual(label_1.get_position()[0], label_2.get_position()[0])
		self.assertFalse(util.overlapping(viz.figure, viz.axis,
										  label_1, label_2))
