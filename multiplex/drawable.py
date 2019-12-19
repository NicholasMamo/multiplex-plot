"""
A class that wraps a figure and provides more functionality to work with visualizations.
"""

import matplotlib.pyplot as plt

class Drawable():
	"""
	The :class:`Drawable` class wraps a matplotlib figure and axis to provide additional functionality.

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
