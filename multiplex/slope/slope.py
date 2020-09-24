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
    viz.draw_slope()
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

    def draw(self, style_plot=True, *args, **kargs):
        """
        Draw a slope graph.
        The function returns a two-tuple with the drawn plot (a line with optional markers) and any drawn labels.

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
        """

        """
        Re-style the plot if need be.
        """
        if style_plot:
            self._style()

        return (None, None)

    def _style(self):
        """
        Style the plot by:

        - Removes the grid,
        - Hides the x-axis
        - Hides the y-axis, and
        - Adds two x-ticks.
        """

        axes = self.drawable.axes
        
        self.drawable.grid(False)
        axes.spines['top'].set_visible(False)
        axes.spines['right'].set_visible(False)
        axes.spines['bottom'].set_visible(False)
        axes.spines['left'].set_visible(False)
        self.drawable.set_xlim((-0.5, 1))
        self.drawable.set_xticks(range(0, 2))
        self.drawable.set_yticks([ ])
        axes.xaxis.set_label_position('bottom')
        axes.xaxis.tick_bottom()
