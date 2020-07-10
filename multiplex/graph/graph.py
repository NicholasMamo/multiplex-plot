"""
Multiplex's graph visualizations use the popular `networkx <https://networkx.github.io/>`_ library.
If you already use networkx, you can visualize networks in a handful of lines:

.. code-block:: python

	import matplotlib.pyplot as plt
	import networkx as nx
	from multiplex import drawable
	viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
	G = nx.path_graph(5)
	viz.draw_graph(G, edge_style={ 'color': 'C1' },
	               node_style={ 'color': 'C4', 'edgecolor': 'C1', 'linewidth': 2, 's': 250 })
	viz.show()

Although Multiplex requires only the graph, you can style the nodes and the edges using the ``node_style`` and ``edge_style`` parameters.

Multiplex supports both undirected and directed edges.
Moreover, the library also supports self-connections, or edges from a node to itself.

Apart from drawing nodes and edges, Multiplex is also capable of drawing names next to nodes and edges.
These can be used, for instance, to write node names or describe the types of relations between nodes.

Finally, Multiplex's graphs also support legend labels for both nodes and edges.

.. warning::

	The graph visualization uses the `networkx <https://networkx.github.io/>`_ package to generate the layout of the graph.
	Therefore it is a prerequisite to have it installed before creating these visualizations.
"""

import math
import networkx as nx
import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
import util

from labelled import LabelledVisualization
from text.annotation import Annotation

class Graph(LabelledVisualization):
	"""
	The :class:`~Graph` class is a general network graph that plots nodes and creates edges between them.
	Like all visualizations, it stores a :class:`~drawable.Drawable` instance and revolves around the :func:`~Graph.draw` function.

	The :class:`~Graph` class builds on the :class:`~labelled.LabelledVisualization`.
	The reason why the :class:`~Graph` builds on that, and not the simpler :class:`~visualization.Visualization`, is that it uses the :class:`~labelled.LabelledVisualization`'s labels for node names.
	In this way, the :class:`~Graph` automatically ensures that the node names do not overlap.
	"""

	def __init__(self, *args, **kwargs):
		"""
		Initialize the graph.
		"""

		super().__init__(*args, **kwargs)

	def draw(self, G, positions=None, node_style=None, name_style=None, edge_style=None, label_style=None, *args, **kwargs):
		"""
		Draw the given `networkx graph <https://networkx.github.io/documentation/stable/reference/classes/index.html>`_ on the :class:`~drawable.Drawable`.

		The method expects only a graph.
		Differently from other visualizations, the styling options are passed on as ``dict`` arguments.

		By default, this method generates the node positions using the `networkx.spring_layout <https://networkx.github.io/documentation/stable/reference/generated/networkx.drawing.layout.spring_layout.html?highlight=spring_layout#networkx.drawing.layout.spring_layout>`_ function.
		The ``args`` and ``kwargs`` are passed on to this function to control how the graph looks.
		However, you can provide your own node positions in the ``positions`` argument.

		To draw the graph, the :class:`~Graph` draws three types of components:

			1. Nodes using `matplotlib's scatter function <https://matplotlib.org/3.2.2/api/_as_gen/matplotlib.pyplot.scatter.html>`_,
			2. Undirected edges using `matplotlib's plot function <https://matplotlib.org/3.2.2/api/_as_gen/matplotlib.pyplot.plot.html>`_ and
			   directed edges using `matplotlib's annotate function <https://matplotlib.org/3.2.2/api/_as_gen/matplotlib.pyplot.annotate.html>`_, and
			3. Node and edge names using :class:`~text.annotation.Annotation`.

		The :class:`~Graph` automatically draws names next to nodes and edges whenever it finds a ``name`` attribute.
		You can set the name directly on the node or edge in the graph:

		.. code-block:: python

			G.nodes['u']['name'] = 'node'
			G.edges[('u', 'v')]['name'] = 'edge'

		Similarly, the :class:`~Graph` adds a legend for nodes and edges whenever it finds a ``label`` attribute.
		You can set the label directly on the node or edge in the graph:

		.. code-block:: python

			G.nodes['u']['label'] = 'node'
			G.edges[('u', 'v')]['label'] = 'edge'

		:param G: The networkx graph to draw.
				  The function automatically detects whether the graph is undirected or directed and draws the edges accordingly.
		:type G: :class:`networkx.classes.graph.Graph`
		:param positions: The node's initial positions.
						  If you provide no positions, the function uses the `networkx.spring_layout <https://networkx.github.io/documentation/stable/reference/generated/networkx.drawing.layout.spring_layout.html?highlight=spring_layout#networkx.drawing.layout.spring_layout>`_ function to find the best position for nodes.
						  If you provide a position for a subset of the nodes, the rest of the positions are generated automatically.

						  You can provide the positions with node names as keys and their positions as values.
						  Positions must be tuples: the x and y coordinates.
		:type positions: dict
		:param node_style: The general style for nodes.
			   			   The ``node_style`` accepts any styling option supported by `matplotlib's scatter function <https://matplotlib.org/3.2.2/api/_as_gen/matplotlib.pyplot.scatter.html>`_.

						   You can override the general style of the nodes by giving them a ``style`` attribute:

						   .. code-block:: python

			   			     G.nodes['u']['style'] = { 'color': '#BB3633' }

						   .. note::

						     You can set the size of nodes by setting the ``s`` key in the ``node_style``.
						     By default, the size is 100.
		:type node_style: dict
		:param name_style: The general style for names.
			   			   The ``name_style`` accepts any styling option supported by the :class:`~text.annotation.Annotation`'s :func:`~text.annotation.Annotation.draw` function.

						   You can override the general style of the names by giving nodes and edges a ``name_style`` attribute:

						   .. code-block:: python

			   			     G.nodes['u']['name_style'] = { 'fontweight': 'bold' }
			   			     G.edges[('u', 'v')]['name_style'] = { 'fontweight': 'bold' }
		:type name_style: dict
		:param edge_style: The general style for edges.
		 				   The ``edge_style`` accepts any styling option supported by `matplotlib's plot <https://matplotlib.org/3.2.2/api/_as_gen/matplotlib.pyplot.plot.html>`_ and `annotate <https://matplotlib.org/3.2.2/api/_as_gen/matplotlib.pyplot.annotate.html>`_ functions.

						   You can override the general style of the edges by giving them a ``style`` attribute:

						   .. code-block:: python

						     G.edges[('u', 'v')]['style'] = { 'color': '#BB3633' }
		:type edge_style: dict
		:param label_style: The general style for labels.
							The ``label_style`` accepts any styling option supported by the :class:`~text.annotation.Annotation`'s :func:`~text.annotation.Annotation.draw` function.
		:type label_style: dict or None

		:return: A tuple containing the drawn components:

				 1. A list of drawn nodes as :class:`matplotlib.collections.PathCollection` instances,
				 2. A list of rendered node names as :class:`~text.annotation.Annotation` instances,
				 3. A list of edges as :class:`matplotlib.lines.Line2D` instances if the graph is undirected or as :class:`matplotlib.text.Annotation` if the graph is directed, and
				 4. A list of rendered edge names as :class:`~text.annotation.Annotation` instances.
		:rtype: tuple
		"""

		positions = positions or { }
		node_style = node_style or { }
		name_style = name_style or { }
		edge_style = edge_style or { }
		label_style = label_style or { }

		self.drawable.axes.axis('off')
		spring = nx.spring_layout(G, *args, **kwargs)
		spring.update(positions)
		positions = spring
		nodes = self._draw_nodes(G.node, positions, **node_style)
		node_names = self._draw_node_names(G.nodes, positions,
										   s=node_style.get('s', 100), **name_style)
		edges = self._draw_edges(G.edges, G.nodes, positions,
								 s=node_style.get('s', 100),
								 directed=nx.is_directed(G), **edge_style)
		edge_names = self._draw_edge_names(G.edges, G.nodes, positions,
										   s=node_style.get('s', 100), **name_style)
		self._draw_node_labels(G.nodes, label_style=label_style, **node_style)
		self._draw_edge_labels(G.edges, directed=nx.is_directed(G), label_style=label_style, **edge_style)
		return nodes, node_names, edges, edge_names

	def _draw_nodes(self, nodes, positions, *args, **kwargs):
		"""
		Draw the nodes onto the :class:`~drawable.Drawable`.

		Any additional arguments and keyword arguments are passed on to the `matplotlib.pyplot.scatter <https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.scatter.html>`_ function.

		The nodes should be given as dictionaries, whose keys are the node names.
		The corresponding values are their positions.

		:param nodes: The list of actual nodes to draw.
		:type nodes: networkx.classes.reportviews.NodeView
		:param positions: The positions of the nodes as a dictionary.
						  The keys are the node names, and the values are the corresponding positions.
		:type positions: dict

		:return: A dictionary of rendered nodes.
				 The keys are the node names and the values are `matplotlib.collections.PathCollection <https://matplotlib.org/3.1.1/api/collections_api.html>`_, representing the rendered nodes.
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
		Draw names for the nodes.
		Names are drawn if they have a `name` attribute.
		The `name_style` attribute, if given, is used to override the default name style.
		By default, names are aligned centrally and are positioned above the node.

		Any additional keyword arguments are considered to be styling options.

		:param nodes: The list of nodes for which to draw names.
		:type nodes: :class:`networkx.classes.reportviews.NodeView`
		:param positions: The positions of the nodes as a dictionary.
						  The keys are the node names, and the values are the corresponding positions.
		:type positions: dict
		:param s: The default radius of the node.
				  It may be overwritten with the node's own radius.
		:type s: float

		:return: A dictionary of rendered node names.
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
											 pad=pad, **default_style)
				annotations[node] = annotation

		return annotations

	def _draw_edges(self, edges, nodes, positions, s, directed=False, *args, **kwargs):
		"""
		Draw the edges connecting the given nodes.
		Depending on whether the graph is undirected or directed, the edges are drawn with arrows.

		Any additional arguments and keyword arguments are passed on to the `matplotlib.pyplot.plot <https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.plot.html>`_ function or as arrowprops.

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
				rendered[(source, target)] = self._draw_loop(nodes[target], positions[target],
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

			"""
			Update the start and end positions so that the edges do not start and end at the center of the nodes.
			This allows nodes to be transparent without the edges looking bad.
			This is done by calculating the radius of the nodes, which is where the edges should end.
			Calculate the distance between the two centers and reduce from it the radius of the source and target nodes.
			"""
			ratio = util.get_aspect(self.drawable.axes)
			angle = self._get_angle(u, v)
			direction = self._get_direction(u, v)
			for node, position in zip([ source, target ], [ u, v ]):
				distance = self._get_distance(u, v) # since positions are changing, the distance has to be computed each time
				radius = self._get_radius(nodes[node], s=nodes[node].get('style', { }).get('s', s))
				if ratio > 1:
					diff = abs(radius[0] * math.cos(angle)) / ratio + abs(radius[1] * math.sin(angle))
				else:
					diff = abs(radius[0] * math.cos(angle)) + abs(radius[1] * math.sin(angle)) * ratio

				"""
				Retract the start and end by the radius.
				"""
				if node == source:
					u = [ u[0] + direction[0] * diff,
						  u[1] + direction[1] * diff ]
				elif node == target:
					v = [ u[0] + direction[0] * (distance - diff),
						  u[1] + direction[1] * (distance - diff) ]

			if not directed:
				"""
				If the graph is not directed, connect the two nodes' centers with a straight line.
				"""
				x, y = (u[0], v[0]), (u[1], v[1])
				rendered[(source, target)] = self.drawable.plot(x, y, zorder=-1, *args, **edge_style)[0]
			if directed:
				rendered[(source, target)] = self.drawable.axes.annotate('', xy=v, xytext=u,
																		 zorder=-1, arrowprops=edge_style)

		return rendered

	def _draw_edge_names(self, edges, nodes, positions, s, *args, **kwargs):
		"""
		Draw names for the edges.
		Names are drawn if they have a `name` attribute.
		The `name_style` attribute, if given, is used to override the default name style.
		Names are written left-to-right.

		Any additional keyword arguments are considered to be styling options.

		:param edges: The list of edges for which to draw names.
		:type edges: :class:`networkx.classes.reportviews.NodeView`
		:param nodes: The list of nodes in the graph.
					  They are used when rendering names for looped edges.
		:type nodes: networkx.classes.reportviews.NodeView
		:param positions: The positions of the nodes as a dictionary.
						  The keys are the node names, and the values are the corresponding positions.
		:type positions: dict
		:param s: The default radius of the node.
				  It may be overwritten with the node's own radius.
		:type s: float

		:return: A dictionary of rendered edge names.
				 The keys are the edge names and the values are :class:`~text.annotation.Annotation`, representing the rendered annotations.
		:rtype: dict
		"""

		annotations = { }

		for (source, target) in edges:
			"""
			Nodes are drawn only if they have a name attribute.
			"""
			name = edges[(source, target)].get('name')
			if name:
				"""
				By default, edge names are aligned centrally.
				However, the style can be overriden by providing a `name_style` attribute.
				"""
				default_style = { 'align': 'center', 'ha': 'left', 'va': 'center' }
				default_style.update(**kwargs)
				style = edges[(source, target)].get('name_style', { })
				default_style.update(style)

				"""
				To draw the name from left to right, order the source and target nodes accordingly.
				"""
				u, v = sorted([ positions[source], positions[target] ],
							  key=lambda node: node[0])

				"""
				Draw the annotation to get an idea of its width and remove it immediately.
				"""
				annotation = Annotation(self.drawable)
				annotation.draw([ name ], (u[0]), u[1], **default_style)
				bb = annotation.get_virtual_bb()
				annotation.remove()

				if source == target:
					"""
					If the edge is a loop, draw the name at the apex.
					"""
					radius = self._get_radius(nodes[source],
											  s=nodes[source].get('style', { }).get('s', s))
					annotation = Annotation(self.drawable)
					x = ( u[0] - bb.width / 2.,
					 	  u[0] + bb.width / 2. )
					y = u[1] + radius[1] * 2 + bb.height
					annotation.draw([ name ], x, y, **default_style)
					continue

				"""
				Re-draw the annotation, this time positionally centered along the edge.
				The rotation depends on the elevation from the source to the target node.
				"""
				ratio = util.get_aspect(self.drawable.axes)
				distance = self._get_distance(u, v)
				direction = self._get_direction(u, v)
				angle = self._get_elevation(u, v)

				"""
				The annotation's x-position is bound rigidly based on the width of the annotation.
				The y-position is based on the angle. This is because the horizontal alignment is always set to `left`.
				"""
				annotation = Annotation(self.drawable)
				x = ( u[0] + direction[0] * distance / 2. - bb.width / 2.,
				 	  u[0] + direction[0] * distance / 2. + bb.width / 2. )
				y = u[1] + direction[1] * distance / 2. + bb.height / 2. * math.sin(angle) * (math.degrees(angle) > 0)
				annotation.draw([ name ], x, y, rotation=math.degrees(angle), **default_style)
				annotations[(source, target)] = annotation

		return annotations

	def _draw_loop(self, node, position, s, directed, offset_angle=math.pi/2, *args, **kwargs):
		"""
		Draw a loop, indicating an edge from a node to itself.

		Any additional arguments and keyword arguments are passed on to the edge drawing functions.

		:param node: The node for which to draw a loop.
		:type node: dict
		:param position: The position of the node as a tuple.
		:type position: tuple
		:param s: The default radius of the node.
				  It may be overwritten with the node's own radius.
		:type s: float
		:param directed: A boolean indicating whether the graph is directed or not.
		:type: bool
		:param offset_angle: The loop's offset angle in radians.
							 By default, the value is :math:`\\frac{\\pi}{2}`, which places the loop on top of the node.
		:type offset_angle: float

		:return: A tuple containing the undirected edge and, if directed, the arrow.
		:rtype: tuple
		"""

		"""
		Get the node's radius and calculate the loop's radius as a fraction of the node's radius.
		To calculate the angles covered by the loop, the loop is initally placed directly above the node.
		Since nodes are circular, the loop's position is just rotated around the node later.
		"""
		radius = self._get_radius(node, s)
		loop = ( radius[0] * 0.5, radius[1] * 0.5 )
		center = ( position[0], position[1] + radius[1] )

		"""
		Get the vertical distance from the node to the place where the loop will intersect with it.
		The notation is taken from `this blog post <https://diego.assencio.com/?index=8d6ca3d82151bad815f78addf9b5c1c6>`_.
		"""
		d = center[1] - position[1]
		d1 = (radius[1] ** 2 - loop[1] ** 2 + d ** 2) / ( 2 * d)
		d2 = d - d1

		"""
		Calculate the horizontal distance from the center of the node to where the node and the loop intersect.
		"""
		ratio = util.get_aspect(self.drawable.axes)
		x1 = math.sqrt( ( (radius[0]) ** 2 * radius[1] ** 2 - (radius[0]) ** 2 * d1 ** 2 ) / ( (radius[0]) ** 2 ) ) * ratio

		"""
		Offset the center of the node properly, this time based on the given offset angle.
		Calculate the angle (in degrees) from the rightmost intersection to the leftmost intersection.
		Use it to calculate the x and y coordinates of the points of the looped edge.
		"""
		center = ( position[0] + radius[0] * math.cos(offset_angle),
				   position[1] + radius[1] * math.sin(offset_angle) )
		angle = math.asin(-d2 / loop[1])
		angle = math.floor(math.degrees(angle))
		x = [ center[0] + loop[0] * math.cos(math.pi * (i / 180 - 1 / 2) + offset_angle) for i in range(angle, - angle + 180) ]
		y = [ center[1] + loop[1] * math.sin(math.pi * (i / 180 - 1 / 2) + offset_angle) for i in range(angle, - angle + 180) ]

		"""
		Remove some style attributes that belong to arrows, not edges.
		"""
		edge_style = dict(kwargs)
		edge_style.pop('headwidth', None)
		edge_style.pop('headlength', None)
		edge_style['linewidth'] = edge_style.get('linewidth', 1) * 2
		edge = self.drawable.plot(x, y, zorder=-1, **edge_style)

		"""
		If the arrow is directed, calculate its position.
		The arrow points is set to always point downwards.
		"""
		if directed:
			arrowprops = dict(kwargs)
			if 'headwidth' in arrowprops:
				arrowprops['headwidth'] = arrowprops.get('headwidth') * 0.75
			if 'headlength' in arrowprops:
				arrowprops['headlength'] = arrowprops.get('headwidth') * 0.75
			xy = ( x[-1], y[-1] )
			xytext = ( x[-2], y[-2] )
			arrow = self.drawable.axes.annotate('', xy=xy, xytext=xytext,
												zorder=-1, arrowprops=arrowprops)


		return ( edge, arrow ) if directed else ( edge, )

	def _draw_node_labels(self, nodes, label_style, *args, **kwargs):
		"""
		Draw labels for the nodes.
		A label is drawn if the edge has a `label` attribute.

		Any additional arguments and keyword arguments are passed on to the legend drawing functions.

		:param nodes: The list of nodes in the graph.
		:type nodes: :class:`networkx.classes.reportviews.NodeView`
		:param label_style: The style of the label.
		:type label_style: dict
		"""

		for node in nodes:
			"""
			Go through each node and look for the label.
			The drawn label depends on the type of graph.
			Once a label is drawn, it is added to a list of drawn labels so it is not drawn again.
			"""
			if 'label' in nodes[node]:
				label = nodes[node]['label']

				default_style = dict(**kwargs)
				default_style.update(nodes[node].get('style', { }))

				"""
				The y-axis change when drawing points.
				Therefore save the y-limit and re-set it after drawing.
				"""
				ylim = self.drawable.axes.get_ylim()
				self.drawable.legend.draw_point(label, label_style=label_style,
												*args, **default_style)
				self.drawable.axes.set_ylim(ylim)

	def _draw_edge_labels(self, edges, directed, label_style, *args, **kwargs):
		"""
		Draw labels for the edges.
		A label is drawn if the edge has a `label` attribute.

		Any additional arguments and keyword arguments are passed on to the legend drawing functions.

		:param edges: The list of edges in the graph.
		:type edges: list of tuple
		:param directed: A boolean indicating whether the graph is directed or not.
		:type directed: bool
		:param label_style: The style of the label.
		:type label_style: dict
		"""

		for edge in edges:
			"""
			Go through each edge and look for the label.
			The drawn label depends on the type of graph.
			Once a label is drawn, it is added to a list of drawn labels so it is not drawn again.
			"""
			if 'label' in edges[edge]:
				label = edges[edge]['label']

				default_style = dict(**kwargs)
				default_style.update(edges[edge].get('style', { }))
				if directed:
					self.drawable.legend.draw_arrow(label, label_style=label_style,
													*args, **default_style)
				else:
					self.drawable.legend.draw_line(label, label_style=label_style,
													*args, **default_style)

	def _get_distance(self, u, v):
		"""
		Get the distance between the two given nodes.

		:param u: The source node's position as a tuple.
		:type u: tuple
		:param v: The target node's position as a tuple.
		:type v: tuple

		:return: The distance between the two nodes.
		:rtype: float
		"""

		diff = [ v[0] - u[0], v[1] - u[1] ]
		return math.sqrt(diff[0] ** 2 + diff[1] ** 2)

	def _get_direction(self, u, v):
		"""
		Get the direction between the two given nodes.
		This is the normalized difference between the nodes' positions.

		:param u: The source node's position as a tuple.
		:type u: tuple
		:param v: The target node's position as a tuple.
		:type v: tuple

		:return: The direction between the two nodes as a tuple.
		:rtype: tuple
		"""

		diff = [ v[0] - u[0], v[1] - u[1] ]
		distance = self._get_distance(u, v)
		if distance:
			return ( diff[0] / distance, diff[1] / distance )

		return (0, 0)

	def _get_angle(self, u, v):
		"""
		Get the angle between the source and target nodes.
		This angle is based on the atan2 function.

		:param u: The source node's position as a tuple.
		:type u: tuple
		:param v: The target node's position as a tuple.
		:type v: tuple

		:return: The angle between the source and target nodes in radians.
		:rtype: float
		"""

		return math.atan2(v[1], v[0]) - math.atan2(u[1], u[0])

	def _get_elevation(self, u, v):
		"""
		Get the angle of elevation from the source node to the target node.
		The angle of elevation considers the aspect ratio.

		:param u: The source node's position as a tuple.
		:type u: tuple
		:param v: The target node's position as a tuple.
		:type v: tuple

		:return: The angle of elevation between the source and target nodes in radians.
		:rtype: float
		"""

		if (u[0] == v[0] and u[1] == v[1]):
			return 0

		xdiff = v[0] - u[0]
		if xdiff == 0:
			return math.pi / 2.

		ratio = util.get_aspect(self.drawable.axes)
		ydiff = (v[1] - u[1]) * ratio

		return math.atan(ydiff / xdiff)

	def _get_radius(self, node, s):
		"""
		Get the radius of the given node in terms of the data axes.
		By default, the radius `s` is 100, but it can be overriden using the node's `style` attribute.

		.. note::

			The square root of the radius is taken because `the radius is originally squared <https://matplotlib.org/3.2.0/api/_as_gen/matplotlib.pyplot.scatter.html>`_.

		:param node: The node whose radius will be calculated.
		:type node: dict
		:param s: The default radius of the node.
				  It may be overwritten with the node's own radius.
		:type s: float

		:return: The radius of the node in terms of the data axes.
				 Two radii are provided: the x- and y-radii.
				 This is because scatter points always look like circles, even when the display or data ratios are not equal.
				 Whn the display or data ratios are not equal, the point is actually an ellipse so that it still looks like a circle.
		:rtype: tuple
		"""

		origin = self.drawable.axes.transData.inverted().transform((0, 0))

		x = (self.drawable.axes.transData.inverted().transform((s ** 0.5, 0))[0] - origin[0])/2.
		y = (self.drawable.axes.transData.inverted().transform((0, s ** 0.5))[1] - origin[1])/2.
		return (x, y)
