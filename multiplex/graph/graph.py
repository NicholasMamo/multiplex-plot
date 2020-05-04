"""
The :class:`~Graph` class can be used to draw directed or undirected graphs.
Each graph is made up of nodes and edges and can be used to show the relations between nodes.

.. image:: ../examples/exports/4-marvel.png
   :width: 500
   :align: center

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

	def draw(self, G, node_style=None, name_style=None, edge_style=None, *args, **kwargs):
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
						   Individual nodes can override this style using the `style` attribute.
		:type node_style: dict
		:param name_style: The general style for names.
						   Keys correspond to the styling parameter and the values are the styling value.
						   They are passed on as keyword arguments to the :func:`~graph.graph.Graph._draw_node_names` function.
						   Individual names can override this style using the `style` attribute.
		:type name_style: dict
		:param edge_style: The general style for edges.
						   Keys correspond to the styling parameter and the values are the styling value.
						   They are passed on as keyword arguments to the :func:`~graph.graph.Graph._draw_edges` function.
						   Individual edges can override this style using the `style` attribute.
		:type edge_style: dict

		:return: A tuple containing the list of drawn nodes, their names, and edges.
		:rtype: tuple
		"""

		node_style = node_style or { }
		name_style = name_style or { }
		edge_style = edge_style or { }

		self.drawable.axis.axis('off')
		positions = nx.spring_layout(G, *args, **kwargs)
		nodes = self._draw_nodes(G.node, positions, **node_style)
		node_names = self._draw_node_names(G.node, positions, **name_style)
		edges = self._draw_edges(G.edges, positions, **edge_style)
		return nodes, node_names, edges

	def _draw_nodes(self, nodes, positions, *args, **kwargs):
		"""
		Draw the nodes onto the :class:`~drawable.Drawable`.

		Any additional arguments and keyword arguments are passed on to the :func:`matplotlib.pyplot.scatter` function.

		The nodes should be given as dictionaries, whose keys are the node names.
		The corresponding values are their positions.

		:param nodes: The list of actual nodes to draw.
		:type nodes: networkx.classes.reportviews.NodeView
		:param positions: The positions of the nodes as a dictionary.
						  The keys are the node names, and the values are the corresponding positions.
		:type positions: dict

		:return: A dictionary of rendered nodes.
				 The keys are the node names and the values are :class:`matplotlib.collections.PathCollection`, representing the rendered nodes.
		:rtype: dict
		"""

		rendered = { }

		"""
		Extract the node positions and draw scatter plots.
		"""
		x = [ position[0] for position in positions.values() ]
		y = [ position[1] for position in positions.values() ]
		for node, x, y in zip(nodes, x, y):
			node_style = dict(kwargs)
			node_style.update(nodes[node].get('style', { }))
			node_style.update({ 'marker': 'o' }) # TODO: do it properly
			rendered[node] = self.drawable.scatter(x, y, *args, **node_style)

		return rendered

	def _draw_node_names(self, nodes, positions, *args, **kwargs):
		"""
		Draw labels for the nodes.
		Labels are drawn if they have a `name` attribute.
		The `name_style` attribute, if given, is used to override the default label style.
		By default, nodes are aligned centrally and are positioned above the node.

		Any additional keyword arguments are considered to be styling options.

		:param nodes: The list of nodes for which to draw labels.
		:type nodes: :class:`networkx.classes.reportviews.NodeView`
		:param positions: The positions of the nodes as a dictionary.
						  The keys are the node names, and the values are the corresponding positions.
		:type positions: dict

		:return: The list of drawn labels.
		:rtype: list of :class:`~text.annotation.Annotation`
		"""

		annotations = [ ]

		"""
		Extract the node positions and draw the names.
		"""
		x = [ position[0] for position in positions.values() ]
		y = [ position[1] for position in positions.values() ]
		for node, x, y in zip(nodes, x, y):
			node = nodes[node]
			"""
			Nodes are drawn only if they have a name attribute.
			"""
			name = node.get('name')
			if name:
				"""
				By default, node names are aligned centrally and are positioned above the node.
				However, the style can be overriden by providing a `name_style` attribute.
				"""
				default_style = { 'align': 'center', 'va': 'bottom' }
				default_style.update(**kwargs)
				style = node.get('name_style', { })
				default_style.update(style)

				"""
				The position of the name depends on the node's radius.
				This is transformed into a padding value.
				"""
				pad = self._get_radius(node)

				"""
				Draw the annotation.
				"""
				# TODO: Add support for drawing names on the left or right of nodes.
				annotation = self.draw_label(name, (x - pad * 2, x + pad * 2), y,
											 pad=pad/2., **default_style)
				annotations.append(annotation)

		return annotations

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

		# TODO: Add support for directed graphs.
		# TODO: Add support for same-node edges.

		rendered = [ ]

		for edge in edges:
			source, target = nodes[edge[0]], nodes[edge[1]]
			x, y = (source[0], target[0]), (source[1], target[1])
			edge_style = dict(kwargs)
			edge_style.update(edges[edge].get('style', { }))
			rendered.append(self.drawable.plot(x, y, zorder=-1, *args, **edge_style)[0])

		return rendered

	def _get_radius(self, node):
		"""
		Get the radius of the given node in terms of the data axis.
		By default, the radius `s` is 100, but it can be overriden using the node's `style` attribute.

		.. note::

			The square root of the radius is taken because `the radius is originally squared <https://matplotlib.org/3.2.0/api/_as_gen/matplotlib.pyplot.scatter.html>`_.

		:param node: The node whose radius will be calculated.
		:type node: dict
		"""

		s = node.get('style', { }).get('s', 100)
		return (self.drawable.axis.transData.inverted().transform((0, s ** 0.5))[1] -
				self.drawable.axis.transData.inverted().transform((0, 0))[1])
