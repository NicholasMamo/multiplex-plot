"""
All of Multiplex's visualizations revolve around the :class:`~Drawable` class.
A :class:`~Drawable` is nothing more than a class that wraps a matplotlib figure and an axis.
All of the functions that you would call on a matplotlib axis, you can call on the :class:`~Drawable`.
The :class:`~Drawable` instance re-routes unknown functions to the matplotlib axis.
However, the :class:`~Drawable` also comes with new visualizations to help you explore or explain data faster.
"""

import matplotlib.pyplot as plt
import os
import re
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from bar.bar100 import Bar100
from graph.graph import Graph
from legend import Legend
from text.annotation import Annotation
from text.text import TextAnnotation
from timeseries.timeseries import TimeSeries
import util

class Drawable():
	"""
	The :class:`~Drawable` class wraps a matplotlib figure and axis to provide additional functionality.
	If no axis is given, the default plot axis (:code:`plt.gca()`) is used.
	The :class:`~Drawable` class can be used as a normal :class:`matplotlib.axis.Axis` object with additional functionality.
	The axis functionality can be called on the :class:`~Drawable` class.
	The :class:`~Drawable` instance re-routes method and attribute calls to the :class:`matplotlib.axis.Axis` instance.

	To create a :class:`~Drawable` instance from a normal plot:

	.. code-block:: python

	  viz = drawable.Drawable(plt.figure(figsize=(10, 5)))

	To create a :class:`~Drawable` instance from an axis, or a subplot:

	.. code-block:: python

	  figure, axis = plt.subplots(2, 1, figsize=(10, 10))
	  viz = drawable.Drawable(figure, axis[0])

	:ivar figure: The figure that the :class:`~Drawable` class wraps.
	:vartype figure: :class:`matplotlib.figure.Figure`
	:ivar axis: The axis where the drawable will draw.
	:vartype axis: :class:`matplotlib.axis.Axis`
	:var caption: The caption, displayed under the title.
	:vartype caption: :class:`~text.annotation.Annotation`

	:ivar timeseries: The time series object that is being used.
					  When no visualization has been created, it is set to `None`.
					  It is instantiated the first time a time series is drawn.
	:vartype timeseries: None or :class:`~timeseries.timeseries.TimeSeries`
	:ivar bar100: The 100% bar chart visualization that is being used.
				  When no visualization has been created, it is set to `None`.
				  It is instantiated the first time a 100% bar chart is drawn.
	:vartype bar100: None or :class:`~bar.100.Bar100`

	:ivar legend: The figure's legend.
	:vartype legend: :class:`~legend.Legend`
	:ivar annotations: The annotations in the visualization.
	:vartype annotations: list of :class:`~text.annotation.Annotation`
	"""

	def __init__(self, figure, axis=None):
		"""
		Create the drawable with the figure.

		:param figure: The figure that the :class:`~Drawable` class wraps.
					   This is mainly used to get the figure renderer.
		:type figure: :class:`matplotlib.figure.Figure`
		:param axis: The axis (or subplot) where to plot visualizations.
					 If `None` is not given, the plot's main subplot is used instead.
		:type axis: `None` or :class:`matplotlib.axis.Axis`
		"""

		self.figure = figure
		self.axis = plt.gca() if axis is None else axis
		self.caption = Annotation(self)

		self.annotations = [ ]
		self.legend = Legend(self)
		self.timeseries = None
		self.bar100 = None

	def set_caption(self, caption, alpha=0.8, lineheight=1.25, *args, **kwargs):
		"""
		Add a caption to the subplot.
		The caption is added just beneath the title.
		The method re-draws the title to make space for the caption.

		The caption is a :class:`~text.text.Annotation` object.
		Any arguments that the constructor accepts can be provided to this method.

		:param caption: The caption to add to the axis.
		:type caption: str
		:param alpha: The opacity of the caption between 0 and 1.
		:type alpha: float
		:param lineheight: The space between lines.
		:type lineheight: float

		:return: The drawn caption.
		:rtype: :class:`~text.annotation.Annotation`
		"""

		self.caption = Annotation(self)
		self.caption.draw(caption, (0, 1), 1,
						  va='bottom', alpha=alpha, lineheight=lineheight,
						  transform=self.axis.transAxes,
						  *args, **kwargs)
		self.redraw()
		return self.caption

	def redraw(self):
		"""
		Re-create the title with the necessary padding to fit the caption and the legend.
		"""

		self._redraw_title()
		self._redraw_caption()
		self.legend.redraw()

	def _redraw_caption(self):
		"""
		Re-draw the caption, re-positioning so that it does not overlap with the legend or axis.
		"""

		figure, axis = self.figure, self.axis

		"""
		Move the caption up to make space for the legend and the label.
		"""
		y = 1
		y += self.legend.get_virtual_bb(transform=self.axis.transAxes).height

		"""
		If the x-label is on top, make space for it in the caption.
		In this case, it is assumed that the ticks are also at the top.
		This is because for some reason they may be set to 'unknown'.
		"""
		if axis.xaxis.get_label_position() == 'top':
			y += self._get_xlabel(transform=self.axis.transAxes).height * 2

			xtick_labels_bb = self._get_xtick_labels(transform=axis.transAxes)
			if xtick_labels_bb:
				y += max(xtick_labels_bb, key=lambda bb: bb.height).height * 2

		self.caption.set_position((0, y), ha='left', va='bottom', transform=self.axis.transAxes)

	def _redraw_title(self):
		"""
		Re-draw the title, adding enough padding so that there is enough space for the axis label, the legend and the caption.
		"""

		figure, axis = self.figure, self.axis

		title = axis.get_title(loc='left')

		"""
		Get the height of the caption and the height of the legend.
		The title should allow enough padding to make space for both.
		"""
		caption_height = 0
		if str(self.caption):
			caption_height = util.to_px(axis, self.caption.get_virtual_bb(transform=axis.transAxes),
										transform=axis.transAxes).height

		legend_height = util.to_px(axis, self.legend.get_virtual_bb(transform=axis.transAxes),
								   transform=axis.transAxes).height

		"""
		If the x-label is on top, make space for it in the title.
		In this case, it is assumed that the ticks are also at the top.
		This is because for some reason they may be set to 'unknown'.
		"""
		label_height = 0
		if axis.xaxis.get_label_position() == 'top':
			label_bb = self._get_xlabel(transform=axis.transData)
			label_height = util.to_px(axis, label_bb,
									  transform=axis.transData).height * 2
			xtick_labels_bb = self._get_xtick_labels(transform=axis.transData)
			if xtick_labels_bb:
				label_bb = max(xtick_labels_bb, key=lambda bb: bb.height)
				label_height += util.to_px(axis, label_bb, transform=axis.transData).height * 2

		"""
		Add some extra padding to the height.
		"""
		height = abs(caption_height) + abs(legend_height) + abs(label_height)
		pad_px = abs(self.axis.transAxes.transform((0, 0.01))[1] - self.axis.transAxes.transform((0, 0))[1])
		self.axis.set_title(title, loc='left', pad=(5 + height + pad_px * 2))

	def _get_xlabel(self, transform=None):
		"""
		Get the bounding box of the x-axis label.

		:param transform: The bounding box transformation.
						  If `None` is given, the data transformation is used.
		:type transform: None or :class:`matplotlib.transforms.TransformNode`

		:return: The bounding box of the x-axis label.
		:rtype: :class:`matplotlib.transforms.Bbox`
		"""

		figure, axis = self.figure, self.axis

		transform = transform or axis.transData
		return util.get_bb(figure, axis, axis.xaxis.get_label(), transform=transform)

	def _get_xtick_labels(self, transform=None):
		"""
		Get the bounding box of the x-axis tick labels.

		:param transform: The bounding box transformation.
						  If `None` is given, the data transformation is used.
		:type transform: None or :class:`matplotlib.transforms.TransformNode`

		:return: The bounding box of the x-axis label.
		:rtype: :class:`matplotlib.transforms.Bbox`
		"""

		figure, axis = self.figure, self.axis

		figure.canvas.draw()
		transform = transform or axis.transData
		return [ util.get_bb(figure, axis, label, transform=transform)
				 for label in axis.xaxis.get_ticklabels(which='both') ]

	def savefig(self, *args, **kwargs):
		"""
		A special function that calls the :func:`matplotlib.pyplot.savefig` function.
		Before doing that, the function redraws the drawable.
		This can be used when the title and caption are set before drawing the data.
		"""

		self.redraw()
		plt.savefig(*args, **kwargs)

	def show(self, *args, **kwargs):
		"""
		A special function that calls the :func:`matplotlib.pyplot.savefig` function.
		Before doing that, the function redraws the drawable.
		This can be used when the title and caption are set before drawing the data.
		"""

		self.redraw()
		plt.show(*args, **kwargs)

	def __getattr__(self, name):
		"""
		Get an attribute indicated by `name` from the class.
		If it gets to this point, then the attribute does not exist.
		Instead, it is retrieved from the :class:`~Drawable` axis.

		:param name: The name of the attribute.
		:type name: str

		:return: The function applied on the axis.
		:rtype: function
		"""

		def method(*args, **kwargs):
			"""
			Try to get the attribute from the axis.
			If arguments were given, then the attribute is treated as a method call.
			Otherwise, it is treated as a normal attribute call.
			"""

			if callable(getattr(self.axis, name)):
				return getattr(self.axis, name)(*args, **kwargs)
			else:
				return getattr(self.axis, name)

		return method

	"""
	Visualizations
	"""

	def annotate(self, text, x, y, marker=None, pad=0.01, *args, **kwargs):
		"""
		Add an annotation to the plot.
		Any additional arguments and keyword arguments are passed on to the annotation's :func:`~text.text.Annotation.draw` function.
		For example, the `va` can be provided to specify the vertical alignment.
		The `align` parameter can be used to specify the text's alignment.

		:param text: The text of the annotation to draw.
		:type text: str
		:param x: A tuple containing the start and end x-coordinates of the annotation.
		:type x: tuple
		:param y: The y-coordinate of the annotation.
		:type y: float
		:param marker: The marker style.
					   If it is not given, no marker is drawn.
		:type marker: None or dict
		:param pad: The amount of padding applied to the annotation.
		:type pad: float

		:return: The drawn annotation.
		:rtype: :class:`~text.annotation.Annotation`
		"""

		annotation = Annotation(self)

		"""
		Draw the marker if it is given.
		The color is obtained from the kwargs if a marker color is not given.
		The point of the marker is based on the alignment of the annotation.
		"""
		if marker is not None:
			marker = dict(marker) # make a copy to avoid overwriting dictionaries
			marker['color'] = marker.get('color', kwargs.get('color'))
			if kwargs.get('align', 'left') == 'left':
				self.axis.plot(x[0], y, *args, **marker)
			elif kwargs.get('align') == 'right':
				self.axis.plot(x[1], y, *args, **marker)
			elif kwargs.get('align') == 'center':
				self.axis.plot((x[0] + x[1])/2., y, *args, **marker)

		tokens = annotation.draw(text, x, y, pad=pad, *args, **kwargs)
		self.annotations.append(annotation)

		return annotation

	def draw_bar_100(self, *args, **kwargs):
		"""
		Draw a bar chart that stacks up to 100% on this :class:`~Drawable`.
		The arguments and keyword arguments are those supported by :func:`~bar.100.Bar100.draw` method.

		:return: A list of drawn bars.
		:rtype: list of :class:`matplotlib.patches.Rectangle`
		"""

		self.bar100 = self.bar100 if self.bar100 else Bar100(self)
		return self.bar100.draw(*args, **kwargs)

	def draw_graph(self, *args, **kwargs):
		"""
		Draw a graph visualization on this :class:`~Drawable`.
		The arguments and keyword arguments are those supported by :func:`~graph.graph.Graph.draw` method.

		:return: A tuple containing the list of drawn nodes, the rendered node names, edges, and the rendered edge names.
		:rtype: tuple
		"""

		graph = Graph(self)
		return graph.draw(*args, **kwargs)

	def draw_text_annotation(self, *args, **kwargs):
		"""
		Draw a text annotation visualization on this :class:`~Drawable`.
		The arguments and keyword arguments are those supported by :func:`~text.annotation.TextAnnotation.draw` method.

		:return: The drawn text annotation's lines.
				 Each line is made up of tuples of lists.
				 The first list in each tuple is the list of legend labels.
				 The second list in each tuple is the list of actual tokens.
		:rtype: list of tuple
		"""

		text_annotation = TextAnnotation(self)
		return text_annotation.draw(*args, **kwargs)

	def draw_time_series(self, *args, **kwargs):
		"""
		Draw a time series visualization on this :class:`~Drawable`.
		The arguments and keyword arguments are those supported by :func:`~timeseries.timeseries.TimeSeries.draw` method.

		:return: A tuple made up of the drawn plot and label.
		:rtype: tuple
		"""

		self.timeseries = self.timeseries if self.timeseries else TimeSeries(self)
		return self.timeseries.draw(*args, **kwargs)
