"""
The :class:`~Bar100` visualization draws stacked bar charts that all add up to 100%.
These types of visualizations are useful to show the make-up of data in terms of percentages.

.. image:: ../examples/exports/5-natural-gas.png
   :class: example inline

The :class:`~Bar100` visualization is based on `matplotlib's barh <https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.barh.html>`_ function.
This class, like the rest of Multiplex's new visualizations, simplifies the construction of 100% bar chart.
For example, you don't have to provide percentages; the :class:`~Bar100` visualization automatically converts numbers to percentages.

For readability, the 100% bar chart visualization also makes a few changes to the plot by:

	- Moving the x-axis label to the top of the plot,
	- Moving the x-ticks to the top of the plot,
	- Converting the x-ticks to percentages, and
	- Removing the grid.

It is very easy to create 100% bar charts.
All you have to do is create a :class:`~drawable.Drawable` class and call the :func:`~drawable.Drawable.draw_bar_100` function.
This method expects, at the very least, the values and the name of the 100% bar:

.. code-block:: python

    import matplotlib.pyplot as plt
    from multiplex import drawable
    viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
    viz.draw_bar_100([ 5, 2, 4, 7, 3 ], 'bar', alpha=0.5, color='C1')
    viz.show()

As usual, you can create more complex visualizations by styling each bar individually and adding legends.

.. note::

	You can view more complex 100% bar chart visualization examples in the `bar chart Jupyter Notebook tutorial <https://github.com/NicholasMamo/multiplex-plot/blob/master/examples/5.%20Bar%20charts.ipynb>`_.
"""

import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
import util

from visualization import Visualization

class Bar100(Visualization):
	"""
	The 100% bar chart visualization draws bars that, unsurprisingly, always sums up to 100%.
	Although the 100% bar chart is based on `matplotlib's barh <https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.barh.html>`_ function, the :class:`~Bar100` visualization does a lot of work behind the scenes to make it easier to create 100% bar charts.

	This class stores the :class:`~drawable.Drawable` instance.
	As usual, the main functionality goes through the :func:`~Bar100.draw` function.

	The :func:`~Bar100.draw` function receives a list of numbers, converts them to percentages and then draws them.
	This class keeps track of all the bars that it has drawn in the ``bars`` instance variable.

	:ivar bars: A list of bars drawn so far.
				Each bar is split into a number of bars that together add up to 100%.
	:vartype bars: list of list of :class:`matplotlib.patches.Rectangle`
	"""

	def __init__(self, *args, **kwargs):
		"""
		Instantiate the 100% bar chart visualization with an empty list of drawn bars.
		"""

		super().__init__(*args, **kwargs)

		self.bars = [ ]

	def draw(self, values, name, style_plot=True,
			 min_percentage=1, pad=0.25, label_style=None, *args, **kwargs):
		"""
		Draws a bar on the :class:`~drawable.Drawable` that spans 100% of the x-axis.
		The function automatically converts the given values into percentages.


		The values can be provided either as a list of floats or as a list of dictionaries.
		If floats are provided, the function automatically converts them into dictionaries.
		Dictionaries should have the following format:

		.. code-block:: python

			{
			  'value': 10,
			  'style': { 'color': 'C1' },
			  'label': None
			}

		Of these keys, only the ``value`` is required.

		If you provide a ``label``, the function automatically adds a legend for the bar.

		You can use the ``style`` to override the general styling options, which you can specify as ``kwargs``.
		The accepted styling options are those supported by the `matplotlib.pyplot.barh <https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.barh.html>`_ method.

		Use the ``kwargs`` as a general style, and the dictionary's ``style`` as a specific style for each bar.
		If you specify a ``kwargs`` styling option, but it is missing from the dictionary's ``style``, the general style is used.

		.. note::

			For example, imagine you specify the bar ``color`` to be ``blue`` and the ``alpha`` to be ``0.2`` in the ``**kwargs``.
			If in the dictionary's ``style`` of a particular bar you set the ``alpha`` to be ``1``, the bar will be opaque.
			However, since the ``color`` is not specified, it will use the general color: ``blue``.

		:param values: A list of values to draw.
					   The visualization expects a ``list`` of floats or a ``list`` of ``dict`` instances as shown above.
		:type values: list of float or list of dict
		:param name: The name of the 100% bar chart.
					 The function automatically adds this name to the y-axis tick labels next to the drawn bar.
		:type name: str
		:param style_plot: A boolean indicating whether the plot should be re-styled.
						   If it is set to ``True``, the visualization:

						       - Moves the x-axis label to the top of the plot,
					   	       - Moves the x-ticks to the top of the plot,
					   	       - Converts the x-ticks to percentages, and
					   	       - Removes the grid.
		:type style_plot: bool
		:param min_percentage: The minimum percentage to show in the 100% bar chart.
							   This is used so that bars with 0% percentage are still shown with a very thin bar.
		:type min_percentage: float
		:param pad: The amount of padding, in percentage, to apply to the given value.
					This padding will be split equally on the left and right of the bar.
					In any case, the padding cannot reduce a bar to below the minimum percentage.
		:type pad: float
		:param label_style: The style of the label.
							By default, the label inherits the style from the ``kwargs`` so that the label is visually similar to the bar.
							The ``label_style`` accepts any styling option supported by the :class:`~text.annotation.Annotation`'s :func:`~text.annotation.Annotation.draw` function.
		:type label_style: dict or None

		:return: The list of drawn bars.
				 These bars are ordered in the same way as the provided values.
				 Together, they add up to 100%.
		:rtype: list of :class:`matplotlib.patches.Rectangle`

		:raises ValueError: When no values are given.
		:raises ValueError: When all values are zero.
		:raises ValueError: When any value is negative.
		:raises ValueError: When the minimum percentage is below 0% or above 100%.
		:raises ValueError: When the minimum percentage multiplied by all values exceeds 100%.
		:raises ValueError: When the name is empty.
		"""

		values = self._to_dict(values)

		"""
		Validate the arguments.
		The width of the bar cannot be 0.
		Therefore the function rejects an empty list of values or a list of zeroes.
		Furthermore, the width of any of the stacked bars cannot be negative.
		Therefore the function rejects negative values.
		"""
		if not values or not any([ value['value'] for value in values ]):
			raise ValueError("At least one non-zero value has to be provided")

		if any([ value['value'] < 0 for value in values ]):
			raise ValueError(f"All values must be non-negative; received { ', '.join([ str(value['value']) for value in values if value['value'] < 0 ]) }")

		"""
		Validate the inputs.
		"""
		if not 0 <= min_percentage <= 100:
			raise ValueError(f"The minimum percentage must be between 0% and 100%; received { min_percentage }")

		if min_percentage * len(values) > 100:
			raise ValueError(f"The minimum percentage exceeds 100%; { min_percentage } × { len(values) } = { min_percentage * len(values) }")

		if not name:
			raise ValueError("The name cannot be empty")

		"""
		Re-style the plot if need be.
		"""
		if style_plot:
			self._style()

		"""
		Draw the bars.
		"""
		bars = self._draw_bars(values, min_percentage=min_percentage, pad=pad,
							   *args, **kwargs)
		self.bars.append(bars)
		self._add_name(name)

		"""
		Draw the legend.
		"""
		self._draw_legend(values, label_style=label_style, *args, **kwargs)

		return bars

	def _style(self):
		"""
		Style the plot by:

		- Moving the x-ticks to the top of the plot,
		- Moving the x-axis label to the top of the plot, and
		- Removing the grid.
		"""

		axes = self.drawable.axes
		axes.xaxis.set_label_position('top')
		axes.xaxis.tick_top()
		axes.spines['top'].set_visible(True)
		axes.spines['bottom'].set_visible(False)
		self.drawable.set_xlim((0, 100))
		self.drawable.set_xticks(range(0, 101, 20))
		self.drawable.set_xticklabels([ f"{ percent }%" for percent in range(0, 101, 20)])
		self.drawable.grid(False)

	def _to_dict(self, values):
		"""
		Convert all values to a list of dictionaries.
		This is done so that all values are uniform.

		:param values: A list of values.
		:type values: list of float or list of dict

		:return: A list of values as dictionaries.
		:rtype: list of dict
		"""

		dicts = [ ]

		for value in values:
			value_dict = dict(value) if type(value) is dict else { 'value': value }
			value_dict['value'] = value_dict.get('value', 0)
			value_dict['style'] = value_dict.get('style', { })
			dicts.append(value_dict)

		return dicts

	def _draw_bars(self, values, min_percentage=0, pad=0, *args, **kwargs):
		"""
		Draw the bars such that they stack up to 100%.

		:param values: A list of values to draw.
		:type values: list of dict
		:param min_percentage: The minimum percentage to show in the 100% bar chart.
							   This is used so that bars with 0% percentage are still shown with a thin bar.
		:type min_percentage: float
		:param pad: The amount of padding, in percentage, to apply to the given value.
					This padding will be split equally on the left and right of the bar.
					In any case, the padding cannot reduce a bar to below the minimum percentage.
		:type pad: float

		:return: A list of drawn bars.
		:rtype: list of :class:`matplotlib.patches.Rectangle`
		"""

		bars = [ ]

		figure = self.drawable.figure
		axes = self.drawable.axes

		"""
		Convert the values to percentages and draw them.
		"""
		percentages = self._to_100([ value['value'] for value in values ],
								   min_percentage=min_percentage)

		"""
		Draw each bar, one after the other.
		"""
		offset = 0
		for i, percentage in enumerate(percentages):
			style = values[i].get('style', { })

			padding = self._pad(percentage, style.pop('pad', pad), min_percentage)

			"""
			Apply the left offset based on padding.
			This is not applied for the first bar.
			"""
			offset += padding if i else 0

			"""
			Calculate the width based on padding.
			All bars except the first and last ones have their width reduced by the padding on both sides.
			The first and last bars have their width reduced by padding on one side only.
			"""
			width = percentage - padding * (2 if 0 < i < len(percentages) - 1 else 1)

			"""
			Draw the bar.
			"""
			default_style = dict(kwargs)
			default_style.update(style)
			bar = self.drawable.barh(len(self.bars), width, left=offset,
									 *args, **default_style)
			bars.append(bar.patches[0])

			"""
			Apply the right offset based on padding.
			"""
			offset += width + padding

		return bars

	def _to_100(self, values, min_percentage=0):
		"""
		Convert the given list of values to percentages.

		:param values: A list of values to convert to percentages.
		:type values: list of float
		:param min_percentage: The minimum percentage, defaults to 0%.
							   This is used so that bars with 0% percentage are still shown with a thin bar.
		:type min_percentage: float

		:return: A list of percentages that add up to 100%.
		:rtype: list of float

		:raises ValueError: When the minimum percentage is below 0% or above 100%.
		:raises ValueError: When the minimum percentage multiplied by all values exceeds 100%.
		"""

		percentages = [ ]

		"""
		Validate the inputs.
		"""
		if not 0 <= min_percentage <= 100:
			raise ValueError(f"The minimum percentage must be between 0% and 100%; received { min_percentage }%")

		if min_percentage * len(values) > 100:
			raise ValueError(f"The minimum percentage exceeds 100%; { min_percentage }% × { len(values) } = { min_percentage * len(values) }%")

		"""
		Return immediately if there are no input values or all values are zero.
		"""
		if not values or not any([ value for value in values ]):
			return values

		"""
		Calculate the percentages and boost any that are below the minimum percentage.
		Then, rescale them back to 100%.
		This process is repeated recursively until all percentages meet the minimum percentage.
		"""
		percentages = [ 100 * value / sum(values) for value in values ]
		if min_percentage and any(round(percentage, 10) < round(min_percentage, 10) for percentage in percentages):
			percentages = [ max(min_percentage, percentage) for percentage in percentages ]
			percentages = self._to_100(percentages, min_percentage=min_percentage)

		return percentages

	def _pad(self, percentage, pad, min_percentage):
		"""
		Get the padding to apply to the given percentage value.
		Padding leaves some space around both ends of the bar.

		:param percentage: The percentage to which padding will be applied.
		:type percentage: float
		:param pad: The amount of padding, in percentage, to apply to the given value.
					This padding will be split equally on the left and right of the bar.
					In any case, the padding cannot reduce a bar to below the minimum percentage.
		:type pad: float
		:param min_percentage: The minimum percentage to allow.
							   This is used so that even very small percentages are shown in the 100% bar chart.
		:type min_percentage: float

		:return: The amount of padding to apply to the given percentage value.
				 The padding returned is for one side.
		:rtype: float

		:raises ValueError: When the percentage is below 0% or above 100%.
		:raises ValueError: When the padding is below 0% or above 100%.
		:raises ValueError: When the minimum percentage is below 0% or above 100%.
		:raises ValueError: When the minimum percentage exceeds the percentage.
		"""

		"""
		Validate the inputs.
		"""
		if not 0 <= percentage <= 100:
			raise ValueError(f"The percentage must be between 0% and 100%; received { percentage }%")

		if not 0 <= round(pad, 10) <= 100:
			raise ValueError(f"The padding must be between 0% and 100%; received { pad }%")

		if not 0 <= min_percentage <= 100:
			raise ValueError(f"The minimum percentage must be between 0% and 100%; received { min_percentage }")

		if round(min_percentage, 10) > round(percentage, 10):
			raise ValueError(f"The minimum percentage cannot exceed the percentage; { min_percentage } > { percentage }")

		"""
		Calculate the left-over percentage after applying padding.
		The left-over percentage cannot be lower than the minimum percentage.
		"""
		leftover = max(percentage - pad, min_percentage)

		"""
		The padding is any space aside from the left-over percentage.
		"""
		return (percentage - leftover) / 2.

	def _add_name(self, name):
		"""
		Add a name to the y-axis.

		This function does two things:

			- Adds a y-tick, and
			- Gives that y-tick the given name.

		:param name: The name of the drawn bar.
		:type name: str
		"""

		"""
		Add a y-tick based on the number of bars.
		"""
		self.drawable.set_yticks(range(len(self.bars)))

		"""
		Get the current labels and filter them.
		"""
		names = [ name.get_text() for name in self.drawable.get_yticklabels() ]
		names = [ name for name in names if name ]
		names.append(name)

		"""
		Add the new label to the y-axis labels.
		"""
		self.drawable.set_yticklabels(names)

	def _draw_legend(self, values, label_style=None, *args, **kwargs):
		"""
		Draw the value labels in the legend.

		Any additional arguments and keyword arguments are passed on to the legend drawing functions.

		:param values: A list of values to draw.
		:type values: list of dict
		:param label_style: The style of the labels.
		:type label_style: dict or None
		"""

		label_style = label_style or { }

		for value in values:
			if 'label' not in value:
				continue

			label = value['label']

			"""
			If the label is empty or `None`, there is nothing to draw, so skip it.
			"""
			if not label:
				continue

			style = value.get('style', { })
			default_style = dict(**kwargs)
			default_style.update(style)
			default_style.update(label_style)
			default_style.update(value.get('label_style', { }))
			default_style.pop('pad', None)

			self.drawable.legend.draw_text_only(label, label_style=default_style)
