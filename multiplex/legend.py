"""
A legend contains a list of labels and their visual representation.
"""

class Legend(object):
	"""
	The legend is made up of visual elements and a short label describing what they represent.

	:ivar components: The legend components, separated into lines.
				  Each component is a tuple of the visual representation and the associated label.
	:vartype components: list of list of tuple
	"""

	def __init__(self):
		"""
		Create the legend.
		"""

		self.components = [ ]

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
