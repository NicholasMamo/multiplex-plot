"""
The :class:`timeseries.timeseries.TimeSeries` class borrows heavily on matplotlib's `plot` function.
This class builds on matplotlib's plotting and introduces more functionality.

For example, Multiplex time series do not have a legend by default.
Instead, to aid readability, the line's label is added to the end of the plot.

To start creating time series visualizations, create a :class:`timeseries.timeseries.TimeSeries` instance and call the :meth:`timeseries.timeseries.TimeSeries.draw` method.
If you are using the :class:`drawable.Drawable` class, just call the :meth:`drawable.Drawable.draw_time_series` method on a :class:`drawable.Drawable` instance instead.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
import util

class TimeSeries(object):
	"""
	The :class:`timeseries.timeseries.TimeSeries` class borrows heavily on matplotlib's `plot` function.
	This class builds on matplotlib's plotting and introduces more functionality.

	:ivar drawable: The :class:`drawable.Drawable` where the time series visualization will be drawn.
	:vartype drawable: :class:`drawable.Drawable`
	:ivar _labels: The labels in the time series.
				   This list is used to ensure that labels do not overlap.
	:vartype _labels: list of :class:`matplotlib.text.Text`
	"""

	def __init__(self, drawable):
		"""
		Initialize the text annotation with the figure and axis.
		The figure is used to get the renderer.
		The visualization is drawn on the given axis.

		:param drawable: The :class:`drawable.Drawable` where the time series visualization will be drawn.
		:type drawable: :class:`drawable.Drawable`
		"""

		self.drawable = drawable

		self._labels = []

	def draw(self, x, y, label=None, label_style=None, *args, **kwargs):
		"""
		Draw a time series on the :class:`drawable.Drawable`.
		The arguments and keyword arguments are passed on to the :meth:`matplotlib.pyplot.plot` method.
		Thus, all of the arguments and keyword arguments accepted by it are also accepted by this function.

		:param x: The list of x-coordinates to plot.
				  The x-coordinates must have the same number of points as the y-coordinates.
		:type x: list of float
		:param y: The list of corresponding y-coordinates to plot.
				  The y-coordinates must have the same number of points as the x-coordinates.
		:type y: list of float
		:param label: The plot's label.
					  If given, the label is drawn at the end of the line.
		:type label: str or None
		:param label_style: The style of the label.
		:type label_style: dict or None
		"""

		axis = self.drawable.axis
		plot = axis.plot(x, y, *args, **kwargs)

		# TODO: Add support for pandas Series

		label_style = {} if label_style is None else label_style

		if label is not None and len(x) and len(y):
			default_label_style = { 'color': plot[0].get_color() }
			default_label_style.update(label_style)
			label = self._draw_label(label, x[-1], y[-1], default_label_style)

			self._labels.append(label)
			self._arrange_labels()

	def _draw_label(self, label, x, y, *args, **kwargs):
		"""
		Draw a label at the end of the line.

		:param label: The label to draw.
		:type label: str
		:param x: The x-position of the last point on the line.
		:type x: float
		:param y: The y-position of the last point on the line.
		:type y: float

		:return: The drawn label's text box.
		:rtype: :class:`matplotlib.text.Text`
		"""

		axis = self.drawable.axis
		text = axis.text(x * 1.01, y, label, va='center', *args, **kwargs)
		return text

	def _arrange_labels(self):
		"""
		Go through the labels and ensure that none overlap.
		If any do overlap, move the labels.
		"""

		overlapping = self._get_overlapping_labels()
		if overlapping:
			pass

	def _get_overlapping_labels(self):
		"""
		Get groups of overlapping labels.
		The function returns a list of lists.
		Each inner list contains the labels that overlap.
		The function automatically excludes labels that do not overlap with other labels.

		:return: A list of lists.
				 Each inner list represents overlapping labels.
		:rtype: list of lists of :class:`matplotlib.text.Text`
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis

		labels = sorted(self._labels, key=lambda x: util.get_bb(figure, axis, x).y0)

		overlapping_labels = []
		for label in labels:
			assigned = False

			"""
			Go through each label and visit each group of overlapping labels.
			If the label overlaps with any label in that group, add it to that group.
			That group would have to be distributed entirely.
			"""
			for group in overlapping_labels:
				if (any([ util.overlapping(figure, axis, label, other) for other in group ])):
					group.append(label)
					assigned = True
					break

			"""
			If the label does not overlap with any other label, add it to its own group.
			Groups with a single label overlap with no other group and require no distribution.
			"""
			if not assigned:
				overlapping_labels.append([ label])

		return [ group for group in overlapping_labels if len(group) > 1 ]

	def _get_middle(self, labels):
		"""
		Get the middle y-coordinate of the given labels.
		The middle is calculated as the mid-point between the label that is highest and lowest.

		:param labels: The list of labels.
		:type labels: list of :class:`matplotlib.text.Text`

		:return: The middle y-coordinate of the labels.
		:rtype: float
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis

		labels = sorted(labels, key=lambda x: util.get_bb(figure, axis, x).y0)
		bb0, bb1 = util.get_bb(figure, axis, labels[0]), util.get_bb(figure, axis, labels[-1])

		return (bb0.y0 + bb1.y1) / 2.
