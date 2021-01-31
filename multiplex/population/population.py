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
    """
