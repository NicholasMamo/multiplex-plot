"""
Unit tests for the :class:`~bar.100.Bar100` class.
"""

import matplotlib
import matplotlib.pyplot as plt
import os
import pandas as pd
import sys

path = os.path.join(os.path.dirname(__file__), '..', '..')
if path not in sys.path:
	sys.path.insert(1, path)

from tests.test import MultiplexTest
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
		self.assertRaises(ValueError, viz.draw_bar_100, [ ], 'label')

	@MultiplexTest.temporary_plot
	def test_draw_all_values_zero(self):
		"""
		Test that when drawing a list made up of only zeroes, a ValueError is raised.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		self.assertRaises(ValueError, viz.draw_bar_100, [ 0 ], 'label')
		self.assertRaises(ValueError, viz.draw_bar_100, [ 0 ] * 10, 'label')

	@MultiplexTest.temporary_plot
	def test_draw_negative_values(self):
		"""
		Test that when drawing a list that includes negative values, a ValueError is raised.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		self.assertRaises(ValueError, viz.draw_bar_100, [ -1 ], 'label')
		self.assertRaises(ValueError, viz.draw_bar_100, [ 1, -1 ], 'label')

	@MultiplexTest.temporary_plot
	def test_draw_all_dict_values_zero(self):
		"""
		Test that when drawing a dictionary list made up of only zeroes, a ValueError is raised.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		self.assertRaises(ValueError, viz.draw_bar_100, [ { 'value': 0 } ], 'label')
		self.assertRaises(ValueError, viz.draw_bar_100, [ { 'value': 0 } ] * 10, 'label')

	@MultiplexTest.temporary_plot
	def test_draw_negative_dict_values(self):
		"""
		Test that when drawing a dictionary list that includes negative values, a ValueError is raised.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		self.assertRaises(ValueError, viz.draw_bar_100, [ { 'value': -1 } ], 'label')
		self.assertRaises(ValueError, viz.draw_bar_100, [ { 'value': 1 }, { 'value': -1 } ], 'label')

	@MultiplexTest.temporary_plot
	def test_draw_min_percentage_below_0(self):
		"""
		Test that when the minimum percentage is below 0, drawing raises a ValueError.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertRaises(ValueError, bar.draw, [ 1 ], 'label', min_percentage=-1)

	@MultiplexTest.temporary_plot
	def test_draw_min_percentage_0(self):
		"""
		Test that when the minimum percentage is 0, drawing does not raise a ValueError.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertTrue(bar.draw([ 1 ], 'label', min_percentage=0))

	@MultiplexTest.temporary_plot
	def test_draw_min_percentage_100(self):
		"""
		Test that when the minimum percentage is 100, drawing does not raise a ValueError.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertTrue(bar.draw([ 1 ], 'label', min_percentage=100))

	@MultiplexTest.temporary_plot
	def test_draw_min_percentage_above_100(self):
		"""
		Test that when the minimum percentage is above 100, drawing raises a ValueError.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertRaises(ValueError, bar.draw, [ 1 ], 'label', min_percentage=101)

	@MultiplexTest.temporary_plot
	def test_draw_min_percentage_exceeds_100(self):
		"""
		Test that when the minimum percentage multiplied by the number of values exceeds 100, drawing raises a ValueError.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertRaises(ValueError, bar.draw, [ 1, 1 ], 'label', min_percentage=75)

	@MultiplexTest.temporary_plot
	def test_draw_empty_label(self):
		"""
		Test that when drawing bars, the label cannot be empty.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertRaises(ValueError, bar.draw, [ 1, 1 ], '')

	@MultiplexTest.temporary_plot
	def test_draw_add_labels(self):
		"""
		Test that when drawing bars, the label is also drawn.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		bar.draw([ 1, 1 ], 'bar 1')
		self.assertEqual(1, len(viz.get_yticklabels()))
		self.assertEqual('bar 1', viz.get_yticklabels()[0].get_text())

	@MultiplexTest.temporary_plot
	def test_draw_name_order(self):
		"""
		Test that when drawing bars, the names are drawn in the correct order.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)

		"""
		Draw the first bar.
		"""
		bar.draw([ 1, 1 ], 'bar 1')
		self.assertEqual(1, len(viz.get_yticklabels()))
		self.assertEqual('bar 1', viz.get_yticklabels()[-1].get_text())

		"""
		Draw the second bar.
		"""
		bar.draw([ 1, 1 ], 'bar 2')
		self.assertEqual(2, len(viz.get_yticklabels()))
		self.assertEqual('bar 2', viz.get_yticklabels()[-1].get_text())

	@MultiplexTest.temporary_plot
	def test_draw_override_pad(self):
		"""
		Test that when drawing bars, padding can be overriden through the style.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = [ { 'value': 10 }, { 'value': 10, 'style': { } },
				   { 'value': 10, 'style': { 'pad': 0 } }, { 'value': 10 } ]
		bars = bar.draw(values, 'label', pad=1)
		self.assertEqual(24, round(util.get_bb(viz.figure, viz.axes, bars[1]).width, 10))
		self.assertEqual(25, round(util.get_bb(viz.figure, viz.axes, bars[2]).width, 10))

	@MultiplexTest.temporary_plot
	def test_draw_legend_no_labels(self):
		"""
		Test that when providing no labels, the legend remains empty.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = list(range(10))
		bars = bar.draw(values, 'label')
		self.assertEqual(0, len(viz.legend.lines[0]))

	@MultiplexTest.temporary_plot
	def test_draw_legend_labels(self):
		"""
		Test that when providing labels, they are drawn in the legend.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = [ { 'value': 10, 'label': 'A' }, { 'value': 10, 'label': 'B' },
				   { 'value': 10, 'label': 'C' }, { 'value': 10, 'label': 'D' } ]
		bars = bar.draw(values, 'label')
		self.assertEqual(4, len(viz.legend.lines[0]))
		self.assertEqual([ 'A', 'B', 'C', 'D' ],
						 [ str(annotation) for _, annotation in viz.legend.lines[0] ])

	@MultiplexTest.temporary_plot
	def test_draw_legend_labels_empty(self):
		"""
		Test that when providing empty or `None` labels, they are not drawn in the legend.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = [ { 'value': 10, 'label': None }, { 'value': 10, 'label': '' } ]
		bars = bar.draw(values, 'label')
		self.assertEqual(0, len(viz.legend.lines[0]))

	@MultiplexTest.temporary_plot
	def test_draw_legend_repeated_labels(self):
		"""
		Test that when providing repeated labels, only the first one is drawn.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = [ { 'value': 10, 'label': 'A' }, { 'value': 10, 'label': 'B' },
				   { 'value': 10, 'label': 'C' }, { 'value': 10, 'label': 'A' } ]
		bars = bar.draw(values, 'label')
		self.assertEqual(3, len(viz.legend.lines[0]))
		self.assertEqual([ 'A', 'B', 'C' ],
						 [ str(annotation) for _, annotation in viz.legend.lines[0] ])

	@MultiplexTest.temporary_plot
	def test_draw_legend_inherits_general_bar_style(self):
		"""
		Test that the legend labels inherit the general bar style.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = [ { 'value': 10, 'label': 'label' } ]
		bars = bar.draw(values, 'label', color='#FF0000')
		self.assertEqual(1, len(viz.legend.lines[0]))
		_, annotation = viz.legend.lines[0][0]
		self.assertEqual('#FF0000', annotation.lines[0][0].get_color())

	@MultiplexTest.temporary_plot
	def test_draw_legend_bar_style_overrides_general_bar_style(self):
		"""
		Test that drawing legend labels, the bar style overrides the general bar style.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = [ { 'value': 10, 'label': 'label' },
				   { 'value': 10, 'label': 'another', 'style': { 'color': '#00FF00' } } ]
		bars = bar.draw(values, 'label', color='#FF0000')
		self.assertEqual(2, len(viz.legend.lines[0]))
		_, annotation = viz.legend.lines[0][0]
		self.assertEqual('#FF0000', annotation.lines[0][0].get_color())
		_, annotation = viz.legend.lines[0][1]
		self.assertEqual('#00FF00', annotation.lines[0][0].get_color())

	@MultiplexTest.temporary_plot
	def test_draw_legend_label_style_overrides_bar_style(self):
		"""
		Test that drawing legend labels, the label style overrides the bar style.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = [ { 'value': 10, 'label': 'label' },
				   { 'value': 10, 'label': 'another', 'style': { 'color': '#00FF00' } } ]
		label_style = { 'color': '#0000FF' }
		bars = bar.draw(values, 'label', color='#FF0000', label_style=label_style)
		self.assertEqual(2, len(viz.legend.lines[0]))
		_, annotation = viz.legend.lines[0][0]
		self.assertEqual('#0000FF', annotation.lines[0][0].get_color())
		_, annotation = viz.legend.lines[0][1]
		self.assertEqual('#0000FF', annotation.lines[0][0].get_color())

	@MultiplexTest.temporary_plot
	def test_draw_legend_bar_label_style_overrides_label_style(self):
		"""
		Test that drawing legend labels, the bar's specific label style overrides the general label style.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = [ { 'value': 10, 'label': 'label' },
				   { 'value': 10, 'label': 'another', 'style': { 'color': '#00FF00' }, 'label_style': { 'color': '#FFFF00' } } ]
		label_style = { 'color': '#0000FF' }
		bars = bar.draw(values, 'label', color='#FF0000', label_style=label_style)
		self.assertEqual(2, len(viz.legend.lines[0]))
		_, annotation = viz.legend.lines[0][0]
		self.assertEqual('#0000FF', annotation.lines[0][0].get_color())
		_, annotation = viz.legend.lines[0][1]
		self.assertEqual('#FFFF00', annotation.lines[0][0].get_color())

	@MultiplexTest.temporary_plot
	def test_draw_legend_inherit_not_overriden(self):
		"""
		Test that drawing legend labels, any value that is not overriden is inherited.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = [ { 'value': 10, 'label': 'label' },
				   { 'value': 10, 'label': 'another', 'style': { 'color': '#00FF00' }, 'label_style': { 'color': '#FFFF00' } } ]
		label_style = { 'color': '#0000FF', 'alpha': 0.5 }
		bars = bar.draw(values, 'label', color='#FF0000', label_style=label_style)
		self.assertEqual(2, len(viz.legend.lines[0]))
		_, annotation = viz.legend.lines[0][0]
		self.assertEqual('#0000FF', annotation.lines[0][0].get_color())
		self.assertEqual(0.5, annotation.lines[0][0].get_alpha())
		_, annotation = viz.legend.lines[0][1]
		self.assertEqual('#FFFF00', annotation.lines[0][0].get_color())
		self.assertEqual(0.5, annotation.lines[0][0].get_alpha())

	@MultiplexTest.temporary_plot
	def test_draw_legend_ignores_pad(self):
		"""
		Test that drawing legend labels, the label style ignores the padding style.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = [ { 'value': 10, 'label': 'label' },
				   { 'value': 10, 'label': 'another', 'style': { 'pad': 0 } } ]
		bars = bar.draw(values, 'label', color='#FF0000')
		self.assertEqual(2, len(viz.legend.lines[0]))
		_, annotation = viz.legend.lines[0][0]
		self.assertEqual('#FF0000', annotation.lines[0][0].get_color())
		_, annotation = viz.legend.lines[0][1]
		self.assertEqual('#FF0000', annotation.lines[0][0].get_color())

	@MultiplexTest.temporary_plot
	def test_to_dict_all_floats_default_value(self):
		"""
		Test that when converting a list of floats to a dictionary, their values are all retained.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = list(range(0, 10))
		dicts = bar._to_dict(values)
		self.assertEqual(values, [ value['value'] for value in dicts ])

	@MultiplexTest.temporary_plot
	def test_to_dict_all_floats_default_style(self):
		"""
		Test that when converting a list of floats to a dictionary, an empty style is added.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = list(range(0, 10))
		dicts = bar._to_dict(values)
		self.assertEqual([ { } ] * 10, [ value['style'] for value in dicts ])

	@MultiplexTest.temporary_plot
	def test_to_dict_all_dicts_default_value(self):
		"""
		Test that when converting a list of dictionaries to a dictionary, their default value is 0.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = [ { }, { 'value': 3 } ]
		dicts = bar._to_dict(values)
		self.assertEqual([ 0, 3 ], [ value['value'] for value in dicts ])

	@MultiplexTest.temporary_plot
	def test_to_dict_all_dicts_default_style(self):
		"""
		Test that when converting a list of dictionaries to a dictionary, their default style is an empty dictionary if they do not have a style already.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = [ { }, { 'style': { 'color': 'red' } } ]
		dicts = bar._to_dict(values)
		self.assertEqual([ { }, { 'color': 'red' } ], [ value['style'] for value in dicts ])

	@MultiplexTest.temporary_plot
	def test_to_dict_mix(self):
		"""
		Test converting a mixed list of floats and dictionaries to a dictionary.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = [ 10, { 'value': 5 }, { 'style': { 'color': 'red' } },
				   { 'value': 2 ,  'style': { 'color': 'blue' } } ]
		dicts = bar._to_dict(values)
		self.assertEqual([ 10, 5, 0, 2 ], [ value['value'] for value in dicts ])
		self.assertEqual([ { }, { }, { 'color': 'red' }, { 'color': 'blue' } ],
						 [ value['style'] for value in dicts ])

	@MultiplexTest.temporary_plot
	def test_to_dict_other_keys(self):
		"""
		Test that when converting values to dictionaries, any additional keys are retained.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = [ { 'value': 2 ,  'style': { 'color': 'blue' }, 'other': 23 } ]
		dicts = bar._to_dict(values)
		self.assertTrue('other' in dicts[0])
		self.assertEqual(23, dicts[0]['other'])

	@MultiplexTest.temporary_plot
	def test_draw_bars_0(self):
		"""
		Test that when drawing bars, they all start at 0.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = bar._to_dict(list(range(10)))
		bars = bar._draw_bars(values)
		self.assertEqual(0, util.get_bb(viz.figure, viz.axes, bars[0]).x0)

	@MultiplexTest.temporary_plot
	def test_draw_bars_0_pad(self):
		"""
		Test that when drawing bars, they all start at 0 even when padding is given.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = bar._to_dict(list(range(10)))
		bars = bar._draw_bars(values, pad=1)
		self.assertEqual(0, util.get_bb(viz.figure, viz.axes, bars[0]).x0)

	@MultiplexTest.temporary_plot
	def test_draw_bars_100(self):
		"""
		Test that when drawing bars, they all end at 100.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = bar._to_dict(list(range(10)))
		bars = bar._draw_bars(values)
		self.assertEqual(100, round(util.get_bb(viz.figure, viz.axes, bars[-1]).x1, 7))

	@MultiplexTest.temporary_plot
	def test_draw_bars_100_pad(self):
		"""
		Test that when drawing bars, they all end at 100 even when padding is given.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = bar._to_dict(list(range(10)))
		bars = bar._draw_bars(values, pad=1)
		self.assertEqual(100, round(util.get_bb(viz.figure, viz.axes, bars[-1]).x1, 7))

	@MultiplexTest.temporary_plot
	def test_draw_bars_percentages(self):
		"""
		Test that when drawing bars, their width equals their percentages.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = list(range(10))
		percentages = bar._to_100(values)
		bars = bar._draw_bars(bar._to_dict(values))
		for percentage, bar in zip(percentages, bars):
			self.assertEqual(round(percentage, 7), round(util.get_bb(viz.figure, viz.axes, bar).width, 7))

	@MultiplexTest.temporary_plot
	def test_draw_bars_no_overlap(self):
		"""
		Test that when drawing bars, none of them overlap.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = bar._to_dict(list(range(10)))
		bars = bar._draw_bars(values)
		for i in range(0, len(bars)):
			for j in range(i + 1, len(bars)):
				self.assertFalse(util.overlapping(viz.figure, viz.axes, bars[i], bars[j]))

	@MultiplexTest.temporary_plot
	def test_draw_bars_no_overlap_pad(self):
		"""
		Test that when drawing bars, none of them overlap even with padding.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = bar._to_dict(list(range(10)))
		bars = bar._draw_bars(values, pad=1)
		for i in range(0, len(bars)):
			for j in range(i + 1, len(bars)):
				self.assertFalse(util.overlapping(viz.figure, viz.axes, bars[i], bars[j]))

	@MultiplexTest.temporary_plot
	def test_draw_bars_return_rectangles(self):
		"""
		Test that when drawing bars, they are returned as matplotlib rectangles.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = bar._to_dict(list(range(10)))
		bars = bar._draw_bars(values)
		self.assertTrue(bars)
		self.assertTrue(all( matplotlib.patches.Rectangle == type(bar) for bar in bars ))

	@MultiplexTest.temporary_plot
	def test_draw_bars_min_percentage(self):
		"""
		Test that when drawing bars, the minimum percentage is respected.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = bar._to_dict([ 0, 1, 2, 3 ])
		bars = bar._draw_bars(values, min_percentage=10)
		self.assertTrue(all( round(util.get_bb(viz.figure, viz.axes, bar).width, 10) >= 10 for bar in bars ))

	@MultiplexTest.temporary_plot
	def test_draw_bars_override_style(self):
		"""
		Test that when drawing bars, the style can be overriden.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = bar._to_dict([{ 'value': 10, 'style': { 'color': '#0000FF' } }, { 'value': 10 }])
		bars = bar._draw_bars(values, color='#FF0000')
		self.assertEqual(bars[0].get_facecolor(), (0, 0, 1, 1))
		self.assertEqual(bars[1].get_facecolor(), (1, 0, 0, 1))

	@MultiplexTest.temporary_plot
	def test_draw_bars_inherit_style(self):
		"""
		Test that when drawing bars, style options that are not overriden are inherited.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		values = bar._to_dict([{ 'value': 10, 'style': { 'alpha': 0.5 } },
							   { 'value': 10 }])
		bars = bar._draw_bars(values, color='#FF0000', alpha=1)
		self.assertTrue(all(bar.get_facecolor() == (1, 0, 0, 1)) for bar in bars)
		self.assertEqual(bars[0].get_alpha(), 0.5)
		self.assertEqual(bars[1].get_alpha(), 1)

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

	@MultiplexTest.temporary_plot
	def test_to_100_min_percentage_below_0(self):
		"""
		Test that when the minimum percentage is below 0, percentage conversion raises a ValueError.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertRaises(ValueError, bar._to_100, [ 1 ], -1)

	@MultiplexTest.temporary_plot
	def test_to_100_min_percentage_0(self):
		"""
		Test that when the minimum percentage is 0, percentage conversion does not raise a ValueError.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertTrue(bar._to_100([ 1 ], 0))

	@MultiplexTest.temporary_plot
	def test_to_100_min_percentage_100(self):
		"""
		Test that when the minimum percentage is 100, percentage conversion does not raise a ValueError.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertTrue(bar._to_100([ 1 ], 100))

	@MultiplexTest.temporary_plot
	def test_to_100_min_percentage_above_100(self):
		"""
		Test that when the minimum percentage is above 100, percentage conversion raises a ValueError.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertRaises(ValueError, bar._to_100, [ 1 ], 101)

	@MultiplexTest.temporary_plot
	def test_to_100_min_percentage_exceeds_100(self):
		"""
		Test that when the minimum percentage multiplied by the number of values exceeds 100, percentage conversion raises a ValueError.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertRaises(ValueError, bar._to_100, [ 1, 1 ], 75)

	@MultiplexTest.temporary_plot
	def test_to_100_min_percentage_equals_100(self):
		"""
		Test that when the minimum percentage multiplied by the number of values is equal to 100, percentage conversion does not raise a ValueError.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertTrue(bar._to_100([ 1, 1 ], 50))

	@MultiplexTest.temporary_plot
	def test_to_100_min_percentage_sums_100(self):
		"""
		Test that when converting values to percentages with a minimum percentage, the values still add up to 100%.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertEqual(100, sum(bar._to_100([ 1, 2 ], 50)))

	@MultiplexTest.temporary_plot
	def test_to_100_min_percentage_no_zero(self):
		"""
		Test that when converting values to percentages with a minimum percentage, no value is 0.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertFalse(any( percentage == 0 for percentage in bar._to_100([ 1, 0, 1 ], 10)))

	@MultiplexTest.temporary_plot
	def test_to_100_min_percentage(self):
		"""
		Test that when providing a minimum percentage, all returned percentages meet that value.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertTrue(all( round(percentage, 10) >= 10 for percentage in bar._to_100([ 1, 0, 1 ], 10) ))

	@MultiplexTest.temporary_plot
	def test_to_100_fold(self):
		"""
		Test that when providing a minimum percentage that fills up the bar, all returned values are the same.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertTrue(all( round(percentage, 7) == round(1/3 * 100, 7)
							 for percentage in bar._to_100([ 10, 0, 5 ], 1/3 * 100) ))

	@MultiplexTest.temporary_plot
	def test_pad_percentage_below_0(self):
		"""
		Test that when the percentage is below 0, padding raises a ValueError.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertRaises(ValueError, bar._pad, -1, 0, 0)

	@MultiplexTest.temporary_plot
	def test_pad_percentage_0(self):
		"""
		Test that when the percentage is 0, padding does not raise a ValueError.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertEqual(0, bar._pad(10, 0, 0))

	@MultiplexTest.temporary_plot
	def test_pad_percentage_100(self):
		"""
		Test that when the percentage is 100, padding does not raise a ValueError.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertEqual(0, bar._pad(100, 0, 0))

	@MultiplexTest.temporary_plot
	def test_pad_percentage_above_100(self):
		"""
		Test that when the percentage is above 100, padding raises a ValueError.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertRaises(ValueError, bar._pad, 101, 0, 0)

	@MultiplexTest.temporary_plot
	def test_pad_pad_below_0(self):
		"""
		Test that when the padding is below 0, padding raises a ValueError.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertRaises(ValueError, bar._pad, 0, -1, 0)

	@MultiplexTest.temporary_plot
	def test_pad_pad_0(self):
		"""
		Test that when the padding is 0, padding does not raise a ValueError.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertEqual(0, bar._pad(10, 0, 0))

	@MultiplexTest.temporary_plot
	def test_pad_pad_100(self):
		"""
		Test that when the padding is 100, padding does not raise a ValueError.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertEqual(0, bar._pad(0, 100, 0))

	@MultiplexTest.temporary_plot
	def test_pad_pad_above_100(self):
		"""
		Test that when the padding is above 100, padding raises a ValueError.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertRaises(ValueError, bar._pad, 0, 101, 0)

	@MultiplexTest.temporary_plot
	def test_pad_min_percentage_below_0(self):
		"""
		Test that when the minimum percentage is below 0, padding raises a ValueError.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertRaises(ValueError, bar._pad, 0, 0, -1)

	@MultiplexTest.temporary_plot
	def test_pad_min_percentage_0(self):
		"""
		Test that when the minimum percentage is 0, padding does not raise a ValueError.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertEqual(0, bar._pad(10, 0, 0))

	@MultiplexTest.temporary_plot
	def test_pad_min_percentage_100(self):
		"""
		Test that when the minimum percentage is 100, padding does not raise a ValueError.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertEqual(0, bar._pad(100, 0, 100))

	@MultiplexTest.temporary_plot
	def test_pad_min_percentage_above_100(self):
		"""
		Test that when the minimum percentage is above 100, padding raises a ValueError.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertRaises(ValueError, bar._pad, 0, 0, 101)

	@MultiplexTest.temporary_plot
	def test_pad_min_percentage_exceeds_percentage(self):
		"""
		Test that when the minimum percentage exceeds the percentage, padding raises a ValueError.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertRaises(ValueError, bar._pad, 50, 0, 51)

	@MultiplexTest.temporary_plot
	def test_pad_min_percentage_equals_percentage(self):
		"""
		Test that when the minimum percentage is equal to the percentage, padding does not raise a ValueError.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertEqual(0, bar._pad(50, 0, 20))

	@MultiplexTest.temporary_plot
	def test_pad_no_padding(self):
		"""
		Test that when applying no padding, zero is returned.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertEqual(0, bar._pad(50, 0, 20))

	@MultiplexTest.temporary_plot
	def test_pad_no_space(self):
		"""
		Test that when the minimum percentage is equal to the percentage, the original percentage is returned.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertEqual(0, bar._pad(50, 10, 50))

	@MultiplexTest.temporary_plot
	def test_pad_one_side(self):
		"""
		Test that the returned padding is half of the amount of padding applied.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertEqual(5, bar._pad(50, 10, 20))

	@MultiplexTest.temporary_plot
	def test_pad_all_space(self):
		"""
		Test that padding and the left-over percentage fill in all the space.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertEqual(50, bar._pad(50, 10, 20) * 2 + 40)

	@MultiplexTest.temporary_plot
	def test_too_much_pad(self):
		"""
		Test that when too much padding is given, not all of it is used.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		bar = Bar100(viz)
		self.assertEqual(15, bar._pad(50, 50, 20))
