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

import math
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
		node_names = self._draw_node_names(G.node, positions,
										   s=node_style.get('s', 100), **name_style)
		edges = self._draw_edges(G.edges, G.nodes, positions,
								 s=node_style.get('s', 100),
								 directed=nx.is_directed(G), **edge_style)
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

	def _draw_node_names(self, nodes, positions, s, *args, **kwargs):
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
		:param s: The default radius of the node.
				  It may be overwritten with the node's own radius.
		:type s: float

		:return: A dictionary of rendered nodes.
				 The keys are the node names and the values are :class:`~text.annotation.Annotation`, representing the rendered annotations.
		:rtype: dict
		"""

		annotations = { }

		"""
		Extract the node positions and draw the names.
		"""
		x = [ position[0] for position in positions.values() ]
		y = [ position[1] for position in positions.values() ]
		for node, x, y in zip(nodes, x, y):
			"""
			Nodes are drawn only if they have a name attribute.
			"""
			name = nodes[node].get('name')
			if name:
				"""
				By default, node names are aligned centrally and are positioned above the node.
				However, the style can be overriden by providing a `name_style` attribute.
				"""
				default_style = { 'align': 'center', 'va': 'bottom' }
				default_style.update(**kwargs)
				style = nodes[node].get('name_style', { })
				default_style.update(style)

				"""
				The position of the name depends on the node's radius.
				This is transformed into a padding value.
				"""
				pad = self._get_radius(nodes[node],
									   s=nodes[node].get('style', { }).get('s', s))[1]

				"""
				Draw the annotation.
				"""
				# TODO: Add support for drawing names on the left or right of nodes.
				annotation = self.draw_label(name, (x - pad * 2, x + pad * 2), y,
											 pad=pad/2., **default_style)
				annotations[node] = annotation

		return annotations

	def _draw_edges(self, edges, nodes, positions, s, directed=False, *args, **kwargs):
		"""
		Draw the edges connecting the given nodes.
		Depending on whether the graph is undirected or directed, the edges are drawn with arrows.

		Any additional arguments and keyword arguments are passed on to the :func:`matplotlib.pyplot.plot` function or as arrowprops.

		:param edges: The list of edges to draw.
					  The edges should be a list of tuples representing the source and target.
		:type edges: list of tuple
		:param nodes: The list of graph nodes.
					  These are not the rendered nodes, but the graph nodes.
		:type nodes: networkx.classes.reportviews.NodeView
		:param positions: The positions of the nodes as a dictionary.
						  The keys are the node names, and the values are the corresponding positions.
						  They are used to connect the edges together.
		:type positions: dict
		:param s: The default radius of the node.
				  It may be overwritten with the node's own radius.
		:type s: float
		:param directed: A boolean indicating whether the graph is directed or not.
		:type directed: bool

		:return: A list of drawn edges.
				 If the graph is undirected, lines are returned.
				 Otherwise, annotations (with arrows) are returned.
		:rtype: list of :class:`matplotlib.lines.Line2D` or list of :class:`matplotlib.text.Annotation`
		"""

		rendered = { }

		for source, target in edges:
			if source == target:
				self._draw_loop(nodes[target], positions[target],
								s=nodes[target].get('style', { }).get('s', s),
								directed=directed, *args, **kwargs)
				continue

			"""
			Load the edge's style.
			The keyword arguments may be overwritten by the edge's style.
			"""
			u, v = list(positions[source]), list(positions[target])
			edge_style = dict(kwargs)
			edge_style.update(edges[(source, target)].get('style', { }))

			if not directed:
				"""
				If the graph is not directed, connect the two nodes' centers with a straight line.
				"""
				x, y = (u[0], v[0]), (u[1], v[1])
				rendered[(source, target)] = self.drawable.plot(x, y, zorder=-1, *args, **edge_style)[0]
			if directed:
				"""
				If the graph is directed, calculate the radius of the target node.
				This is where the arrow should end.
				Calculate the distance between the two centers and reduce from it the radius of the target node.
				This is done so that the arrow is not under the target node, but outside and pointing to it.
				"""
				radius = self._get_radius(nodes[target],
										  s=nodes[target].get('style', { }).get('s', s))
				distance = [ v[0] - u[0], v[1] - u[1] ]
				magnitude = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
				normalized = [ distance[0] / magnitude, distance[1] / magnitude ]
				ratio = util.get_aspect(self.drawable.axis)
				angle = self._get_angle(u, v)
				if ratio > 1:
					diff = abs(radius[0] * math.cos(angle)) / ratio + abs(radius[1] * math.sin(angle))
				else:
					diff = abs(radius[0] * math.cos(angle)) + abs(radius[1] * math.sin(angle)) * ratio

				"""
				Retract the line by the radius.
				"""
				v = [ u[0] + normalized[0] * (magnitude - diff),
				 	  u[1] + normalized[1] * (magnitude - diff) ]
				rendered[(source, target)] = self.drawable.axis.annotate('', xy=v, xytext=u,
																		 zorder=-1, arrowprops=edge_style)

		return rendered

	def _draw_loop(self, node, position, s, directed, *args, **kwargs):
		"""
		Draw a loop, indicating an edge from a node to itself.

		Any additional arguments and keyword arguments are passed on to the edge drawing functions.

		:param node: The node where to draw a loop.
		:type node: ?
		:param position: The position of the node as a tuple.
		:type position: tuple
		:param s: The default radius of the node.
				  It may be overwritten with the node's own radius.
		:type s: float
		:param directed: A boolean indicating whether the graph is directed or not.
		:type: bool

		:return: ?
		:rtype: ?
		"""

		"""
		Get the node's radius and use it to calculate the loop's radius.
		The loop's radius is calculated as a fraction of the node's radius.
		"""
		radius = self._get_radius(node, s)
		loop = ( radius[0] * 0.75, radius[1] * 0.75 )

		"""
		Draw a loop first.
		This is always drawn, regardless if the edge is directed or not.
		It is assumed that the node is a circle.
		"""
		ratio = util.get_aspect(self.drawable.axis)
		x = [ position[0] + loop[0] * math.cos(math.pi / 180 * i) for i in range(-25, 360-160) ]
		y = [ (position[1] + radius[1] / 0.75) + loop[1] * math.sin(math.pi / 180 * i) for i in range(-25, 360-160) ]

		"""
		Remove some style attributes that belong to arrows, not edges.
		"""
		edge_style = dict(kwargs)
		edge_style.pop('headwidth', None)
		edge_style.pop('headlength', None)
		edge_style['linewidth'] = edge_style.get('linewidth', 1) * 2
		self.drawable.plot(x, y, zorder=-1, **edge_style)

		"""
		If the arrow is directed, calculate its position.
		The arrow points is set to always point downwards.
		"""
		if directed:
			arrowprops = dict(kwargs)
			arrowprops['headwidth'] = arrowprops.get('headwidth') * 0.75
			arrowprops['headlength'] = arrowprops.get('headwidth') * 0.75
			xy = ( position[0] + loop[0] * math.cos(math.pi),
			 			 (position[1] + radius[1] / 0.75) + loop[1] * math.sin(3 * math.pi / 2) )
			xytext = ( xy[0], xy[1] + radius[1] / 100 )
			self.drawable.axis.annotate('', xy=xy, xytext=xytext,
										zorder=-1, arrowprops=arrowprops)

	def _get_angle(self, source, target):
		"""
		Get the angle between the source and target nodes.

		:param source: The source node's position as a tuple.
		:type source: tuple
		:param target: The target node's position as a tuple.
		:type target: tuple

		:return: The angle between the source and target nodes in radians.
		:rtype: float
		"""

		xdiff = target[0] - source[0]
		ydiff = target[1] - source[1]

		return math.atan2(ydiff, xdiff)

	def _get_radius(self, node, s):
		"""
		Get the radius of the given node in terms of the data axis.
		By default, the radius `s` is 100, but it can be overriden using the node's `style` attribute.

		.. note::

			The square root of the radius is taken because `the radius is originally squared <https://matplotlib.org/3.2.0/api/_as_gen/matplotlib.pyplot.scatter.html>`_.

		:param node: The node whose radius will be calculated.
		:type node: dict
		:param s: The default radius of the node.
				  It may be overwritten with the node's own radius.
		:type s: float

		:return: The radius of the node in terms of the data axis.
				 Two radii are provided: the x- and y-radii.
				 This is because scatter points always look like circles, even when the display or data ratios are not equal.
				 Whn the display or data ratios are not equal, the point is actually an ellipse so that it still looks like a circle.
		:rtype: tuple
		"""

		origin = self.drawable.axis.transData.inverted().transform((0, 0))

		x = (self.drawable.axis.transData.inverted().transform((s ** 0.5, 0))[0] - origin[0])/2.
		y = (self.drawable.axis.transData.inverted().transform((0, s ** 0.5))[1] - origin[1])/2.
		return (x, y)
