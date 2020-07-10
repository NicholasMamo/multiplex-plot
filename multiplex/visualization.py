"""
All visualizations must have, at least, a :class:`~drawable.Drawable`.
They must also implement the :class:`~visualization.Visualization.draw` function.
Any other functionality is up to the visualization type.

The goal of visualizations is not to run away with the data.
Their purpose is to structure the data and apply only the styling that is absolutely required.
They should allow the user to style all aspects of the visualization.

In short, visualization implementations are largely concerned with the structure, not the style.
"""

from abc import ABC, abstractmethod

class Visualization(ABC):
	"""
	All visualizations contain at least a :class:`~drawable.Drawable`.
	Furthermore, all classes that inherit the :class:`~visualization.Visualization` class also need to implement functionality to draw a visualization.
	This is implemented in the :func:`~visualization.Visualization.draw` function.

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

	@abstractmethod
	def draw(self, *args, **kwargs):
		"""
		The draw method is the central method, used to create the visualization on this class' :class:`~drawable.Drawable` instance.
		The purpose of this function is two-fold:

			- Structure the data and apply the bare minimum styling to the visualization, and
			- Allow the user to style the created visualization's components.

		Therefore the drawing function should mainly be concerned with the layout.

		At the end, the function should return the drawn component.
		If the function draws multiple components, it can return them as a tuple.
		"""

		pass
