"""
A legend contains a list of labels and their visual representation.
"""

import os
import sys

from matplotlib import lines

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

		line = lines.Line2D([ 0, 0.025 ], [ 1 ] * 2,
							transform=axis.transAxes, *args, **kwargs)
		line.set_clip_on(False)
		axis.add_line(line)

		label_style = label_style or { }
		line_offset = util.get_bb(figure, axis, line, transform=axis.transAxes).x1
		annotation = self.draw_annotation(label, line_offset, 1, **label_style)

		self.lines[-1].append((line, annotation))
		return (line, annotation)

	def draw_annotation(self, label, x, y, va='center', *args, **kwargs):
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

	def _get_offset(self):
		"""
		Get the x-coordinate offset for the next legend.

		:return: The x-coordinate offset for the next legend.
		:rtype: float
		"""

		if self.lines:
			last = self.lines[-1]
			if last:
				(visual, annotation) = last[-1]
				return annotation.get_virtual_bb().x1

		return 0
