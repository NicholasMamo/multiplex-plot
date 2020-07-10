"""
The basic :class:`~TimeSeries` class borrows heavily from `matplotlib's plot function <https://matplotlib.org/3.2.2/api/_as_gen/matplotlib.pyplot.plot.html>`_.
The only thing that it modifies is the way in which time series plots are labelled.

For example, Multiplex's :class:`~TimeSeries` visualizations do not have a legend by default.
Instead, to aid readability, the label is added to the end of the time series.
If you prefer the more traditional way, you can also create a normal legend.

Creating a time series is very easy.
All you have to do is create a :class:`~drawable.Drawable` class and call the :func:`~drawable.Drawable.draw_time_series` function.
You can keep calling the :func:`~drawable.Drawable.draw_time_series` function on the same :class:`~drawable.Drawable` instance to draw more time series.

Like `matplotlib's plot function <https://matplotlib.org/3.2.2/api/_as_gen/matplotlib.pyplot.plot.html>`_, it expects the x and y-coordinates of the time series:
However, you can also add your own styling:

.. code-block:: python

    import matplotlib.pyplot as plt
    from multiplex import drawable
    viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
    viz.draw_time_series(range(0, 10), range(0, 10),
                         color='#F6B913', linewidth=2,
                         label='A', label_style={ 'fontweight': '500' })
    viz.show()

Use the ``label`` keyword argument—and the related ``label_style``—to annotate the time series.
By default, the ``label`` goes at the end of a time series, but you can set ``with_legend=True`` to draw a :class:`~legend.Legend`.
"""

import os
import pandas
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
import util

from labelled import LabelledVisualization

class TimeSeries(LabelledVisualization):
	"""
	The :class:`~TimeSeries` class builds on the :class:`~labelled.LabelledVisualization`.
	The reason why the :class:`~TimeSeries` builds on that, and not the simpler :class:`~visualization.Visualization`, is that it supports drawing time series names at the end of the line.
	In these cases, the :class:`~labelled.LabelledVisualization` automatically ensures that the labels do not overlap.
	Like all visualizations, it revolves around the :func:`~TimeSeries.draw` function.

	Aside from that, the :class:`~TimeSeries` class borrows heavily from `matplotlib's plot function <https://matplotlib.org/3.2.2/api/_as_gen/matplotlib.pyplot.plot.html>`_.
	The new functionality is the ability to add labels at the end of the lines.
	Instead of labels, you can also label time series in the :class:`~legend.Legend`.
	"""

	def __init__(self, *args, **kwargs):
		"""
		Initialize the time series.
		"""

		super().__init__(*args, **kwargs)

	def draw(self, x, y, label=None, label_style=None, with_legend=False, *args, **kwargs):
		"""
		Draw a time series on the :class:`~drawable.Drawable`.
		The function expects, at the very least, the points on the time series: a list of x-coordinates and their corresponding y-coordinates.

		If a ``label`` is given, it is drawn at the end of the time series.
		You can use the ``label_style`` to style the label.
		If you prefer to add the label to the :class:`~legend.Legend`, set ``with_legend=True``.

		Any additional arguments and keyword arguments are used to style the line.
		The function accepts any arguments and keyword arguments accepted by the `matplotlib.pyplot.plot <https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.plot.html>`_ function.

		:param x: The list of x-coordinates to plot.
				  The x-coordinates must have the same number of points as the y-coordinates.
		:type x: list of float or :class:`pandas.core.series.Series`
		:param y: The list of corresponding y-coordinates to plot.
				  The y-coordinates must have the same number of points as the x-coordinates.
		:type y: list of float or :class:`pandas.core.series.Series`
		:param label: The plot's label.
					  If given, the label is drawn at the end of the line or in the legend, depending on the value of the ``with_legend`` parameter.
		:type label: str or None
		:param label_style: The style of the label.
							By default, the time series' ``color`` is used for the label's color, even if the ``color`` is not set in the ``kwargs``.
							The ``label_style`` accepts any styling option supported by the :class:`~text.annotation.Annotation`'s :func:`~text.annotation.Annotation.draw` function.
		:type label_style: dict or None
		:param with_legend: A boolean indicating whether the labels should be drawn as a legend.
							If it is set to ``False``, the labels are drawn at the end of the line.
							Otherwise, the label is added to the :class:`~legend.Legend`.
		:type with_legend: bool

		:return: A tuple made up of the drawn plot and label.
				 If the legend label is drawn, only a string is returned.
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
		Convert pandas series to a list.
		"""
		x = x.tolist() if type(x) is pandas.core.series.Series else x
		y = y.tolist() if type(y) is pandas.core.series.Series else y

		"""
		Plot the time series first.
		"""
		axes = self.drawable.axes
		line = axes.plot(x, y, *args, **kwargs)[0]

		"""
		Draw the label.
		If the label is drawn at the end of the line, by default it inherits the line's color.
		"""
		if label is not None and len(x) and len(y):
			default_label_style = { 'color': line.get_color() }
			default_label_style.update(kwargs)
			default_label_style.pop('linewidth', 0)
			if with_legend:
				self.drawable.legend.draw_line(label, label_style=label_style,
											   *args, **default_label_style)
			else:
				default_label_style.update(label_style or { })
				label = self.draw_label(label, x[-1], y[-1], **default_label_style)

		return (line, label)
