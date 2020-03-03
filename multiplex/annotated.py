"""
An annotated visualization allows you to draw text on plots to describe data better.
The annotations use :class:`~text.text.TextAnnotation` to draw text on the plot.
Therefore you can use all of the text annotation flexibility to explain the visualization, and not just show it.
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import util

from text.text import Annotation
from visualization import Visualization

class AnnotatedVisualization(Visualization):
	"""
	Annotated visualizations use the most basic of explanations—text—to describe graphics.
	The annotations use :class:`~text.text.TextAnnotation` to draw text on the plot.

	:ivar annotations: The annotations in the visualization.
	:vartype annotations: list of :class:`~text.text.TextAnnotation`
	"""

	def __init__(self, *args, **kwargs):
		"""
		Create the annotated visualization by initializing the list of annotations.
		"""

		super().__init__(*args, **kwargs)
		self.annotations = [ ]

	def annotate(self, text, x, y, *args, **kwargs):
		"""
		Add an annotation to the plot.
		Any additional arguments and keyword arguments are passed on to the annotation's :meth:`~text.text.TextAnnotation.draw` function.
		For example, the `va` can be provided to specify the vertical alignment.
		The `align` parameter can be used to specify the text's alignment.

		:param text: The text of the annotation to draw.
		:type text: str
		:param x: A tuple containing the start and end x-coordinates of the annotation.
		:type x: tuple
		:param y: The y-coordinate of the annotation.
		:type y: float
		"""

		annotation = Annotation(self.drawable)
		tokens = annotation.draw(text, x, y, *args, **kwargs)
		self.annotations.append(annotation)
		return tokens
