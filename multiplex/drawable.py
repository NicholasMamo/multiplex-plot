"""
A :class:`~Drawable` is nothing more than a class that wraps a matplotlib figure and an axes.
All of the functions that you would call on a `matplotlib axes <https://matplotlib.org/api/axes_api.html>`_, you can call on the :class:`~Drawable`.
If you call any function that belongs to a `matplotlib axes <https://matplotlib.org/api/axes_api.html>`_, then matplotlib handles it as usual.
However, if you call a function that is new to Multiplex, such as a new visualization, then the library handles it.

To create a :class:`~Drawable` instance from a normal plot:

.. code-block:: python

  viz = drawable.Drawable(plt.figure(figsize=(10, 5)))

To create a :class:`~Drawable` instance from an axes, or a subplot:

.. code-block:: python

  figure, axes = plt.subplots(2, 1, figsize=(10, 10))
  viz = drawable.Drawable(figure, axes[0])

Some important functionality that the :class:`~Drawable` class provides:

- The :func:`~drawable.Drawable.set_caption` function.
  This function sets a caption under the title so that readers immediately know what the visualization is about.
- The :func:`~drawable.Drawable.savefig` and :func:`~drawable.Drawable.show` functions.
  These functions mirror matplotlib's `savefig <https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.savefig.html>`_ and `show <https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.show.html>`_ functions respectively.
  When you call these functions, the :class:`~Drawable` re-draws the visualization, making sure that the title, caption and legend do not overlap.
- The :func:`~drawable.Drawable.annotate` function.
  You can call this function to add text to any plot.
  This function is useful to point to information that is not immediately obvious, or to draw your readers' attention.
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
	The :class:`~Drawable` class wraps a matplotlib figure and axes to provide additional functionality.
	If no axes is given, the default plot axes (:code:`plt.gca()`) is used.
	The :class:`~Drawable` class can be used as a normal `matplotlib.axes.Axes <https://matplotlib.org/api/axes_api.html>`_ object with additional functionality.
	The axes functionality can be called on the :class:`~Drawable` class.
	The :class:`~Drawable` instance re-routes method and attribute calls to the `matplotlib.axes.Axes <https://matplotlib.org/api/axes_api.html>`_ instance.

	:ivar figure: The figure that the :class:`~Drawable` class wraps.
	:vartype figure: :class:`matplotlib.figure.Figure`
	:ivar axes: The axes where the drawable will draw.
	:vartype axes: :class:`matplotlib.axes.Axes`
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

	def __init__(self, figure, axes=None):
		"""
		Create the drawable with the figure.

		:param figure: The figure that the :class:`~Drawable` class wraps.
					   This is mainly used to get the figure renderer.
		:type figure: :class:`matplotlib.figure.Figure`
		:param axes: The axes (or subplot) where to plot visualizations.
					 If `None` is given, the plot's main subplot is used instead.
		:type axes: `None` or :class:`matplotlib.axes.Axes`
		"""

		self.figure = figure
		self.axes = plt.gca() if axes is None else axes
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

		:param caption: The caption to add to the axes.
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
						  transform=self.axes.transAxes,
						  *args, **kwargs)
		self.redraw()
		return self.caption

	def redraw(self):
		"""
		Re-create the title, with the goal of leaving enough space to fit the caption and the legend.
		Afterwards, it redraws the legend.
		"""

		self._redraw_title()
		self._redraw_caption()
		self.legend.redraw()

	def _redraw_caption(self):
		"""
		Re-draw the caption, re-positioning so that it does not overlap with the legend or axes.
		"""

		figure, axes = self.figure, self.axes

		"""
		Move the caption up to make space for the legend and the label.
		"""
		y = 1
		y += self.legend.get_virtual_bb(transform=self.axes.transAxes).height

		"""
		If the x-label is on top, make space for it in the caption.
		In this case, it is assumed that the ticks are also at the top.
		This is because for some reason they may be set to 'unknown'.
		"""
		if axes.xaxis.get_label_position() == 'top':
			y += self._get_xlabel(transform=self.axes.transAxes).height * 2

			xtick_labels_bb = self._get_xtick_labels(transform=axes.transAxes)
			if xtick_labels_bb:
				y += max(xtick_labels_bb, key=lambda bb: bb.height).height * 2

		pad = 0.1
		self.caption.set_position((0, y + pad), ha='left', va='bottom', transform=self.axes.transAxes)

	def _redraw_title(self):
		"""
		Re-draw the title, adding enough padding so that there is enough space for the axes label, the legend and the caption.
		"""

		figure, axes = self.figure, self.axes

		title = axes.get_title(loc='left')

		"""
		Get the height of the caption and the height of the legend.
		The title should allow enough padding to make space for both.
		"""
		caption_height = 0
		if str(self.caption):
			caption_height = util.to_px(axes, self.caption.get_virtual_bb(transform=axes.transAxes),
										transform=axes.transAxes).height

		legend_height = util.to_px(axes, self.legend.get_virtual_bb(transform=axes.transAxes),
								   transform=axes.transAxes).height

		"""
		If the x-label is on top, make space for it in the title.
		In this case, it is assumed that the ticks are also at the top.
		This is because for some reason they may be set to 'unknown'.
		"""
		label_height = 0
		if axes.xaxis.get_label_position() == 'top':
			label_bb = self._get_xlabel(transform=axes.transData)
			label_height = util.to_px(axes, label_bb,
									  transform=axes.transData).height * 2
			xtick_labels_bb = self._get_xtick_labels(transform=axes.transData)
			if xtick_labels_bb:
				label_bb = max(xtick_labels_bb, key=lambda bb: bb.height)
				label_height += util.to_px(axes, label_bb, transform=axes.transData).height * 2

		"""
		Add some extra padding to the height.
		"""
		height = abs(caption_height) + abs(legend_height) + abs(label_height)
		pad_px = abs(self.axes.transAxes.transform((0, 0.05))[1] - self.axes.transAxes.transform((0, 0))[1])
		pad = pad_px * 2
		self.axes.set_title(title, loc='left', pad=(5 + height + pad))

	def _get_xlabel(self, transform=None):
		"""
		Get the bounding box of the x-axis label.

		:param transform: The bounding box transformation.
						  If `None` is given, the data transformation is used.
		:type transform: None or :class:`matplotlib.transforms.TransformNode`

		:return: The bounding box of the x-axis label.
		:rtype: :class:`matplotlib.transforms.Bbox`
		"""

		figure, axes = self.figure, self.axes

		transform = transform or axes.transData
		return util.get_bb(figure, axes, axes.xaxis.get_label(), transform=transform)

	def _get_xtick_labels(self, transform=None):
		"""
		Get the bounding box of the x-axis tick labels.

		:param transform: The bounding box transformation.
						  If `None` is given, the data transformation is used.
		:type transform: None or :class:`matplotlib.transforms.TransformNode`

		:return: The bounding box of the x-axis label.
		:rtype: :class:`matplotlib.transforms.Bbox`
		"""

		figure, axes = self.figure, self.axes

		figure.canvas.draw()
		transform = transform or axes.transData
		return [ util.get_bb(figure, axes, label, transform=transform)
				 for label in axes.xaxis.get_ticklabels(which='both') ]

	def savefig(self, *args, **kwargs):
		"""
		A special function that calls the `matplotlib.pyplot.savefig <https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.savefig.html>`_ function.
		Before doing that, the function first redraws the drawable.

		This function is very important when the title and caption are set before drawing the visualization.
		In these cases, it is possible that the legend or the plot labels cause the caption or title to overlap with the plot.
		"""

		self.redraw()
		plt.savefig(*args, **kwargs)

	def show(self, *args, **kwargs):
		"""
		A special function that calls the `matplotlib.pyplot.show <https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.show.html>`_ function.
		Before doing that, the function first redraws the drawable.

		This function is very important when the title and caption are set before drawing the visualization.
		In these cases, it is possible that the legend or the plot labels cause the caption or title to overlap with the plot.
		"""

		self.redraw()
		plt.show(*args, **kwargs)

	def __getattr__(self, name):
		"""
		The magic function through which most of :class:`~Drawable`'s functionality passes.
		This function receives any unknown call and passes it on to the :class:`~Drawable`'s `matplotlib.axes.Axes <https://matplotlib.org/api/axes_api.html>`_.
		This function automatically checks whether the call is referencing a function or a variable.

		:param name: The name of the attribute.
		:type name: str

		:return: The function applied on the axes.
		:rtype: function
		"""

		def method(*args, **kwargs):
			"""
			Try to get the attribute from the axes.
			If arguments were given, then the attribute is treated as a method call.
			Otherwise, it is treated as a normal attribute call.
			"""

			if callable(getattr(self.axes, name)):
				return getattr(self.axes, name)(*args, **kwargs)
			else:
				return getattr(self.axes, name)

		return method

	"""
	Visualizations
	"""

	def annotate(self, text, x, y, marker=None, pad=0.01, *args, **kwargs):
		"""
		Add a text annotation to the plot.
		This function can be used to draw attention to certain or describe the visualization on the plot itself.

		Any additional arguments and keyword arguments are passed on to the :class:`~text.annotation.Annotation`'s :func:`~text.annotation.Annotation.draw` function.
		For example, the `va` can be provided to specify the text's vertical alignment, andthe `align` parameter can be used to specify the text's alignment.

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
				self.axes.plot(x[0], y, *args, **marker)
			elif kwargs.get('align') == 'right':
				self.axes.plot(x[1], y, *args, **marker)
			elif kwargs.get('align') == 'center':
				self.axes.plot((x[0] + x[1])/2., y, *args, **marker)

		tokens = annotation.draw(text, x, y, pad=pad, *args, **kwargs)
		self.annotations.append(annotation)

		return annotation

	def draw_bar_100(self, *args, **kwargs):
		"""
		Draw a bar chart that stacks up to 100% on this :class:`~Drawable`.
		The arguments and keyword arguments are those supported by the :class:`~bar.bar100.Bar100`'s :func:`~bar.bar100.Bar100.draw` method.

		:return: A list of drawn bars.
		:rtype: list of :class:`matplotlib.patches.Rectangle`
		"""

		self.bar100 = self.bar100 if self.bar100 else Bar100(self)
		return self.bar100.draw(*args, **kwargs)

	def draw_graph(self, *args, **kwargs):
		"""
		Draw a graph visualization on this :class:`~Drawable`.
		The arguments and keyword arguments are those supported by the :class:`~graph.graph.Graph`'s :func:`~graph.graph.Graph.draw` method.

		:return: A tuple containing the list of drawn nodes, the rendered node names, edges, and the rendered edge names.
		:rtype: tuple
		"""

		graph = Graph(self)
		return graph.draw(*args, **kwargs)

	def draw_text_annotation(self, *args, **kwargs):
		"""
		Draw a text annotation visualization on this :class:`~Drawable`.
		The arguments and keyword arguments are those supported by the :class:`~text.text.TextAnnotation`'s :func:`~text.text.TextAnnotation.draw` method.

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
		The arguments and keyword arguments are those supported by the :class:`~timeseries.timeseries.TimeSeries`' :func:`~timeseries.timeseries.TimeSeries.draw` method.

		:return: A tuple made up of the drawn plot and label.
		:rtype: tuple
		"""

		self.timeseries = self.timeseries if self.timeseries else TimeSeries(self)
		return self.timeseries.draw(*args, **kwargs)
