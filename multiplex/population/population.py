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
        viz.draw_population()
        viz.show()
    """

    def draw(self):
        """
        Draw a new population on this plot.

        :return: A list of drawn scatter points.
        :rtype: list of :class:`matplotlib.collections.PathCollection`
        """

        return [ ]
