"""
All visualizations must have, at least, a :class:`~drawable.Drawable`.
Any other functionality is up to the visualization type.
"""

class Visualization(object):
	"""
	All visualizations contain at least a :class:`~drawable.Drawable`.

	:ivar drawable: The :class:`~drawable.Drawable` where the visualization will be drawn.
	:vartype drawable: :class:`~drawable.Drawable`
	"""

	def __init__(self, drawable, *args, **kwargs):
		"""
		Create the visualization with a drawable.

		:param drawable: The :class:`~drawable.Drawable` where the visualization will be drawn.
		:type drawable: :class:`~drawable.Drawable`
		"""

		self.drawable = drawable
