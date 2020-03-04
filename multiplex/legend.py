"""
Legends are a common sight in visualizations, and a helpful one as well.
They give a name to the components that you include in your visualization.

.. image:: ../examples/exports/3-time-series.png
   :class: example

Legends are alternatives to inline labels in time series.
Multiplex's legends are drawn just below the caption.
In this way, users can look at the drawn data and understand it immediately.
"""

import os
import sys

from matplotlib import lines, rcParams
from matplotlib.transforms import Bbox

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from text.annotation import Annotation
import util

class Legend(object):
	"""
	The legend is made up of visual elements and a short label describing what they represent.

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

	def draw_line(self, label, label_style=None, *args, **kwargs):
		"""
		Draw a line legend for the given label.
		Any additional arguments and keyword arguments are provided to the plotting function.

		:param label: The text of the legend label.
		:type label: str
		:param label_style: The style of the label.
							If `None` is given, a default style is used.
		:type label_style: None or dict

		:return: A tuple made up of the function return value and the drawn label.
		:rtype: tuple
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis

		label_style = label_style or { 'alpha': 0.8 }
		default_style = self._get_legend_params('fontsize')
		default_style.update(label_style)

		"""
		Get the offset for the new legend.
		Then, draw the line first and the annotation second.
		"""
		offset = self._get_offset(transform=axis.transAxes)
		linespacing = util.get_linespacing(figure, axis, transform=axis.transAxes, **default_style)

		line = lines.Line2D([ offset, offset + 0.025 ], [ 1 + linespacing / 2. ] * 2,
							transform=axis.transAxes, *args, **kwargs)
		line.set_clip_on(False)
		axis.add_line(line)

		"""
		Load the default legend style and update the styling.
		If a custom style is given, it overwrites the styling.
		"""
		line_offset = util.get_bb(figure, axis, line, transform=axis.transAxes).x1 + 0.00625
		annotation = self.draw_annotation(label, line_offset, 1, **default_style)
		if annotation.get_virtual_bb(transform=axis.transAxes).x1 > 1:
			self._newline(line, annotation, linespacing)
		else:
			self.lines[-1].append((line, annotation))

		self.drawable.redraw()
		return (line, annotation)

	def draw_annotation(self, label, x, y, va='bottom', *args, **kwargs):
		"""
		Get the annotation for the legend.
		The arguments and keyword arguments are passed on to the :meth:`~text.annotation.Annotation.draw` function.

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
		axis = self.drawable.axis

		annotation = Annotation(self.drawable)
		annotation.draw(label, (x, 1), y, va=va, transform=axis.transAxes, **kwargs)
		return annotation

	def get_virtual_bb(self, transform=None):
		"""
		Get the bounding box of the entire annotation.
		This is called a virtual bounding box because it is not a real bounding box.
		Rather, it is a bounding box that covers all of the bounding boxes of the legend.

		.. note::

			The legend always spans the entire x-axis.

		:param transform: The bounding box transformation.
						  If `None` is given, the data transformation is used.
		:type transform: None or :class:`matplotlib.transforms.TransformNode`

		:return: The bounding box of the annotation.
		:rtype: :class:`matplotlib.transforms.Bbox`
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis

		transform = axis.transData if transform is None else transform

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
		axis = self.drawable.axis

		"""
		Go through each line and move all of its components one line up.
		"""
		for line in self.lines:
			for push_visual, push_annotation in line:
				"""
				The lines can be pushed up by the height of the line.
				"""
				bb = util.get_bb(figure, axis, push_visual, transform=axis.transAxes)
				push_visual.set_ydata([ bb.y0 + linespacing ] * 2)

				"""
				The annotations are moved differently depending on the vertical alignment.
				If the vertical alignment is `top`, the annotation is moved from the top.
				If the vertical alignment is `center`, the annotation is moved from the center.
				If the vertical alignment is `bottom`, the annotation is moved from the bottom.
				"""
				bb = push_annotation.get_virtual_bb(transform=axis.transAxes)
				if va == 'top':
					y = bb.y1
				elif va == 'center':
					y = (bb.y0 + bb.y1) / 2.
				elif va == 'bottom':
					y = bb.y0

				push_annotation.set_position((bb.x0, y + linespacing), va=va, transform=axis.transAxes)

		"""
		Move the visual and the annotation to the start of the line.
		Finally, create a new line container.
		"""
		visualbb = util.get_bb(figure, axis, visual, transform=axis.transAxes)
		visual.set_xdata([ 0, 0.025 ])
		annotationbb = annotation.get_virtual_bb(transform=axis.transAxes)
		annotation.set_position((visualbb.width + 0.00625, 1), va=va, transform=axis.transAxes)
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
