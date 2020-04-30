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

	def draw(self, G, s=100, node_style=None, edge_style=None, *args, **kwargs):
		"""
		Draw the given graph.

		Any additional arguments and keyword arguments are passed on to the :func:`networkx.spring_layout` function.

		:param G: The networkx graph to draw.
		:type G: :class:`networkx.classes.graph.Graph`
		:param s: The size of the nodes.
		:type s: float
		:param node_style: The general style for nodes.
						   Keys correspond to the styling parameter and the values are the styling value.
						   They are passed on as keyword arguments to the :func:`~graph.graph.Graph._draw_nodes` function.
		:type node_style: dict
		:param edge_style: The general style for edges.
						   Keys correspond to the styling parameter and the values are the styling value.
						   They are passed on as keyword arguments to the :func:`~graph.graph.Graph._draw_edges` function.
		:type edge_style: dict

		:return: A tuple containing the list of drawn nodes and edges.
		:rtype: tuple
		"""

		node_style = node_style or { }
		edge_style = edge_style or { }

		self.drawable.axis.axis('off')
		positions = nx.spring_layout(G, *args, **kwargs)
		nodes = self._draw_nodes(positions, s=s, **node_style)
		edges = self._draw_edges(G.edges, positions, **edge_style)
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

		:return: A list of drawn edges.
		:rtype: list of :class:`matplotlib.lines.Line2D`
		"""

		paths = [ ]

		for edge in edges:
			source, target = nodes[edge[0]], nodes[edge[1]]
			x, y = (source[0], target[0]), (source[1], target[1])
			paths.append(self.drawable.plot(x, y, zorder=-1, *args, **kwargs)[0])

		return paths
