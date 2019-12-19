"""
A class that wraps a figure and provides more functionality to work with visualizations.
All functionality goes through this class.
"""

import matplotlib.pyplot as plt

class Drawable():
	"""
	The :class:`Drawable` class wraps a matplotlib figure and axis to provide additional functionality.
	If no axis is given, the default plot axis (:code:`plt.gca()`) is used.
	The :class:`Drawable` class can be used as a normal :class:`matplotlib.axis.Axis` object with additional functionality.
	The axis functionality can be called on the :class:`Drawable` class.
	The :class:`Drawable` instance re-routes method and attribute calls to the :class:`matplotlib.axis.Axis` instance.

	To create a :class:`Drawable` instance from a normal plot:

	.. code-block:: python

	  viz = drawable.Drawable(plt.figure(figsize=(10, 5)))

	To create a :class:`Drawable` instance from an axis, or a subplot:

	.. code-block:: python

	  figure, axis = plt.subplots(2, 1, figsize=(10, 10))
	  viz = drawable.Drawable(figure, axis[0])

	:ivar figure: The figure that the :class:`Drawable` class wraps.
	:vartype figure: :class:`matplotlib.figure.Figure`
	:ivar axis: The axis where the drawable will draw.
	:vartype axis: :class:`matplotlib.axis.Axis`
	"""

	def __init__(self, figure, axis=None):
		"""
		Create the drawable with the figure.

		:param figure: The figure that the :class:`Drawable` class wraps.
					   This is mainly used to get the figure renderer.
		:type figure: :class:`matplotlib.figure.Figure`
		:param axis: The axis (or subplot) where to plot visualizations.
					 If `None` is not given, the plot's main subplot is used instead.
		:type axis: `None` or :class:`matplotlib.axis.Axis`
		"""

		self.figure = figure
		self.axis = plt.gca() if axis is None else axis

	def __getattr__(self, name):
		"""
		Get an attribute indicated by `name` from the class.
		If it gets to this point, then the attribute does not exist.
		Instead, it is retrieved from the :class:`Drawable` axis.

		:param name: The name of the attribute.
		:type name: str
		"""

		def method(*args, **kwargs):
			"""
			Try to get the attribute from the axis.
			If arguments were given, then the attribute is treated as a method call.
			Otherwise, it is treated as a normal attribute call.
			"""

			if len(args) or len(kwargs):
				getattr(self.axis, name)(*args, **kwargs)
			else:
				getattr(self.axis, name)

		return method
