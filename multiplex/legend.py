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

	def draw(self, label, func, *args, **kwargs):
		"""
		Draw a legend for the given label.
		Any additional arguments and keyword arguments are provided to the specified plotting function.

		:param label: The text of the legend label.
		:type label: str
		:param func: The type of plotting function to call.
					 The arguments and keyword arguments are passed on to this function.
		:type func: func

		:return: A tuple made up of the function return value and the drawn label.
		:rtype: tuple
		"""

		pass
