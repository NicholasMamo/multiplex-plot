"""
The :class:`~Graph` class can be used to draw directed or undirected graphs.
Each graph is made up of nodes and edges and can be used to show the relations between nodes.

.. note::

	The graph visualization uses the `networkx` package to generate the layout of the graph.
	Therefore it is a prerequisite to create these visualizations.
"""

import networkx as nx
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

	def draw(self, G, s=100, k=None, *args, **kwargs):
		"""
		Draw the given graph.

		Any additional arguments and keyword arguments are passed on to the node and edge drawing functions.

		:param G: The networkx graph to draw.
		:type G: :class:`networkx.classes.graph.Graph`
		:param s: The size of the nodes.
		:type s: float
		:param k: The optimal distance between nodes, bound between 0 and 1.
				  If `None` is given, networkx's default value of :math:`\\func{1}{\\sqrt{n}}`, where :math:`n` is the number of nodes, is used.
				  The higher the number, the more distance between nodes.
		:type k: float

		:return: A tuple containing the list of drawn nodes and edges.
		:rtype: tuple
		"""

		self.drawable.axis.axis('off')
		positions = nx.spring_layout(G, k=k)
		nodes = self._draw_nodes(positions, s=s, *args, **kwargs)
		edges = self._draw_edges(G.edges, positions, *args, **kwargs)
		return nodes, edges

	def _draw_nodes(self, positions, s, *args, **kwargs):
		"""
		Draw the nodes onto the :class:`~drawable.Drawable`.

		Any additional arguments and keyword arguments are passed on to the :func:`matplotlib.pyplot.scatter` function.

		The nodes should be given as dictionaries, whose keys are the node names.
		The corresponding values are their positions.

		:param positions: The positions of the nodes as a dictionary.
						  The keys are the node names, and the values are the corresponding positions.
		:type positions: dict
		:param s: The size of the nodes.
		:type s: float

		:return: The list of drawn nodes.
		:rtype: :class:`matplotlib.collections.PathCollection`
		"""

		nodes = [ ]

		"""
		Extract the node positions and draw scatter plots.
		"""
		x = [ position[0] for position in positions.values() ]
		y = [ position[1] for position in positions.values() ]
		nodes = self.drawable.scatter(x, y, s=s, *args, **kwargs)

		return nodes

	def _draw_edges(self, edges, nodes, *args, **kwargs):
		"""
		Draw the edges connecting the given nodes.

		Any additional arguments and keyword arguments are passed on to the :func:`matplotlib.pyplot.plot` function.

		:param edges: The list of edges to draw.
					  The edges should be a list of tuples representing the source and target.
		:type edges: list of tuple
		:param nodes: The nodes in terms of their positions as a dictionary.
					  The keys are the node names, and the values are the corresponding positions.
		:type nodes: dict
		"""

		paths = [ ]

		for edge in edges:
			source, target = nodes[edge[0]], nodes[edge[1]]
			x, y = (source[0], target[0]), (source[1], target[1])
			paths.append(self.drawable.plot(x, y, zorder=-1, *args, **kwargs))

		return paths
