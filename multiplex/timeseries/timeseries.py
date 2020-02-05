"""
The :class:`timeseries.timeseries.TimeSeries` class borrows heavily from matplotlib's `plot` function.
This class builds on matplotlib's plotting and introduces more functionality.

.. image:: ../../examples/exports/3-time-series.png
   :class: example

For example, Multiplex time series do not have a legend by default.
Instead, to aid readability, the line's label is added to the end of the plot.
Multiplex also supports annotations, making it easier to tell a story through time series.

To start creating time series visualizations, create a :class:`timeseries.timeseries.TimeSeries` instance and call the :meth:`timeseries.timeseries.TimeSeries.draw` method.
If you are using the :class:`drawable.Drawable` class, just call the :meth:`drawable.Drawable.draw_time_series` method on a :class:`drawable.Drawable` instance instead.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
import util

from text.annotation import Annotation

class TimeSeries(object):
	"""
	The :class:`timeseries.timeseries.TimeSeries` class borrows heavily on matplotlib's `plot` function.
	This class builds on matplotlib's plotting and introduces more functionality.

	For example, Multiplex's time series have no legend.
	Instead, it adds a label at the end of the time series for readability.
	Multiplex also makes it easy to annotate points on the time series with descriptions to explain their significance.

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

	def draw(self, x, y, label=None, label_style=None, annotations=None,
			 marker_style=None, annotation_style=None, *args, **kwargs):
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
		:param annotations: A list of annotations.
							If a list of annotations is given, it must be equal to the number of points.
							The annotations can either be simple strings, or dictionaries.
							With dictionaries, you can style each annotation separately.
							If no dictionary is given, then a default style is used.
							Dictionaries must have the following format:

							.. code-block:: python

								{
								  'marker_style': { },
								  'annotation_style': { },
								  'text': 'annotation',
								}
		:type annotations: list of dict or list of str
		:param marker_style: A dictionary containing the style that should be applied in general to all annotation markers.
							 This dictionary is over-written by any annotation-specific style.
		:type marker_style: dict or None
		:param annotation_style: A dictionary containing the style that should be applied in general to the annotation text.
								 This dictionary is over-written by any annotation-specific style.
								 A special key, `wordspacing`, can be set to determine the spacing between words in the annotation.
		:type annotation_style: dict or None

		:raises: ValueError
		"""

		if len(x) != len(y):
			raise ValueError("The number of x-coordinates and y-coordinates must be equal; received %d x-coordinates and %d y-coordinates" % (len(x), len(y)))

		axis = self.drawable.axis
		plot = axis.plot(x, y, *args, **kwargs)

		# TODO: Add support for pandas Series

		"""
		Draw the label at the end of the line.
		"""
		if label is not None and len(x) and len(y):
			default_label_style = { 'color': plot[0].get_color() }
			label_style = {} if label_style is None else label_style
			default_label_style.update(label_style)
			label = self._draw_label(label, x[-1], y[-1], default_label_style)

			self._labels.append(label)
			self._arrange_labels()

		"""
		Draw the annotations.
		"""
		if annotations:
			if len(annotations) != len(x):
				raise ValueError("The number of annotations must be equal to the number of points; received %d annotations and %d points" % (len(annotations), len(x)))
			if len(annotations) != len(y):
				raise ValueError("The number of annotations must be equal to the number of points; received %d annotations and %d points" % (len(annotations), len(y)))

			"""
			By default, the annotations' markers have the same color as the plot.
			However, this may be over-written by the marker style.
			"""
			default_marker_style = {
				'color': plot[0].get_color(),
				'marker': 'o', 'markersize': 8
			}
			marker_style = {} if marker_style is None else marker_style
			default_marker_style.update(marker_style)

			"""
			By default, the annotations have the same color as the plot.
			However, this may be over-written by the annotation style.
			The default wordpsacing is based on the plot width.
			"""
			x_lim = axis.get_xlim()
			x_lim_width = x_lim[1] - x_lim[0]
			default_annotation_style = { 'color': plot[0].get_color(), 'wordspacing': x_lim_width/250. }
			annotation_style = {} if annotation_style is None else annotation_style
			default_annotation_style.update(annotation_style)

			"""
			Draw the annotations separately.
			Annotations that are empty (or `None`) are skipped.
			"""
			for (x, y, annotation) in zip(x, y, annotations):
				if annotation:
					self._draw_annotation(x, y, annotation, default_marker_style, default_annotation_style)

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
		The function keeps repeating until no labels overlap.

		.. image:: ../../examples/exports/3-overlapping-labels.png
		   :class: example
		"""

		overlapping = self._get_overlapping_labels()
		while overlapping:
			for group in overlapping:
				self._distribute_labels(group)
			overlapping = self._get_overlapping_labels()

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

	def _distribute_labels(self, labels):
		"""
		Distribute the given labels so that they do not overlap.

		:param labels: The list of overlapping labels.
		:type labels: list of :class:`matplotlib.text.Text`
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis

		"""
		Calculate the total height that the labels should occupy.
		Then, get the mean y-coordinate of the labels to find the middle.
		"""
		total_height = self._get_total_height(labels)
		middle = self._get_middle(labels)

		"""
		Sort the labels in ascending order of position (y-coordinate).
		Then, move the labels one by one.
		The initial offset is calculated as the distance that the first label needs to move.
		Subsequently, the offset is calculated by adding the height of each label.
		"""
		labels = sorted(labels, key=lambda x: util.get_bb(figure, axis, x).y0)
		y0 = middle - total_height / 2.
		for label in labels:
			position = label.get_position()
			bb = util.get_bb(figure, axis, label)
			label.set_position((position[0], y0 + bb.height / 2.))
			y0 += bb.height

	def _get_total_height(self, labels):
		"""
		Get the total height of the given labels.

		:param labels: The list of labels.
		:type labels: list of :class:`matplotlib.text.Text`

		:return: The total height of the labels.
		:rtype: float
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis

		return sum([ util.get_bb(figure, axis, label).height for label in labels ])

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

	def _draw_annotation(self, x, y, annotation, marker_style, annotation_style, *args, **kwargs):
		"""
		Draw the annotation at the given coordinates.

		:param annotation: The annotation to draw.
						   The function accepts either a string or a dictionary.
						   If a dictionary is provided, it must have the following format:

						   .. code-block:: python

							   {
								 'marker_style': { },
								 'annotation_style': { },
								 'text': 'annotation',
							   }
		:type annotation: str or dict
		:param x: The x-coordinate of the annotation.
		:type x: float
		:param y: The y-coordinate of the annotation.
		:type y: float
		:param marker_style: A dictionary containing the style that should be applied to the annotation marker.
		:type marker_style: dict
		:param annotation_style: A dictionary containing the style that should be applied to the annotations.
								 A special key, `wordspacing`, can be set to determine the spacing between words in the annotation.
		:type annotation_style: dict
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis

		marker_style.update(annotation.get('marker_style', {}))
		axis.plot(x, y, *args, **marker_style)

		"""
		Calculate the best horizontal and vertical alignments.
		"""
		annotation_style.update(annotation.get('annotation_style', {}))
		ha, va = annotation_style.pop('ha', self._get_best_ha(x)), annotation_style.pop('va', self._get_best_va(y))
		annotation_style['va'] = va

		"""
		Add some padding to the annotations based on the horizontal alignment.
		"""
		x_lim = axis.get_xlim()
		x_lim_width = x_lim[1] - x_lim[0]
		x_pad = x_lim_width * 0.01
		if ha == 'left':
			x = (x + x_pad, x + x_lim_width * 0.15)
		elif ha == 'right':
			x = (x - x_lim_width * 0.15, x - x_pad)
		elif ha == 'center':
			x = (x - x_lim_width * 0.15 / 2., x + x_lim_width * 0.15 / 2.)
		else:
			# TODO: raise exception
			pass

		y_lim = axis.get_ylim()
		y_lim_width = y_lim[1] - y_lim[0]
		y_pad = y_lim_width * 0.01
		if va == 'top':
			y -= y_pad
		elif va == 'bottom':
			y += y_pad
		else:
			# TODO: complete
			y += y_pad

		annotation_text = annotation if type(annotation) is str else annotation.get('text')
		annotation_ = Annotation(self.drawable)
		wordspacing = annotation_style.pop('wordspacing')
		tokens = annotation_.draw(annotation_text, x, y, wordspacing, *args, **annotation_style)
		return tokens

	def _get_best_ha(self, x):
		"""
		Get the best horizontal alignment for the annotation.
		The horizontal alignment is either `left` or `right`.

		:param x: The x-coordinate of the annotation.
		:type x: float
		"""

		axis = self.drawable.axis

		"""
		Get the x-limit.
		If the x-coordinate is within less than or equal to 10% of the x-axis start, plot the annotation on the right.
		Otherwise, plot it on the left.
		"""
		x_lim = axis.get_xlim()
		x_lim_width = x_lim[1] - x_lim[0]

		if (x - x_lim[0])/x_lim_width <= 0.1:
			return 'left' # the annotation is on the right
		else:
			return 'right' # the annotation is on the left

	def _get_best_va(self, y):
		"""
		Get the best vertcial alignment for the annotation.
		The vertcial alignment is either `top` or `bottom`.

		:param y: The y-coordinate of the annotation.
		:type y: float
		"""

		axis = self.drawable.axis

		"""
		Get the y-limit.
		If the y-coordinate is within less than or equal to 10% of the y-axis start, plot the annotation on the top.
		Otherwise, plot it on the bottom.
		"""
		y_lim = axis.get_ylim()
		y_lim_width = y_lim[1] - y_lim[0]

		if (y - y_lim[0])/y_lim_width >= 0.9:
			return 'top' # the annotation is at the bottom
		else:
			return 'bottom' # the annotation is at the top

	def _newline(self, lines, line_tokens, ha, va):
		"""
		Create a new line.

		:param lines: A list of lines, each containing tokens.
		:type lines: list of lists of :class:`matplotlib.text.Text`
		:param line_tokens: The tokens in the current line, which will be 'retired'.
		:type line_tokens: list of :class:`matplotlib.text.Text`
		:param ha: The horizontal alignment: 'left' or 'right'.
		:type ha: str
		:param va: The vertical alignment: 'top' or 'bottom'.
		:type va: str
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis

		if ha == 'right':
			if va == 'top':
				"""
				Go through the previous lines and make a new line out of them.
				"""
				for line in lines:
					for other in line:
						position = other.get_position()
						bb = util.get_bb(figure, axis, other)
						other.set_position((position[0], position[1] - bb.height))
			elif va == 'bottom':
				"""
				Make a new line out of the last line.
				"""
				for other in line_tokens:
					position = other.get_position()
					bb = util.get_bb(figure, axis, other)
					other.set_position((position[0], position[1] + len(lines) * bb.height))
		elif ha == 'left':
			if va == 'bottom':
				"""
				Go through the previous lines and make a new line out of them.
				"""
				for line in lines:
					for other in line:
						position = other.get_position()
						bb = util.get_bb(figure, axis, other)
						other.set_position((position[0], position[1] + bb.height))
			elif va == 'top':
				"""
				Make a new line out of the last line.
				"""
				for other in line_tokens:
					position = other.get_position()
					bb = util.get_bb(figure, axis, other)
					other.set_position((position[0], position[1] - len(lines) * bb.height))

	def _remove_empty_line(self, lines, va):
		"""
		Remove the last empty line from the annotation.

		:param lines: A list of lines, each containing tokens.
		:type lines: list of lists of :class:`matplotlib.text.Text`
		:param va: The vertical alignment: 'top' or 'bottom'.
		:type va: str
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis

		"""
		Go through each line and offset every token by its height.
		"""
		for line in lines:
			for token in line:
				position = token.get_position()
				bb = util.get_bb(figure, axis, token)
				token.set_position((position[0], position[1] - bb.height))
