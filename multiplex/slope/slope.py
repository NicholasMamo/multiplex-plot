"""
The :class:`~Slope` class allows you to create slope graphs that show how values changed, such as:

- Before and after an operation, or
- Over a time period.

Slope graphs are not commonly included in visualization packages, but they can be great tools to tell a story.

.. image:: ../examples/exports/6-slope.png
   :class: example inline

To draw a slope graph, create a :class:`~drawable.Drawable` class and call the :func:`~drawable.Drawable.draw_slope` function:

.. code-block:: python

    import matplotlib.pyplot as plt
    from multiplex import drawable
    viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
    viz.draw_slope(5, 5)
    viz.show()

You can also draw multiple slopes at the same time by providing a list instead:

.. code-block:: python

    viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
    viz.draw_slope([ 0, 3 ], [ 5, 2 ])

In addition to the slopes, you can also provide the ticks on both sides.
Ticks can be:

- ``None`` (default): Adds the values as ticks,
- Empty string: Add no ticks, or
- Other (such as a string): Add the given value as a label.

For example, the following snippet adds a tick with label '0' on the left y-axis, and a tick with label '3' on the right y-axis.

.. code-block:: python

    viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
    viz.draw_slope(0, 3, y1_tick=None, y2_tick=None)

Multiplex overwrites ticks if you provide ``None`` or a value for the tick labels, but not if you provide an empty string.
If you are creating multiple slopes at the same time, ``None`` and the empty string apply for all slopes.
You can, however, provide a list of ticks labels corresponding to each slope.
For example, the next snippet adds 'A' and 'B' on the left y-axis, and '3' and '5' as ticks on the right y-axis.

.. code-block:: python

    viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
    viz.draw_slope([ 0, 1 ], [ 3, 5 ], y1_tick=[ 'A', 'B' ], y2_tick=None)
"""

from collections.abc import Iterable
from numbers import Number
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

    :ivar slopes: The drawn slopes.
    :vartype slopes: list of :class:`matplotlib.lines.Line2D`
    :ivar llabels: The slope labels on the left.
    :vartype llabels: list of :class:`~text.annotation.Annotation`
    :ivar rlabels: The slope labels on the right.
    :vartype rlabels: list of :class:`~text.annotation.Annotation`
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the slope graph with a drawable.
        This function also creates a container for all the drawn slopes.
        """

        super().__init__(*args, **kwargs)
        self.slopes = [ ]
        self.llabels, self.rlabels = [ ], [ ]

    def draw(self, y1, y2, y1_tick=None, y2_tick=None,
             label=None, where='both', label_style=None,
             style_plot=True, *args, **kwargs):
        """
        Draw a slope graph.
        The function returns a two-tuple with the drawn plot (a line with optional markers) and any drawn labels.

        Any additional arguments and keyword arguments are used as styling options.
        The accepted styling options are those supported by the `matplotlib.pyplot.plot <https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.plot.html>`_ method.

        :param y1: The start value of the slope, or a list of start values.
        :type y1: float or list of float
        :param y2: The end value of the slope, or a list of end values.
        :type y2: float or list of float
        :param y1_tick: The tick label to show on the left side, which can be:

                         - ``None`` (default): Adds the values as ticks,
                         - Empty string: Add no ticks, or
                         - Other (such as a string): Add the given value as a label.

                         If you are drawing a list of slopes, you can provide a list.
                         This list too can be made up of ``None``, empty strings or any other value with the same behavior as above.
        :type y1_tick: None or str or list
        :param y2_tick: The tick label to show on the right side, which can be:

                         - ``None`` (default): Adds the values as ticks,
                         - Empty string: Add no ticks, or
                         - Other (such as a string): Add the given value as a label.

                         If you are drawing a list of slopes, you can provide a list.
                         This list too can be made up of ``None``, empty strings or any other value with the same behavior as above.
        :type y2_tick: None or str or list
        :param label: The slope's label.
                      The label is different from the ticks: ticks show values, labels show the name of the slope.
                      If ``None`` or an empty string is given, no labels added.
                      If you provide a list of slopes, you can also provide a list of labels: one for each slope.
        :type label: None or str or list
        :param label_style: The style of the labels.
                            The ``label_style`` accepts any styling option supported by the :class:`~text.annotation.Annotation`'s :func:`~text.annotation.Annotation.draw` function.
        :type label_style: dict or None
        :param where: The position of the labels: ``left``, ``right`` or ``both``.
                      If ``left`` is given, the labels are added to the primary (left) axes.
                      If ``right`` is given, the labels are added to the secondary (right) axes.
                      If ``both`` is given, the labels are added to both axes.

                      If multiple labels are given, one ``where`` can be provided for each label as a list.
        :type where: str or list of str
        :param style_plot: A boolean indicating whether the plot should be re-styled.
                           If it is set to ``True``, the visualization:

                           - Removes the grid,
                           - Hides the x-axis
                           - Hides the y-axis, and
                           - Adds two x-ticks.
        :type style_plot: bool

        :return: A tuple containing the drawn plot, any drawn labels on the left, and any drawn labels on the right.
        :rtype: tuple (:class:`matplotlib.lines.Line2D`, list of :class:`~text.annotation.Annotation`, list of :class:`~text.annotation.Annotation`)

        :raises ValueError: If the ``y1`` and ``y2`` parameters are lists of unequal length.
        :raises ValueError: If the number of start points and start tick labels are not equal.
        :raises ValueError: If the number of end points and end tick labels are not equal.
        :raises ValueError: If the number of slopes and labels are not equal.
        :raises ValueError: If the label position is unknown (not ``left`` or ``right``, ``both``).
        """

        y1 = [ y1 ] if isinstance(y1, Number) else y1
        y2 = [ y2 ] if isinstance(y2, Number) else y2
        label_style = label_style or { }

        """
        Re-style the plot if need be.
        """
        if style_plot:
            self._style()

        # draw the slopes
        slopes = self._draw(y1, y2, *args, **kwargs)
        self.slopes.extend(slopes)

        # draw the ticks
        self._add_ticks(y1, y1_tick, where='left')
        self._add_ticks(y2, y2_tick, where='right')

        # draw the labels and re-fit the axes
        left, right = self._add_labels(y1, y2, label, where=where, **label_style)
        self.llabels.extend(left)
        self.rlabels.extend(right)
        self._fit_axes()

        return (slopes, left, right)

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
        :type y1: list of float
        :param y2: The end value of the slope.
        :type y2: list of float

        :return: The drawn slopes.
        :rtype: list of :class:`matplotlib.lines.Line2D`

        :raises ValueError: If the ``y1`` and ``y2`` parameters are lists of unequal length.
        """

        if len(y1) != len(y2):
            raise ValueError(f"The list of points should be equal; received { len(y1) } start and { len(y2) } end values")

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

                       - ``None`` (default): Adds the values as ticks,
                       - Empty string: Add no ticks, or
                       - Other (such as a string): Add the given value as a label.

                       If you are drawing a list of slopes, you can provide a list.
                       This list too can be made up of ``None``, empty strings or any other value with the same behavior as above.
        :type labels: None or str or list
        :param where: The position of the ticks: ``left`` or ``right``.
                      If ``left`` is given, the ticks are added to the primary (left) axes.
                      If ``right`` is given, the ticks are added to the secondary (right) axes.
        :type where: str

        :raises ValueError: If the tick position is unknown (not ``left`` or ``right``).
        :raises ValueError: If the number of ticks and labels are not equal.
        """

        where = where.lower()
        if where not in [ 'left', 'right' ]:
            raise ValueError(f"Unknown tick position { where }; expected 'left' or 'right'")
        axes = self.drawable.axes if where == 'left' else self.drawable.secondary

        """
        If the labels are ``None``, the ticks are used as labels.
        If an empty string is given as labels, no ticks are added.
        """
        if labels is None:
            labels = ticks
        elif isinstance(labels, str) and labels == '':
            return

        labels = [ labels ] if (not isinstance(labels, Iterable) or isinstance(labels, str)) else labels # convert the labels to a list if they are not a list
        if len(ticks) != len(labels):
            raise ValueError(f"The list of ticks and labels should be equal; received { len(ticks) } ticks and { len(labels) } labels")

        # get the new list of ticks
        ticks = { tick: label for tick, label in zip(ticks, labels)
                              if label != '' }
        _ticks = dict(zip(axes.get_yticks(), axes.get_yticklabels())) # the current ticks
        _ticks.update(ticks) # add the new ticks, overwriting old ones in case of overlaps
        _ticks = { tick: (label if label is not None else tick) for tick, label in _ticks.items() } # replace ``None`` with the tick

        # draw the new ticks
        _ticks = sorted(_ticks.items(), key=lambda _tick: _tick[0])
        ticks = [ tick for tick, label in _ticks ]
        labels = [ label for tick, label in _ticks ]
        axes.set_yticks(ticks)
        axes.set_yticklabels(labels)

    def _add_labels(self, y1, y2, labels, where='both', va='center', *args, **kwargs):
        """
        Add labels to the slopes.
        Labels are added on the outer part of the plot, so left of the left axis and right of the right axis.

        Unlike ticks, there is no option for the labels on the left to be different from the labels on the right.
        This is simply because it doesn't make sense for one slope to have different labels, or names.

        Any additional arguments or keyword arguments are used to style the labels.

        :param y1: The start position of the slopes on the left.
        :type y1: list of float
        :param y2: The end position of the slopes on the right.
        :type y2: list of float
        :param labels: The slopes' labels.
                       If ``None`` or an empty string is given, no labels added.
                       If you provide a list of slopes, you can also provide a list of labels: one for each slope.
        :type labels: None or str or list
        :param where: The position of the labels: ``left``, ``right`` or ``both``.
                      If ``left`` is given, the labels are added to the primary (left) axes.
                      If ``right`` is given, the labels are added to the secondary (right) axes.
                      If ``both`` is given, the labels are added to both axes.

                      If multiple labels are given, one ``where`` can be provided for each label as a list.
        :type where: str or list of str
        :param va: The slope label's vertical alignment, defaults to the center.
        :type va: str

        :return: A tuple of labels drawn on the left and on the right.
        :rtype: tuple of list of :class:`~text.annotation.Annotation`

        :raises ValueError: If the number of slopes and labels are not equal.
        :raises ValueError: If the label position is unknown (not ``left`` or ``right``, ``both``).
        """

        left, right = [ ], [ ]

        # if the labels are ``None`` or an empty string is given, no labels are added
        if labels is None or (isinstance(labels, str) and labels == ''):
            return (left, right)

        # convert the labels to a list if they are not a list
        labels = [ labels ] if (not isinstance(labels, Iterable) or isinstance(labels, str)) else labels
        if len(y1) != len(labels):
            raise ValueError(f"The list of slopes and labels should be equal; received { len(y1) } ticks and { len(labels) } labels")

        if isinstance(where, str):
            where = [ where.lower() ] * len(labels)

        # validate the label locations
        for pos in where:
            if pos.lower() not in [ 'left', 'right', 'both' ]:
                raise ValueError(f"Unknown label position { pos }; expected 'left', 'right' or 'both'")

        align = kwargs.pop('align', None)
        # draw the labels on the left
        for y, label, pos in zip(y1, labels, where):
            if not label or pos not in [ 'left', 'both' ]:
                continue

            left.append(self.draw_label(label, (-2, -1), y,
                                         align=(align or 'right'), va=va,
                                         *args, **kwargs))

        # draw the labels on the right
        for y, label, pos in zip(y2, labels, where):
            if not label or pos not in [ 'right', 'both' ]:
                continue

            right.append(self.draw_label(label, (2, 3), y,
                                         align=(align or 'left'), va=va,
                                         *args, **kwargs))

        return (left, right)

    def _fit_axes(self):
        """
        Make space for the x-axes.
        This function reduces the actual plot size so that the axes tick labels fit neatly.

        After it does that, it re-positions all of the labels on the left and right so they do not overlap with the axes.
        Here again, the axes are widened to fit the labels.
        """

        figure, axes, secondary = self.drawable.figure, self.drawable.axes, self.drawable.secondary

        if not self.llabels and not self.rlabels:
            super()._fit_axes()
            return

        _xlim = None
        while _xlim is None or abs(_xlim[0] - axes.get_xlim()[0]) > 1e-10: # repeat until convergence
            _xlim = axes.get_xlim()

            # draw the labels to get an idea of their widths
            for label in self.llabels + self.rlabels:
                label.redraw()
            lwidth = min(1, max( label.get_virtual_bb().width for label in self.llabels ) if self.llabels else 0 )
            rwidth = min(1, max( label.get_virtual_bb().width for label in self.rlabels ) if self.rlabels else 0 )
            lpad = 0.1 if self.llabels else 0
            rpad = 0.1 if self.rlabels else 0

            # find the new x-limit
            xlim = axes.get_xlim()
            x0 = min( util.get_bb(figure, axes, tick).x0 for tick in axes.get_yticklabels() ) if axes.get_yticklabels() else -0.1
            x1 = max( util.get_bb(figure, axes, tick).x1 for tick in secondary.get_yticklabels() ) if secondary.get_yticklabels() else 1.1
            axes.set_xlim(( x0 - lwidth - lpad, x1 + rwidth + rpad ))

            # move the left labels
            for label in self.llabels:
                label.x = ( x0 - 1 - lpad, x0 - lpad )

            # move the right labels
            for label in self.rlabels:
                label.x = ( x1 + rpad, x1 + 1 + rpad )
