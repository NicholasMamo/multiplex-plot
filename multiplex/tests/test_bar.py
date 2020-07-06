"""
Unit tests for the :class:`~bar.100.Bar100` class.
"""

import matplotlib.pyplot as plt
import os
import pandas as pd
import sys

path = os.path.join(os.path.dirname(__file__), '..')
if path not in sys.path:
	sys.path.insert(1, path)

from .test import MultiplexTest
from bar.bar100 import Bar100
import drawable
import util

class TestBar100(MultiplexTest):
	"""
	Unit tests for the :class:`~bar.100.Bar100` class.
	"""

	@MultiplexTest.temporary_plot
	def test_draw_empty_values(self):
		"""
		Test that when drawing an empty list of values, a ValueError is raised.
		"""
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		self.assertRaises(ValueError, viz.draw_bar_100, [ ])

	@MultiplexTest.temporary_plot
	def test_draw_all_values_zero(self):
		"""
		Test that when drawing a list made up of only zeroes, a ValueError is raised.
		"""
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		self.assertRaises(ValueError, viz.draw_bar_100, [ 0 ])
		self.assertRaises(ValueError, viz.draw_bar_100, [ 0 ] * 10)

	@MultiplexTest.temporary_plot
	def test_draw_negative_values(self):
		"""
		Test that when drawing a list that includes negative values, a ValueError is raised.
		"""
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		self.assertRaises(ValueError, viz.draw_bar_100, [ -1 ])
		self.assertRaises(ValueError, viz.draw_bar_100, [ 1, -1 ])

	@MultiplexTest.temporary_plot
	def test_to_100_empty_values(self):
		"""
		Test that when no values are given to be converted to percentages, an empty list is returned again.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertEqual([ ], bar._to_100([ ]))

	@MultiplexTest.temporary_plot
	def test_to_100_zero_values(self):
		"""
		Test that when zero values are given to be converted to percentages, the same list is returned.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertEqual([ 0, 0 ], bar._to_100([ 0, 0 ]))

	@MultiplexTest.temporary_plot
	def test_to_100_add_up_to_100(self):
		"""
		Test that when converting values to percentages, the returned percentages add up to 100%.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertEqual(100, sum(bar._to_100([ 10 ] * 3)))

	@MultiplexTest.temporary_plot
	def test_to_100_same_order(self):
		"""
		Test that when converting values to percentages, the percentages are returned in the same order as the input.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = [ 10, 20, 30 ]
		percentages = bar._to_100(values)
		self.assertEqual(100, sum(percentages))
		self.assertLess(percentages[0], percentages[1])
		self.assertLess(percentages[1], percentages[2])

	@MultiplexTest.temporary_plot
	def test_to_100_same_number(self):
		"""
		Test that when converting values to percentages, the same number of percentages as values are returned.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = [ 10, 20, 30 ] * 123
		percentages = bar._to_100(values)
		self.assertEqual(len(values), len(percentages))
