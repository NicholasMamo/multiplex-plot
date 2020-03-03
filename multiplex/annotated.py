"""
An annotated visualization allows you to draw text on plots to describe data better.
The annotations use :class:`~text.text.TextAnnotation` to draw text on the plot.
Therefore you can use all of the text annotation flexibility to explain the visualization, and not just show it.
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import util

from visualization import Visualization
from text.text import Annotation

class AnnotatedVisualization(Visualization):
	"""
	Annotated visualizations use the most basic of explanations—text—to describe graphics.
	The annotations use :class:`~text.text.TextAnnotation` to draw text on the plot.
	"""

	pass
