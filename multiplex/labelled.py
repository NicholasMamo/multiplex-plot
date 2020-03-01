"""
A labelled visualization is one that allows labels.
These labels are normal :class:`~text.text.TextAnnotation`.
However, a labelled visualization has functionality to ensure that the labels do not overlap.
"""

class LabelledVisualization(object):
	"""
	The labelled visualization adds functionality to visualizations that use labels.
	Labels are normal :class:`~text.text.TextAnnotation`.
	This class adds functionality to distribute overlapping labels.

	:ivar labels: The labels in the time series.
				  This list is used to ensure that labels do not overlap.
	:vartype labels: list of :class:`~text.text.TextAnnotation`
	"""

	def __init__(self):
		"""
		Create the labelled visualization by initializing the list of annotations that make up the labels.
		"""

		self.labels = [ ]
