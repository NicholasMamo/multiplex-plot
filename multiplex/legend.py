"""
A legend contains a list of labels and their visual representation.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from text.annotation import Annotation

class Legend(object):
	"""
	The legend is made up of visual elements and a short label describing what they represent.

	:ivar drawable: The :class:`~drawable.Drawable` where the legend will be drawn.
	:vartype drawable: :class:`~drawable.Drawable`
	:ivar components: The legend components, separated into lines.
				  Each component is a tuple of the visual representation and the associated label.
	:vartype components: list of list of tuple
	"""

	def __init__(self, drawable):
		"""
		Create the legend.

		:param drawable: The :class:`~drawable.Drawable` where the legend will be drawn.
		:type drawable: :class:`~drawable.Drawable`
		"""

		self.components = [ ]
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

		pass
