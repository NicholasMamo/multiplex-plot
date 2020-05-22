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

	@MultiplexTest.temporary_plot
	def test_label_style_legend(self):
		"""
		Test that when drawing a time series legend, the label style is used.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		label_style = { 'color': '#FF00FF' }
		line, label = viz.draw_time_series([ 1 ] * 5, [ 1 ] * 5, label='A',
										   label_style=label_style, with_legend=True)

		self.assertEqual(1, len(viz.legend.lines[0]))
		self.assertEqual('A', str(viz.legend.lines[0][0][1]))
		self.assertEqual(label_style['color'], viz.legend.lines[0][0][1].lines[0][0].get_color())

	@MultiplexTest.temporary_plot
	def test_label_style_line(self):
		"""
		Test that when drawing a time series legend at the end of the line, the label style is used.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		label_style = { 'color': '#FF00FF' }
		line, label = viz.draw_time_series([ 1 ] * 5, [ 1 ] * 5, label='A',
										   label_style=label_style, with_legend=False)

		self.assertEqual(0, len(viz.legend.lines[0]))
		self.assertEqual('A', str(label))
		self.assertEqual(label_style['color'], label.lines[0][0].get_color())
