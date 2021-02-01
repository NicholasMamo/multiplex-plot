"""
Multiplex's population chart is a brand new type of visualization that builds on matplotlib.
This visualization makes it easy to show how different populations, in a broad sense, vary from each other.
"""

from collections.abc import Iterable
import math
from numbers import Number
import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
import util

from visualization import Visualization

class Population(Visualization):
    """
    The :class:`~Population` class plots scatter points that represent populations.
    Like all visualizations, it stores a :class:`~drawable.Drawable` instance and revolves around the :func:`~Population.draw` function.

    To draw a population chart, create a :class:`~drawable.Drawable` class and call the :func:`~drawable.Drawable.draw_population` function.
    This method expects, at the very least, the values and the name of the 100% bar:

    .. code-block:: python

        import matplotlib.pyplot as plt
        from multiplex import drawable
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.draw_population(25, 10)
        viz.show()
    """

    def draw(self, population, rows, style_plot=True, height=0.6, *args, **kwargs):
        """
        Draw a new population on this plot.

        You can pass additional styling options as ``args`` or ``kwargs``.
        The accepted styling options are those supported by the `matplotlib.pyplot.barh <https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.scatter.html>`_ method.

        :param population: The population to draw.
                           This can be simply the size of the population or a list of values.
        :type population: int or list
        :param rows: The number of rows in which to split the population.
        :type rows: int
        :param style_plot: A boolean indicating whether the plot should be re-styled.
                           If it is set to ``True``, the visualization:

                               - Removing the y-axis,
                               - Inverting the y-axis, and
                               - Removing the grid.
        :type style_plot: bool
        :param height: The height of the population, between 0 (exclusive) and 1.
        :type height: float

        :return: A list of drawn scatter points, separated by column.
        :rtype: list of list of :class:`matplotlib.collections.PathCollection`

        :raise TypeError: If the population is not an integer.
        :raise TypeError: If the population is not a positive integer.
        :raise TypeError: If the number of rows is not an integer.
        :raise TypeError: If the number of rows is not a positive integer.
        :raise ValueError: If the height is not between 0 and 1.
        """

        # draw the population
        population = self._draw_population(population, rows, height, *args, **kwargs)

        # re-style the plot if need be, leaving it until last since the population changes the y-axis
        if style_plot:
            self._style()

        return population

    def _style(self):
        """
        Style the plot by:

        - Removing the y-axis,
        - Inverting the y-axis, and
        - Removing the grid.
        """

        self.drawable.axes.spines['left'].set_visible(False)
        self.drawable.invert_yaxis()
        self.drawable.grid(False)

    def _draw_population(self, population, rows, height, *args, **kwargs):
        """
        Draw a new population on this plot.

        :param population: The population to draw.
                           This can be simply the size of the population or a list of values.
        :type population: int or list
        :param rows: The number of rows in which to split the population.
        :type rows: int

        :return: A list of drawn scatter points, separated by column.
        :rtype: list of list of :class:`matplotlib.collections.PathCollection`

        :raise TypeError: If the population is not an integer.
        :raise TypeError: If the population is not a positive integer.
        :raise TypeError: If the number of rows is not an integer.
        :raise TypeError: If the number of rows is not a positive integer.
        :raise ValueError: If the height is not between 0 and 1.
        """

        drawn = [ ]

        if isinstance(population, Number) and population % 1:
            raise TypeError(f"The number of population items must be an integer, received { population } ({ type(population).__name__ })")

        if isinstance(population, Number) and population < 0:
            raise ValueError(f"The number of population items must be zero or a positive integer, received { population }")

        if rows % 1:
            raise TypeError(f"The number of rows must be an integer, received { rows } ({ type(rows).__name__ })")

        if rows < 1:
            raise ValueError(f"The number of rows must be a positive integer, received { rows }")

        # calculate the gap size
        lim = self._limit(height)
        gap = self._gap_size(lim, rows)
        self.drawable.set_ylim(-0.1, 1.1)

        # convert the items into a list, whatever their type
        items = list(population) if isinstance(population, Iterable) else [ True for _ in range(population) ]
        columns = math.ceil(len(items)/rows)

        # draw the population
        for x in range(0, columns):
            _drawn = [ ]
            for y in range(0, rows):
                # stop drawing if all points have been drawn
                if x * rows + y >= len(items):
                    break

                point = self.drawable.scatter(1 + x, lim[0] + y * gap, *args, **kwargs)
                _drawn.append(point)

            drawn.append(_drawn)

        return drawn

    def _limit(self, height):
        """
        Calculate the limit of the population based on the give height.

        :raise ValueError: If the height is not between 0 and 1.
        """

        if not 0 < height <= 1:
            raise ValueError(f"The height of the population must be greater than 0, and less than or equal to 1, received { height }")

        return (0.5 - height / 2, 0.5 + height / 2)

    def _gap_size(self, lim, rows):
        """
        Calculate the gap size such that the given number of rows fit between the given limit.

        :param lim: The y-limit of the entire population.
        :type lim: tuple of float
        :param rows: The number of rows to fit in the limit.
        :type rows: int

        :return: The gap between each row such that the population fits perfectly between the limit.

        :raise TypeError: If the number of rows is not an integer.
        :raise TypeError: If the number of rows is not a positive integer.
        """

        if rows % 1:
            raise TypeError(f"The number of rows must be an integer, received { rows } ({ type(rows).__name__ })")

        if rows < 1:
            raise ValueError(f"The number of rows must be a positive integer, received { rows }")

        if rows == 1:
            return 0

        return (lim[1] - lim[0])/(rows - 1)
