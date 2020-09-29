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

    def draw(self, y1, y2, y1_ticks=None, y2_ticks=None, style_plot=True, *args, **kwargs):
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
        :param y1_ticks: The tick labels to show on the left side, which can be:

                         - ``None`` (default): The values are used as ticks,
                         - Empty string: No ticks are added, or
                         - A string, or a list of strings: Ticks corresponding to each ``y1`` value.
        :type y1_ticks: None or str or list of str
        :param y2_ticks: The tick labels to show on the right side, which can be:

                         - ``None`` (default): The values are used as ticks,
                         - Empty string: No ticks are added, or
                         - A string, or a list of strings: Ticks corresponding to each ``y1`` value.
        :type y2_ticks: None or str or list of str

        :return: A tuple made up of the drawn plot and any drawn labels.
                 If the legend label is drawn, only a string is returned.
        :rtype: tuple

        :raises ValueError: When the ``y1`` and ``y2`` parameters are lists of unequal length.
        :raises ValueError: If the number of start points and start labels are not equal.
        :raises ValueError: If the number of end points and end labels are not equal.
        """

        y1 = [ y1 ] if type(y1) in [ float, int ] else y1 # TODO: Add support for other numbers
        y2 = [ y2 ] if type(y2) in [ float, int ] else y2 # TODO: Add support for other numbers
        if len(y1) != len(y2):
            raise ValueError(f"The list of points should be equal; received { len(y1) } start and { len(y2) } end values")

        """
        Re-style the plot if need be.
        """
        if style_plot:
            self._style()

        slopes = self._draw(y1, y2, *args, **kwargs)
        self._add_ticks(y1, y1_ticks, where='left')
        self._add_ticks(y2, y2_ticks, where='right')

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
        self._update_ylim()
        return slopes

    def _update_ylim(self):
        """
        Align the y-limits of the primary and secondary axes so that they are the same.
        This is important so that the y-ticks are aligned properly.
        """

        ylim = (min(self.drawable.axes.get_ylim()[0], self.drawable.secondary.get_ylim()[0]),
                max(self.drawable.axes.get_ylim()[1], self.drawable.secondary.get_ylim()[1]))
        self.drawable.axes.set_ylim(ylim)
        self.drawable.secondary.set_ylim(ylim)

    def _add_ticks(self, ticks, labels, where):
        """
        Add ticks to the axes.

        :param ticks: The position of the ticks.
        :type ticks: list of float
        :param labels: The ticks to add, which can be:

                       - ``None`` (default): The values are used as ticks,
                       - Empty string: No ticks are added, or
                       - A string, or a list of strings: Ticks corresponding to each ``y1`` value.
        :type labels: None or str or list of str
        :param where: The position of the ticks: ``left`` or ``right``.
                      If ``left`` is given, the ticks are added to the primary (left) axes.
                      If ``right`` is given, the ticks are added to the secondary (right) axes.
        :type where: str

        :raises ValueError: If the tick position is unknown (not ``left`` or ``right``).
        :raises ValueError: If the number of ticks and labels are not equal.
        """

        where = where.lower()
        if where not in [ 'left', 'right' ]:
            raise ValueError(f"Unknown tick position { where }; expected 'left' or 'right '")
        axes = self.drawable.axes if where == 'left' else self.drawable.secondary

        """
        If the labels are ``None``, the ticks are used as labels.
        If an empty string is given as labels, no ticks are added.
        """
        if labels is None:
            labels = ticks
        elif labels == '':
            return

        labels = [ labels ] if type(labels) not in [ list, range ] else labels # convert the labels to a list if they are not a list
        if len(ticks) != len(labels):
            raise ValueError(f"The list of ticks and labels should be equal; received { len(ticks) } ticks and { len(labels) } labels")

        """
        Get the new list of ticks.
        """
        _ticks = dict(zip(axes.get_yticks(), axes.get_yticklabels())) # the current ticks
        _ticks.update(dict(zip(ticks, labels))) # add the new ticks, overwriting old ones in case of overlaps
        _ticks = { tick: (label if label is not None else tick) for tick, label in _ticks.items() } # replace `None` with the tick

        """
        Draw the new ticks.
        """
        _ticks = sorted(_ticks.items(), key=lambda _tick: _tick[0])
        ticks = [ tick for tick, label in _ticks ]
        labels = [ label for tick, label in _ticks ]
        axes.set_yticks(ticks)
        axes.set_yticklabels(labels)
