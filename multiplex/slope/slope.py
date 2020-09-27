"""
The :class:`~Slope` class allows you to create slope graphs that show how values changed, such as:

- Before and after an operation, or
- Over a time period.

Slope graphs are not commonly included in visualization packages, but they can be great tools to tell a story.

To draw a slope graph, create a :class:`~drawable.Drawable` class and call the :func:`~drawable.Drawable.draw_slope` function:

.. code-block:: python

    import matplotlib.pyplot as plt
    from multiplex import drawable
    viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
    viz.draw_slope(5, 5)
    viz.show()

You can also draw multiple slopes at the same time by providing a list instead:

.. code-block:: python

    import matplotlib.pyplot as plt
    from multiplex import drawable
    viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
    viz.draw_slope([ 0, 3 ], [ 5, 2 ])
    viz.show()
"""

import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
import util

from labelled import LabelledVisualization

class Slope(LabelledVisualization):
    """
    The :class:`~Slope` class builds on the :class:`~labelled.LabelledVisualization`.
    The reason behind this is that each slope in the visualization has a label associated with it.
    In these cases, the :class:`~labelled.LabelledVisualization` automatically ensures that the labels do not overlap.

    Like all visualizations, it revolves around the :func:`~Slope.draw` function.
    """

    def draw(self, y1, y2, style_plot=True, *args, **kwargs):
        """
        Draw a slope graph.
        The function returns a two-tuple with the drawn plot (a line with optional markers) and any drawn labels.

        Any additional arguments and keyword arguments are used as styling options.
        The accepted styling options are those supported by the `matplotlib.pyplot.plot <https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.plot.html>`_ method.

        :param y1: The start value of the slope, or a list of start values.
        :type y1: float or list of float
        :param y2: The end value of the slope, or a list of end values.
        :type y2: float or list of float
        :param style_plot: A boolean indicating whether the plot should be re-styled.
                           If it is set to ``True``, the visualization:

                           - Removes the grid,
                           - Hides the x-axis
                           - Hides the y-axis, and
                           - Adds two x-ticks.
        :type style_plot: bool

        :return: A tuple made up of the drawn plot and any drawn labels.
                 If the legend label is drawn, only a string is returned.
        :rtype: tuple

        :raises ValueError: When the ``y1`` and ``y2`` parameters are lists of unequal length.
        """

        y1 = [ y1 ] if type(y1) in [ float, int ] else y1
        y2 = [ y2 ] if type(y2) in [ float, int ] else y2
        if len(y1) != len(y2):
            raise ValueError(f"The list of points should be equal; received { len(y1) } start and { len(y2) } end values")

        """
        Re-style the plot if need be.
        """
        if style_plot:
            self._style()

        slopes = self._draw(y1, y2, *args, **kwargs)

        return (slopes, None)

    def _style(self):
        """
        Style the plot by:

        - Removes the grid,
        - Hides the x-axis
        - Hides the y-axis, and
        - Adds two x-ticks.
        """

        if self.drawable.secondary != self.drawable.axes:
            return

        self.drawable.secondary = self.drawable.axes.twinx()

        self.drawable.set_xlim((-0.1, 1.1))
        self.drawable.set_xticks(range(0, 2))
        self.drawable.axes.xaxis.set_label_position('bottom')
        self.drawable.axes.xaxis.tick_bottom()
        for axes in (self.drawable.axes, self.drawable.secondary):
            axes.grid(False)
            axes.set_yticks([ ])
            axes.spines['top'].set_visible(False)
            axes.spines['right'].set_visible(False)
            axes.spines['right'].set_position(('data', 1.1))
            axes.spines['bottom'].set_visible(True)
            axes.spines['bottom'].set_bounds(0, 1)
            axes.spines['left'].set_visible(False)
            axes.spines['left'].set_position(('data', -0.1))

    def _draw(self, y1, y2, *args, **kwargs):
        """
        Draw a slope starting from ``y1`` to ``y2``.

        Any additional arguments and keyword arguments are used as styling options.
        The accepted styling options are those supported by the `matplotlib.pyplot.plot <https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.plot.html>`_ method.

        :param y1: The starting value of the slope.
        :type y1: float
        :param y2: The end value of the slope.
        :type y2: float

        :return: The drawn slopes.
        :rtype: list of :class:`matplotlib.lines.Line2D`
        """

        slopes = self.drawable.plot([0, 1], [y1, y2], *args, **kwargs)

        return slopes
