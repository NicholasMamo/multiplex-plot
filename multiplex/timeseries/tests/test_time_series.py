"""
Unit tests for the :class:`~timeseries.timeseries.TimeSeries` class.
"""

import matplotlib.pyplot as plt
import os
import pandas as pd
import sys

path = os.path.join(os.path.dirname(__file__), '..', '..')
if path not in sys.path:
	sys.path.insert(1, path)

from tests.test import MultiplexTest
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
		Test that when drawing a time series label at the end of the line, the line color is used by default.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		line_style = { 'color': '#FF0000' }
		line, label = viz.draw_time_series([ 1 ] * 5, [ 1 ] * 5, label='A',
										   **line_style, with_legend=False)

		self.assertEqual(0, len(viz.legend.lines[0]))
		self.assertEqual('A', str(label))
		self.assertEqual(line_style['color'], label.lines[0][0].get_color())

	@MultiplexTest.temporary_plot
	def test_label_style_line_override(self):
		"""
		Test that when drawing a time series label at the end of the line, the line style can override the color.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		label_style = { 'color': '#FF00FF' }
		line, label = viz.draw_time_series([ 1 ] * 5, [ 1 ] * 5, label='A',
										   label_style=label_style, with_legend=False)

		self.assertEqual(0, len(viz.legend.lines[0]))
		self.assertEqual('A', str(label))
		self.assertEqual(label_style['color'], label.lines[0][0].get_color())

	@MultiplexTest.temporary_plot
	def test_label_style_legend(self):
		"""
		Test that when drawing a time series label as a legend, the line color is not used.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		line_style = { 'color': '#FF0000' }
		line, label = viz.draw_time_series([ 1 ] * 5, [ 1 ] * 5, label='A',
										   **line_style, with_legend=True)

		self.assertEqual(1, len(viz.legend.lines[0]))
		line, label = viz.legend.lines[0][0]
		self.assertEqual('A', str(label))
		self.assertFalse(line_style['color'] == label.lines[0][0].get_color())

	@MultiplexTest.temporary_plot
	def test_draw_legend_linewidth(self):
		"""
		Test that when drawing a time series legend, the linewidth is ignored.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		line_style = { 'color': '#FF0000', 'linewidth': 1 }
		line, label = viz.draw_time_series([ 1 ] * 5, [ 1 ] * 5, label='A',
										   **line_style, with_legend=True)

		self.assertEqual(1, len(viz.legend.lines[0]))
		line, label = viz.legend.lines[0][0]
		self.assertEqual('A', str(label))
		self.assertFalse(line_style['color'] == label.lines[0][0].get_color())

	@MultiplexTest.temporary_plot
	def test_line_series(self):
		"""
		Test that if a pandas series is provided, the line points are drawn just like a list.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		label_style = { 'color': '#FF00FF' }
		x, y = range(0, 5), range(5, 10)
		line, _ = viz.draw_time_series(x, y)
		pd_line, _ = viz.draw_time_series(pd.Series(x), pd.Series(y))
		self.assertEqual(list(line.get_xdata()), list(pd_line.get_xdata()))
		self.assertEqual(list(line.get_ydata()), list(pd_line.get_ydata()))

	@MultiplexTest.temporary_plot
	def test_line_series_with_custom_index(self):
		"""
		Test that if a pandas series with a custom index is provided, the line points are drawn just like a list.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		label_style = { 'color': '#FF00FF' }
		df = pd.DataFrame()
		df['x'] = pd.Series(range(0, 5))
		df['y'] = pd.Series(range(5, 10))
		df.index = range(0, 5)
		pd_line, _ = viz.draw_time_series(df.index, df.y, label='line')
		self.assertEqual(df.x.tolist(), list(pd_line.get_xdata()))
		self.assertEqual(df.y.tolist(), list(pd_line.get_ydata()))
