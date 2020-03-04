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
	:vartype timeseries: :class:`~timeseries.timeseries.TimeSeries`
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
		self.caption.draw(caption, (0, 1), 1, va='bottom', alpha=alpha, lineheight=lineheight, *args, **kwargs, transform=self.axis.transAxes)
		self.redraw()
		return self.caption

	def redraw(self):
		"""
		Re-create the title with the necessary padding to fit the caption and the legend.
		"""

		"""
		Move the caption up to make space for the legend.
		"""
		legend_bb = self.legend.get_virtual_bb(transform=self.axis.transAxes)
		self.caption.set_position((0, 1 + 0.01 + legend_bb.height),
								   ha='left', va='bottom', transform=self.axis.transAxes)

		"""
		Get the height of the caption and the height of the legend.
		The title should allow enough padding to make space for both.
		"""
		title = self.axis.get_title(loc='left')
		caption_bb = self.axis.transData.transform(self.caption.get_virtual_bb())
		height = abs(caption_bb[0][1] - caption_bb[1][1])
		legend_bb = self.axis.transData.transform(self.legend.get_virtual_bb())
		height += abs(legend_bb[0][1] - legend_bb[1][1])
		pad_px = self.axis.transAxes.transform((0, 0.01))[1] - self.axis.transAxes.transform((0, 0))[1]
		self.axis.set_title(title, loc='left', pad=(5 + height + pad_px * 2))

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

	def draw_text_annotation(self, *args, **kwargs):
		"""
		Draw a text annotation visualization on this :class:`~Drawable`.
		The arguments and keyword arguments are those supported by :meth:`~text.annotation.TextAnnotation.draw` method.

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
		The arguments and keyword arguments are those supported by :meth:`~text.annotation.TextAnnotation.draw` method.

		:return: A tuple made up of the drawn plot and label.
		:rtype: tuple
		"""

		self.timeseries = self.timeseries if self.timeseries is not None else TimeSeries(self)
		return self.timeseries.draw(*args, **kwargs)

	def annotate(self, text, x, y, marker=None, pad=0.01, *args, **kwargs):
		"""
		Add an annotation to the plot.
		Any additional arguments and keyword arguments are passed on to the annotation's :meth:`~text.text.Annotation.draw` function.
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
		"""

		annotation = Annotation(self)

		"""
		Draw the marker if it is given.
		The color is obtained from the kwargs if a marker color is not given.
		The point of the marker is based on the alignment of the annotation.
		"""
		if marker is not None:
			marker['color'] = marker.get('color', kwargs.get('color'))
			if kwargs.get('align', 'left') == 'left':
				self.axis.plot(x[0], y, *args, **marker)
			elif kwargs.get('align') == 'right':
				self.axis.plot(x[1], y, *args, **marker)
			elif kwargs.get('align') == 'center':
				self.axis.plot((x[0] + x[1])/2., y, *args, **marker)

		tokens = annotation.draw(text, x, y, pad=pad, *args, **kwargs)
		self.annotations.append(annotation)

		return tokens
