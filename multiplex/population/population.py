"""
Multiplex's population chart is a brand new type of visualization that builds on matplotlib.
This visualization makes it easy to show how different populations, in a broad sense, vary from each other.
"""

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

    def draw(self, population, rows):
        """
        Draw a new population on this plot.

        :param population: The population to draw.
                           This can be simply the size of the population.
        :type population: int
        :param rows: The number of rows in which to split the population.
        :type rows: int

        :return: A list of drawn scatter points.
        :rtype: list of :class:`matplotlib.collections.PathCollection`

        :raise TypeError: If the population is not an integer.
        :raise TypeError: If the population is not a positive integer.
        :raise TypeError: If the number of rows is not an integer.
        :raise TypeError: If the number of rows is not a positive integer.
        """

        if population % 1:
            raise TypeError(f"The number of population must be an integer, received { population } ({ type(population).__name__ })")

        if population < 0:
            raise ValueError(f"The number of population must be zero or a positive integer, received { population }")

        if rows % 1:
            raise TypeError(f"The number of rows must be an integer, received { rows } ({ type(rows).__name__ })")

        if rows < 1:
            raise ValueError(f"The number of rows must be a positive integer, received { rows }")

        return [ ]

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
