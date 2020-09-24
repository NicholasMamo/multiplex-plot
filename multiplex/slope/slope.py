"""
The :class:`~Slope` class allows you to create slope graphs that show how values changed, such as:

- Before and after an operation, or
- Over a time period.

Slope graphs are not commonly included in visualization packages, but they can be great tools to tell a story.
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

    def draw(self):
        """
        Draw a slope graph.
        The function returns a two-tuple with the drawn plot (a line with optional markers) and any drawn labels.

        :return: A tuple made up of the drawn plot and any drawn labels.
                 If the legend label is drawn, only a string is returned.
        :rtype: tuple
        """

        return (None, None)
