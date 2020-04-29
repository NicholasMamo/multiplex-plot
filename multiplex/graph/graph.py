"""
The :class:`~Graph` class can be used to draw directed or undirected graphs.
Each graph is made up of nodes and edges and can be used to show the relations between nodes.
"""

import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
import util

from labelled import LabelledVisualization

class Graph(LabelledVisualization):
	"""
	The :class:`~Graph` class draws nodes and edges.
	"""

	def __init__(self, *args, **kwargs):
		"""
		Initialize the graph.
		"""

		super().__init__(*args, **kwargs)

	def draw(self, G, s=100, *args, **kwargs):
		"""
		Draw the given graph.

		Any additional arguments and keyword arguments are passed on to the node and edge drawing functions.

		:param G: The networkx graph to draw.
		:type G: :class:`networkx.classes.graph.Graph`
		:param s: The size of the nodes.
		:type s: float

		:return: A tuple containing the list of drawn nodes and edges.
		:rtype: tuple
		"""

