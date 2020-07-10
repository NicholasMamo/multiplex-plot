"""
Legends are a common sight in visualizations, and a helpful one at that.
Multiplex places legends just beneath the caption and above the plot.
That way, readers can understand how to interpret the visualization before seeing it.

.. image:: ../examples/exports/3-time-series.png
   :class: example

Apart from drawing the annotations, the legend aligns and organizes them on different lines.
"""

import os
import sys

from matplotlib import collections, lines, text, rcParams
from matplotlib.transforms import Bbox

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from text.annotation import Annotation
import util

class Legend(object):
	"""
	The legend is made up of tuples: a visual element and a short label describing what they represent.
	The legend class stores these and the :class:`~drawable.Drawable` as instance variables.

	All of the drawn legend annotations go through the :func:`~legend.Legend.draw` decorator.
	This function first draws the visual part of the annotation.
	Then, it draws the label next to it.
	This function is also responsible to lay out the legend annotations, creating new lines when necessary.

	:ivar drawable: The :class:`~drawable.Drawable` where the legend will be drawn.
	:vartype drawable: :class:`~drawable.Drawable`
	:ivar lines: The legend components, separated into lines.
				 Each component is a tuple of the visual representation and the associated label.
	:vartype lines: list of list of tuple
	"""

	def __init__(self, drawable):
		"""
		Create the legend.

		:param drawable: The :class:`~drawable.Drawable` where the legend will be drawn.
		:type drawable: :class:`~drawable.Drawable`
		"""

		self.lines = [ [ ] ]
		self.drawable = drawable

	def draw(f):
		"""
		This function is the most important one in the :class:`~legend.Legend` class.
		This decorator wraps all of the legend annotations and draws them in three steps:

		1. First, it draws the visual part of the legend annotation.
		2. Second, it draws the textual label next to the visual part.
		3. Third, it adds a new line to the legend if need be.

		:param f: The function to wrap.
		:type f: function

		:return: The wrapped function.
		:rtype: function
		"""

		def wrapper(self, label, label_style=None, *args, **kwargs):
			"""
			Call the test function with any arguments and keyword arguments.

			:param label: The text of the legend label.
			:type label: str
			:param label_style: The style of the label.
								If `None` is given, a default style is used.
			:type label_style: None or dict

			:return: A tuple containing the drawn visual and the annotation.
			:rtype: tuple
			"""

			figure = self.drawable.figure
			axes = self.drawable.axes

			"""
			If the label is already in the legend, return it.
			"""
			drawn = self._contains(label)
			if drawn:
				return drawn

			"""
			Load the default legend style and update the styling.
			If a custom style is given, it overwrites the styling.
			"""
			label_style = label_style or { }
			default_style = self._get_legend_params('fontsize')
			default_style.update(label_style)
			default_style['alpha'] = default_style.get('alpha', 0.8)

			"""
			Get the x and y offsets for the new legend.
			Then, draw the line first and the annotation second.
			"""
			offset = self._get_offset(transform=axes.transAxes)
			linespacing = util.get_linespacing(figure, axes, transform=axes.transAxes, **default_style)
			y = 1.05
			if axes.xaxis.get_label_position() == 'top':
				y += self.drawable._get_xlabel(transform=axes.transAxes).height * 2

				xtick_labels_bb = self.drawable._get_xtick_labels(transform=axes.transAxes)
				if xtick_labels_bb:
					y += max(xtick_labels_bb, key=lambda bb: bb.height).height * 2

			visual = f(self, *args, offset=offset, y=y, linespacing=linespacing, **kwargs)

			"""
			Calculate the offset of the annotation.
			"""
			if visual:
				offset = util.get_bb(figure, axes, visual, transform=axes.transAxes).x1 + 0.00625
			annotation = self.draw_annotation(label, offset, y, **default_style)

			"""
			If need be, create a new line for the legend.
			"""
			if annotation.get_virtual_bb(transform=axes.transAxes).x1 > 1:
				self._newline(visual, annotation, linespacing)
			else:
				self.lines[-1].append((visual, annotation))

			self.drawable.redraw()
			return (visual, annotation)

		wrapper.__doc__ = f.__doc__
		return wrapper

	def redraw(self):
		"""
		Redraw the legend.
		This function only has an effect when the x-axis label and ticks are at the top, instead of at the bottom.
		In this case, this function moves the legend up to make room for the label and ticks.
		"""

		figure, axes = self.drawable.figure, self.drawable.axes

		"""
		If the legend is empty, do nothing.
		"""
		if not(self.lines[-1]):
			return

		"""
		Get the position at which the legend should be.
		"""
		y = 1.05
		if axes.xaxis.get_label_position() == 'top':
			y += self.drawable._get_xlabel(transform=axes.transAxes).height * 2

			xtick_labels_bb = self.drawable._get_xtick_labels(transform=axes.transAxes)
			if xtick_labels_bb:
				y += max(xtick_labels_bb, key=lambda bb: bb.height).height * 2

		"""
		Get the position of the last line.
		"""
		bottom = self.get_virtual_bb(transform=axes.transAxes).y0

		"""
		If the legend is below the x-axis label and tick labels, move all lines up by that amount.
		"""
		if bottom < y:
			offset = y - bottom
			for line in self.lines:
				for (visual, annotation) in line:
					"""
					Move the visual first, then the text.
					"""
					if visual:
						bb = util.get_bb(figure, axes, visual, transform=axes.transAxes)
						if type(visual) == lines.Line2D:
							visual.set_ydata([ bb.y0 + offset ] * 2)
						elif type(visual) == text.Annotation:
							visual.xyann = (bb.x0, bb.y1 + offset)
							visual.xy = (bb.x1, bb.y1 + offset)
						elif type(visual) == collections.PathCollection:
							offsets = visual.get_offsets()[0]
							visual.set_offsets([[ offsets[0], offsets[1] + offset ]])

					bb = annotation.get_virtual_bb(transform=axes.transAxes)
					annotation.set_position((bb.x0, bb.y0 + offset), transform=axes.transAxes)

	def draw_annotation(self, label, x, y, va='bottom', *args, **kwargs):
		"""
		Draw a text annotation.
		This function is called by the :func:`~legend.Legend.draw` function after drawing the visual part of the legend annotation.

		The text annotation is based on the :class:`~text.annotation.Annotation` class.
		The arguments and keyword arguments are passed on to the :func:`~text.annotation.Annotation.draw` function.

		:param label: The text of the legend label.
		:type label: str
		:param x: The starting x-coordinate of the annotation.
		:type x: float
		:param y: The y-coordinate of the annotation.
		:type y: float
		:param va: The vertical alignment, can be one of `top`, `center` or `bottom`.
				   If the vertical alignment is `top`, the given y-coordinate becomes the highest point of the annotation.
				   If the vertical alignment is `center`, the given y-coordinate becomes the center point of the annotation.
				   If the vertical alignment is `bottom`, the given y-coordinate becomes the lowest point of the annotation.
		:type va: str

		:return: The drawn annotation.
		:rtype: :class:`~text.annotation.Annotation`
		"""

		figure = self.drawable.figure
		axes = self.drawable.axes

		annotation = Annotation(self.drawable)
		annotation.draw(label, (x, 1), y, va=va, transform=axes.transAxes, **kwargs)
		return annotation

	@draw
	def draw_text_only(self, *args, **kwargs):
		"""
		draw_text_only(self, *args, **kwargs)

		Draw nothing as the visual part of the annotation.
		This is used for text-based annotations that require no visual annotation.

		:return: `None`
		:rtype: None
		"""

		return None

	@draw
	def draw_arrow(self, offset, y=1, linespacing=1, *args, **kwargs):
		"""
		draw_arrow(self, offset, y=1, linespacing=1, *args, **kwargs)

		Draw an arrow visual annotation.
		Any additional arguments and keyword arguments are provided to the `matplotlib.text.Annotation <https://matplotlib.org/3.2.2/tutorials/text/annotations.html>`_ class.

		:param offset: The x-offset where to draw the annotation.
		:type offset: float
		:param y: The y-position of the annotation.
		:type y: float
		:param linespacing: The linespacing of the accompanying text annotation.
		:type linespacing: float

		:return: The drawn arrow.
		:rtype: :class:`matplotlib.text.annotation`
		"""

		figure = self.drawable.figure
		axes = self.drawable.axes

		arrow = text.Annotation('', xy=(offset + 0.025, y - linespacing / 2.),
								xytext=(offset, y - linespacing / 2.),
								xycoords=axes.transAxes, textcoords=axes.transAxes, arrowprops=kwargs)
		arrow.set_clip_on(False)
		axes.add_artist(arrow)

		return arrow

	@draw
	def draw_line(self, offset, y=1, linespacing=1, horizontal=True, *args, **kwargs):
		"""
		draw_line(self, offset, y=1, linespacing=1, horizontal=True, *args, **kwargs)

		Draw a line visual annotation.
		Any additional arguments and keyword arguments are provided to the `matplotlib.lines.Line2D <https://matplotlib.org/3.2.2/api/_as_gen/matplotlib.lines.Line2D.html>`_ class.

		:param offset: The x-offset where to draw the annotation.
		:type offset: float
		:param y: The y-position of the annotation.
		:type y: float
		:param linespacing: The linespacing of the accompanying text annotation.
		:type linespacing: float
		:param horizontal: A boolean indicating whether the line should be horizontal.
		:type horizontal: bool

		:return: The drawn line.
		:rtype: :class:`matplotlib.lines.Line2D`
		"""

		figure = self.drawable.figure
		axes = self.drawable.axes

		x = [ offset, offset + 0.0125 ] if horizontal else [ offset ] * 2
		y = [ y + linespacing / 2. ] * 2 if horizontal else [ y, y + linespacing ]
		line = lines.Line2D(x, y, transform=axes.transAxes, *args, **kwargs)
		line.set_clip_on(False)
		axes.add_line(line)

		return line

	@draw
	def draw_point(self, offset, y=1, linespacing=1, *args, **kwargs):
		"""
		draw_point(self, offset, y=1, linespacing=1, *args, **kwargs)

		Draw a scatter point visual annotation.
		Any additional arguments and keyword arguments are provided to the `matplotlib.pyplot.scatter <https://matplotlib.org/3.2.2/api/_as_gen/matplotlib.pyplot.scatter.html>`_ class.

		:param offset: The x-offset where to draw the annotation.
		:type offset: float
		:param y: The y-position of the annotation.
		:type y: float
		:param linespacing: The linespacing of the accompanying text annotation.
		:type linespacing: float

		:return: The drawn point.
		:rtype: :class:`matplotlib.collections.PathCollection`
		"""

		figure = self.drawable.figure
		axes = self.drawable.axes

		"""
		Update the offset by by calculating the x-radius of the point.
		"""
		kwargs['s'] = 100
		origin = self.drawable.axes.transAxes.inverted().transform((0, 0))
		x = (self.drawable.axes.transAxes.inverted().transform((kwargs['s'] ** 0.5, 0))[0] - origin[0]) / 2.
		offset += x

		point = axes.scatter(offset, y + linespacing / 2., transform=axes.transAxes, *args, **kwargs)
		point.set_clip_on(False)

		return point

	def get_virtual_bb(self, transform=None):
		"""
		Get the bounding box of the entire annotation.
		This is called a virtual bounding box because it is not a real bounding box.
		Rather, it is the smallest rectangular bounding box that covers all of the bounding boxes of the legend.

		:param transform: The bounding box transformation.
						  If `None` is given, the data transformation is used.
		:type transform: None or :class:`matplotlib.transforms.TransformNode`

		:return: The bounding box of the legend.
				 This bounding box covers all of the annotations in the legend.
		:rtype: :class:`matplotlib.transforms.Bbox`
		"""

		figure = self.drawable.figure
		axes = self.drawable.axes

		transform = axes.transData if transform is None else transform

		"""
		If there are lines that are not empty, get the bounding boxes from the first and last lines.
		The virtual bounding box's top value is equivalent to the first line's highest point.
		The virtual bounding box's bottom value is equivalent to the last line's lowest point.
		"""
		if self.lines:
			top = self.lines[0]
			bottom = self.lines[-1]

			"""
			If the lines are empty, return a flat bounding box.
			Otherwise, get the maximum and minimum points of these bounding boxes.
			"""
			if not len(top) or not len(bottom):
				return Bbox(((0, 1), (1, 1)))

			y1 = max( annotation.get_virtual_bb(transform=transform).y1 for _, annotation in top )
			y0 = min( annotation.get_virtual_bb(transform=transform).y0 for _, annotation in bottom )
			return Bbox(((0, y0), (1, y1)))

	def _contains(self, label):
		"""
		Check whether the legend already contains a legend for the given label.
		If it exists, the visual and the annotation are returned as a tuple.

		:param label: The label to look for.
		:type label: str

		:return: Check whether the legend already contains the given label.
				 If it exists, the visual and the annotation are returned as a tuple.
		:rtype: tuple or None
		"""

		for line in self.lines:
			for visual, annotation in line:
				if str(annotation) == label:
					return (visual, annotation)

	def _get_offset(self, pad=0.025, transform=None):
		"""
		Get the x-coordinate offset for the next legend.

		:param pad: The padding to add to the offset.
					This padding is not added if there are no legends in the line.
		:type pad: float
		:param transform: The bounding box transformation.
						  If `None` is given, the data transformation is used.
		:type transform: None or :class:`matplotlib.transforms.TransformNode`

		:return: The x-coordinate offset for the next legend.
		:rtype: float
		"""

		if self.lines:
			last = self.lines[-1]
			if last:
				(visual, annotation) = last[-1]
				return annotation.get_virtual_bb(transform).x1 + pad

		return 0

	def _newline(self, visual, annotation, linespacing, va='bottom'):
		"""
		Create a new line with the given legend.

		:param visual: The visual of the legend.
		:type visual: object
		:param annotation: The drawn annotation.
		:type annotation: :class:`~text.annotation.Annotation`
		:param linespacing: The space between lines.
		:type linespacing: float
		:param va: The vertical alignment, can be one of `top`, `center` or `bottom`.
				   If the vertical alignment is `top`, the given y-coordinate becomes the highest point of the annotation.
				   If the vertical alignment is `center`, the given y-coordinate becomes the center point of the annotation.
				   If the vertical alignment is `bottom`, the given y-coordinate becomes the lowest point of the annotation.
		:type va: str
		"""

		figure = self.drawable.figure
		axes = self.drawable.axes

		"""
		Go through each line and move all of its components one line up.
		"""
		for line in self.lines:
			for push_visual, push_annotation in line:
				"""
				The lines that have been drawn can be pushed up by the height of the line.
				"""
				if push_visual:
					bb = util.get_bb(figure, axes, push_visual, transform=axes.transAxes)
					if type(push_visual) == lines.Line2D:
						push_visual.set_ydata([ bb.y0 + linespacing ] * 2)
					elif type(push_visual) == text.Annotation:
						push_visual.xyann = (bb.x0, bb.y1 + linespacing / 2.)
						push_visual.xy = (bb.x1, bb.y1 + linespacing / 2.)
					elif type(push_visual) == collections.PathCollection:
						offsets = push_visual.get_offsets()[0]
						push_visual.set_offsets([[ offsets[0], offsets[1] + linespacing ]])

				"""
				The annotations are moved differently depending on the vertical alignment.
				If the vertical alignment is `top`, the annotation is moved from the top.
				If the vertical alignment is `center`, the annotation is moved from the center.
				If the vertical alignment is `bottom`, the annotation is moved from the bottom.
				"""
				bb = push_annotation.get_virtual_bb(transform=axes.transAxes)
				if va == 'top':
					y = bb.y1
				elif va == 'center':
					y = (bb.y0 + bb.y1) / 2.
				elif va == 'bottom':
					y = bb.y0

				push_annotation.set_position((bb.x0, y + linespacing), va=va, transform=axes.transAxes)

		"""
		Move the visual and the annotation to the start of the line.
		Finally, create a new line container.
		"""
		if visual:
			bb = util.get_bb(figure, axes, visual, transform=axes.transAxes)
			if type(visual) == lines.Line2D:
				visual.set_xdata([ 0, 0.025 ])
			elif type(visual) == text.Annotation:
				visual.xyann = (0, bb.y0 + linespacing / 2.)
				visual.xy = (0.025, bb.y0 + linespacing / 2.)
			elif type(push_visual) == collections.PathCollection:
				origin = self.drawable.axes.transData.inverted().transform((0, 0))
				x = (self.drawable.axes.transData.inverted().transform((100 ** 0.5, 0))[0] - origin[0]) / 4.
				visual.set_offsets([[ x, 1 + linespacing / 2. ]])

		annotationbb = annotation.get_virtual_bb(transform=axes.transAxes)
		annotation.set_position((bb.width + 0.00625, 1), va=va, transform=axes.transAxes)
		self.lines.append( [ (visual, annotation) ] )

	def _get_legend_params(self, *args):
		"""
		Read the style parameters for the legend.

		:return: An array containing the legend parameters.
				 If arguments are given, only parameters in the arguments are returned.
		:rtpe: dict
		"""

		params = { param: rcParams[param] for param in rcParams if param.startswith('legend') }
		params = { param[ param.index('.') + 1: ]: params[param] for param in params }
		if args:
			params = { param: params[param] for param in params if param in args }

		return params
