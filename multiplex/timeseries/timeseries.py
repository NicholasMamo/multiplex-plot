"""
The :class:`~TimeSeries` class borrows heavily from matplotlib's `plot` function.
This class builds on matplotlib's plotting and introduces more functionality.

.. image:: ../examples/exports/3-time-series.png
   :class: example

For example, Multiplex time series do not have a legend by default.
Instead, to aid readability, the line's label is added to the end of the plot.
Creating a time series is very easy:

.. code-block:: python

    import matplotlib.pyplot as plt
    from multiplex import drawable
    viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
    viz.draw_time_series(range(0, 10), range(0, 10),
                         color='#F6B913', linewidth=2,
                         label='A', label_style={ 'fontweight': '500' })

You can keep calling the :meth:`~drawable.Drawable.draw_time_series` function on the same :class:`~drawable.Drawable` instance to draw on the same plot.

To start creating time series visualizations, create a :class:`~TimeSeries` instance and call the :meth:`~TimeSeries.draw` method.
If you are using the :class:`~drawable.Drawable` class, just call the :meth:`~drawable.Drawable.draw_time_series` method on a :class:`~drawable.Drawable` instance instead.
"""

import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
import util

from labelled import LabelledVisualization

class TimeSeries(LabelledVisualization):
	"""
	The :class:`~TimeSeries` class borrows heavily on matplotlib's `plot` function.
	This class builds on matplotlib's plotting and introduces more functionality.

	For example, Multiplex's time series have no legend.
	Instead, it adds a label at the end of the time series for readability.
	Multiplex also makes it easy to annotate points on the time series with descriptions to explain their significance.
	"""

	def __init__(self, *args, **kwargs):
		"""
		Initialize the time series.
		"""

		super().__init__(*args, **kwargs)

	def draw(self, x, y, label=None, label_style=None, with_legend=False, *args, **kwargs):
		"""
		Draw a time series on the :class:`~drawable.Drawable`.
		The arguments and keyword arguments are passed on to the :meth:`~matplotlib.pyplot.plot` method.
		Thus, all of the arguments and keyword arguments accepted by it are also accepted by this function.

		:param x: The list of x-coordinates to plot.
				  The x-coordinates must have the same number of points as the y-coordinates.
		:type x: list of float
		:param y: The list of corresponding y-coordinates to plot.
				  The y-coordinates must have the same number of points as the x-coordinates.
		:type y: list of float
		:param label: The plot's label.
					  If given, the label is drawn at the end of the line.
		:type label: str or None
		:param label_style: The style of the label.
		:type label_style: dict or None
		:param with_legend: A boolean indicating whether the labels should be drawn as a legend.
							If false, the labels are drawn at the end of the line.
		:type with_legend: bool

		:return: A tuple made up of the drawn plot and label.
		:rtype: tuple

		:raises ValueError: When the number of x-coordinates and y-coordinates are not equal.
		:raises ValueError: When no x-coordinates or no y-coordinates are given.
		"""

		"""
		Validate the arguments.
		A non-zero number of points need to be provided.
		The number of x-coordinates and y-coordinates need to be equal.
		"""
		if len(x) != len(y):
			raise ValueError("The number of x-coordinates and y-coordinates must be equal; received %d x-coordinates and %d y-coordinates" % (len(x), len(y)))

		if not len(x) or not len(y):
			raise ValueError("The time series needs a positive number of points")

		"""
		Plot the time series first.
		"""
		axis = self.drawable.axis
		line = axis.plot(x, y, *args, **kwargs)

		# TODO: Add support for pandas Series

		"""
		Draw the label at the end of the line.
		"""
		if label is not None and len(x) and len(y):
			if with_legend:
				self.drawable.legend.draw_line(label, *args, **kwargs)
			else:
				default_label_style = { 'color': line[0].get_color() }
				default_label_style.update(label_style or { })
				self.draw_label(label, x[-1], y[-1], **default_label_style)

		return (line, label)
