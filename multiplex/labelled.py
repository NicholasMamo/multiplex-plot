"""
A labelled visualization is one that allows labels.
These labels are normal :class:`~text.text.TextAnnotation`.
However, a labelled visualization has functionality to ensure that the labels do not overlap.
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import util

from visualization import Visualization
from text.text import Annotation

class LabelledVisualization(Visualization):
	"""
	The labelled visualization adds functionality to visualizations that use labels.
	Labels are normal :class:`~text.text.TextAnnotation`.
	This class adds functionality to distribute overlapping labels.

	:ivar labels: The labels in the visualizations.
				  This list is used to ensure that labels do not overlap.
	:vartype labels: list of :class:`~text.text.TextAnnotation`
	"""

	def __init__(self, *args, **kwargs):
		"""
		Create the labelled visualization by initializing the list of labels.
		"""

		super().__init__(*args, **kwargs)
		self.labels = [ ]

	def draw_label(self, label, x, y, *args, **kwargs):
		"""
		Draw a label at the end of the line.

		:param label: The label to draw.
		:type label: str
		:param x: The x-position of the last point on the line.
		:type x: float
		:param y: The y-position of the last point on the line.
		:type y: float
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis
		xlim_width = abs(axis.get_xlim()[1] - axis.get_xlim()[0])

		annotation = Annotation(self.drawable)
		annotation.draw(label, (x * 1.01, x * 1.01 + xlim_width * 0.2),
						y, va='center', *args, **kwargs)
		self.labels.append(annotation)
		self._arrange_labels()

	def _arrange_labels(self):
		"""
		Go through the labels and ensure that none overlap.
		If any do overlap, move the labels.
		The function keeps repeating until no labels overlap.

		.. image:: ../examples/exports/3-overlapping-labels.png
		   :class: example
		"""

		overlapping = self._get_overlapping_labels()
		while overlapping:
			for group in overlapping:
				self._distribute_labels(group)
			overlapping = self._get_overlapping_labels()

	def _get_overlapping_labels(self):
		"""
		Get groups of overlapping labels.
		The function returns a list of lists.
		Each inner list contains the labels that overlap.
		The function automatically excludes labels that do not overlap with other labels.

		:return: A list of lists.
				 Each inner list represents overlapping labels.
		:rtype: list of lists of :class:`matplotlib.text.Text`
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis

		labels = sorted(self.labels, key=lambda label: label.get_virtual_bb().y0)

		overlapping_labels = [ ]
		for label in labels:
			assigned = False

			"""
			Go through each label and visit each group of overlapping labels.
			If the label overlaps with any label in that group, add it to that group.
			That group would have to be distributed entirely.
			"""
			for group in overlapping_labels:
				if (any([ util.overlapping_bb(label.get_virtual_bb(), other.get_virtual_bb()) for other in group ])):
					group.append(label)
					assigned = True
					break

			"""
			If the label does not overlap with any other label, add it to its own group.
			Groups with a single label overlap with no other group and require no distribution.
			"""
			if not assigned:
				overlapping_labels.append([ label])

		return [ group for group in overlapping_labels if len(group) > 1 ]

	def _distribute_labels(self, labels):
		"""
		Distribute the given labels so that they do not overlap.

		:param labels: The list of overlapping labels.
		:type labels: list of :class:`matplotlib.text.Text`
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis

		"""
		Calculate the total height that the labels should occupy.
		Then, get the mean y-coordinate of the labels to find the middle.
		"""
		total_height = self._get_total_height(labels)
		middle = self._get_middle(labels)

		"""
		Sort the labels in descending order of position.
		Since labels are centered around the last point, the sorting is based on the center of labels.
		The labels are moved one by one.

		The initial offset is calculated as the distance that the first label needs to move.
		Subsequently, the offset is calculated by adding the height of each label.
		"""
		labels = sorted(labels, reverse=True,
						key=lambda label: (label.get_virtual_bb().y0 + label.get_virtual_bb().y1)/2.)

		y1 = middle + total_height / 2.
		for label in labels:
			bb = label.get_virtual_bb()
			label.set_position((bb.x0, y1))
			y1 -= bb.height

	def _get_total_height(self, labels):
		"""
		Get the total height of the given labels.

		:param labels: The list of labels.
		:type labels: list of :class:`matplotlib.text.Text`

		:return: The total height of the labels.
		:rtype: float
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis

		return sum([ label.get_virtual_bb().height for label in labels ])

	def _get_middle(self, labels):
		"""
		Get the middle y-coordinate of the given labels.
		The middle is calculated as the mid-point between the label that is highest and lowest.

		:param labels: The list of labels.
		:type labels: list of :class:`matplotlib.text.Text`

		:return: The middle y-coordinate of the labels.
		:rtype: float
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis

		labels = sorted(labels, key=lambda label: label.get_virtual_bb().y0)
		bb0, bb1 = labels[0].get_virtual_bb(), labels[-1].get_virtual_bb()

		return (bb0.y0 + bb1.y1) / 2.
