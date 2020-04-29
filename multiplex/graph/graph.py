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
