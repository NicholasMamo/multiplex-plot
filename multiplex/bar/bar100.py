"""
The :class:`~bar.100.Bar100` visualization draws stacked bar charts that all add up to 100%.
The 100% bar chart visualization is useful to show the make-up of data.

This visualization is based on `matplotlib's barh <https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.barh.html>`_ function.
However, it also comes with functionality to make it easier to construct 100% bar chart visualizations.
For example, you don't have to provide percentages; the :class:`~bar.100.Bar100` visualization automatically converts numbers to percentages.

For readability, the 100% bar chart visualization also makes a few changes to the plot by:

- Moving the x-ticks to the top of the plot,
- Moving the x-axis label to the top of the plot, and
- Removing the grid.
"""

import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
import util

from visualization import Visualization

class Bar100(Visualization):
	"""
	The 100% bar chart visualization draws bars that, unsurprisingly, always sums up to 100%.
	This class revolves around the :func:`~bar.100.Bar100.draw` function.
	The :func:`~bar.100.Bar100.draw` function receives a list of numbers and automatically converts them to percentages.

	This class keeps track of all the bars that it has drawn in the :ivar:`~bar.100.Bar100.bars` instance variable.

	:ivar bars: A list of bars drawn so far.
				Each bar is, in turn, made up of more bars, all of which add up to 100%.
	:vartype bars: list of list of :class:`matplotlib.patches.Rectangle`
	"""

	def __init__(self, *args, **kwargs):
		"""
		Instantiate the 100% bar chart visualization with an empty list of drawn bars.
		"""

		super().__init__(*args, **kwargs)

		self.bars = [ ]

	def draw(self, values, style_plot=True, *args, **kwargs):
		"""
		Draw a bar on the :class:`~drawable.Drawable`.
		All values are converted to percentages.

		The arguments and keyword arguments are passed on to the :func:`~matplotlib.pyplot.barh` method.
		Thus, all of the arguments and keyword arguments accepted by it are also accepted by this function.

		:param values: A list of values to draw.
		:type values: list of float
		:param style_plot: A boolean indicating whether the plot should be re-styled.
						   If it is set to `True`, the visualization:

						   - Moves the x-ticks to the top of the plot,
						   - Moves the x-axis label to the top of the plot, and
						   - Removes the grid.
		:type style_plot: bool

		:return: A list of drawn bars.
		:rtype: list of :class:`matplotlib.patches.Rectangle`
		"""

		"""
		Validate the arguments.
		The width of the bar cannot be 0.
		Therefore the function rejects an empty list of values or a list of zeroes.
		Furthermore, the width of any of the stacked bars cannot be negative.
		Therefore the function rejects negative values.
		"""
		if not values or not any([ value for value in values ]):
			raise ValueError("At least one non-zero value has to be provided")

		if any([ value < 0 for value in values ]):
			raise ValueError(f"All values must be non-negative; received { ', '.join([ str(value) for value in values if value < 0 ]) }")

		"""
		Re-style the plot if need be.
		"""
		if style_plot:
			self._style()

		"""
		Draw the bars.
		"""
		bars = self._draw_bars(values, *args, **kwargs)
		self.bars.append(bars)

		return bars

	def _style(self):
		"""
		Style the plot by:

		- Moving the x-ticks to the top of the plot,
		- Moving the x-axis label to the top of the plot, and
		- Removing the grid.
		"""

		axis = self.drawable.axis
		axis.xaxis.set_label_position('top')
		axis.xaxis.tick_top()
		axis.spines['top'].set_visible(True)
		axis.spines['bottom'].set_visible(False)
		self.drawable.grid(False)

	def _draw_bars(self, values, *args, **kwargs):
		"""
		Draw the bars such that they stack up to 100%.

		:param values: A list of values to draw.
		:type values: list of float

		:return: A list of drawn bars.
		:rtype: list of :class:`matplotlib.patches.Rectangle`
		"""

		bars = [ ]

		figure = self.drawable.figure
		axis = self.drawable.axis

		"""
		Convert the values to percentages and draw them.
		"""
		percentages = self._to_100(values)

		"""
		Draw each bar, one after the other.
		"""
		offset = 0
		for percentage in percentages:
			bar = self.drawable.barh(len(self.bars), percentage, left=offset,
									 *args, **kwargs)
			bars.append(bar.patches[0])
			offset += percentage

		return bars

	def _to_100(self, values):
		"""
		Convert the given list of values to percentages.

		:param values: A list of values to convert to percentages.
		:type values: list of float

		:return: A list of percentages that add up to 100%.
		:rtype: list of float
		"""

		if not values or not any([ value for value in values ]):
			return values

		return [ 100 * value / sum(values) for value in values ]
