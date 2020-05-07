"""
Unit tests for the :class:`~graph.graph.Graph` class.
"""

import math
import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import os
import sys

path = os.path.join(os.path.dirname(__file__), '..')
if path not in sys.path:
	sys.path.insert(1, path)

from .test import MultiplexTest
from graph.graph import Graph
import drawable
import util

class TestGraph(MultiplexTest):
	"""
	Unit tests for the :class:`~graph.graph.Graph` class.
	"""

	@MultiplexTest.temporary_plot
	def test_draw_graph_empty(self):
		"""
		Test that when plotting an empty graph, an empty set of nodes and edges are returned.
		"""

		G = nx.Graph()

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		nodes, node_names, edges = viz.draw_graph(G)
		self.assertFalse(len(nodes))
		self.assertFalse(node_names)
		self.assertFalse(edges)

	@MultiplexTest.temporary_plot
	def test_draw_graph_single_node(self):
		"""
		Test drawing a graph with one node.
		"""

		G = nx.Graph()
		G.add_node(1)

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		nodes, node_names, edges = viz.draw_graph(G)
		self.assertEqual(1, len(nodes))
		self.assertFalse(node_names)
		self.assertFalse(edges)

	@MultiplexTest.temporary_plot
	def test_draw_graph_without_edges(self):
		"""
		Test drawing a graph with multiple nodes, but no edges.
		"""

		G = nx.Graph()
		G.add_node(1)
		G.add_node(2)

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		nodes, node_names, edges = viz.draw_graph(G)
		self.assertEqual(2, len(nodes))
		self.assertFalse(node_names)
		self.assertFalse(edges)

	@MultiplexTest.temporary_plot
	def test_draw_graph_directed_edge_type(self):
		"""
		Test that when plotting an undirected graph, the edges are drawn as lines.
		"""

		E = [ ('A', 'C'), ('B', 'A') ]
		G = nx.from_edgelist(E)

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		edge_style = { 'alpha': 0.5, 'color': '#ff0000', 'linewidth': 0.5 }
		nodes, node_names, edges = viz.draw_graph(G, edge_style=edge_style)
		self.assertEqual(3, len(nodes))
		self.assertEqual(2, len(edges))
		self.assertTrue(all(type(edge) == matplotlib.lines.Line2D for edge in edges.values()))

	@MultiplexTest.temporary_plot
	def test_draw_graph_undirected_with_single_edge(self):
		"""
		Test that when drawing a graph with one edge, the correct nodes are connected.
		"""

		G = nx.Graph()
		G.add_node(1)
		G.add_node(2)
		G.add_node(3)
		G.add_edge(1, 3)

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		nodes, node_names, edges = viz.draw_graph(G)
		self.assertEqual(3, len(nodes))
		self.assertEqual(1, len(edges))
		self.assertEqual(nodes[1].get_offsets()[0][0], edges[(1, 3)].get_xdata()[0])
		self.assertEqual(nodes[1].get_offsets()[0][1], edges[(1, 3)].get_ydata()[0])
		self.assertEqual(nodes[3].get_offsets()[0][0], edges[(1, 3)].get_xdata()[1])
		self.assertEqual(nodes[3].get_offsets()[0][1], edges[(1, 3)].get_ydata()[1])

	@MultiplexTest.temporary_plot
	def test_draw_graph_undirected_with_multiple_edges(self):
		"""
		Test that when drawing a graph with one edge, the correct nodes are connected.
		"""

		E = [ ('A', 'C'), ('B', 'A') ]
		G = nx.from_edgelist(E)

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		nodes, node_names, edges = viz.draw_graph(G)
		self.assertEqual(3, len(nodes))
		self.assertEqual(2, len(edges))
		for (source, target), edge in edges.items():
			self.assertEqual(nodes[source].get_offsets()[0][0], edge.get_xdata()[0])
			self.assertEqual(nodes[source].get_offsets()[0][1], edge.get_ydata()[0])
			self.assertEqual(nodes[target].get_offsets()[0][0], edge.get_xdata()[1])
			self.assertEqual(nodes[target].get_offsets()[0][1], edge.get_ydata()[1])

	@MultiplexTest.temporary_plot
	def test_draw_graph_undirected_edge_style(self):
		"""
		Test that when providing the edge style, it is used when creating edges.
		"""

		E = [ ('A', 'C'), ('B', 'A') ]
		G = nx.from_edgelist(E)

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		edge_style = { 'alpha': 0.5, 'color': '#ff0000', 'linewidth': 0.5 }
		nodes, node_names, edges = viz.draw_graph(G, edge_style=edge_style)
		self.assertEqual(3, len(nodes))
		self.assertEqual(2, len(edges))

		self.assertTrue(all(edge.get_alpha() == edge_style['alpha'] for edge in edges.values()))
		self.assertTrue(all(edge.get_color() == edge_style['color'] for edge in edges.values()))
		self.assertTrue(all(edge.get_linewidth() == edge_style['linewidth'] for edge in edges.values()))

	@MultiplexTest.temporary_plot
	def test_draw_graph_undirected_override_edge_style(self):
		"""
		Test that when providing a custom style for an edge, it overwrites the default style.
		"""

		E = [ ('A', 'C'), ('B', 'A'), ('C', 'B') ]
		G = nx.from_edgelist(E)

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		edge_style = { 'alpha': 0.5 }
		G.edges[('C', 'A')]['style'] = { 'alpha': 1 }
		nodes, node_names, edges = viz.draw_graph(G, edge_style=edge_style)
		self.assertEqual(3, len(nodes))
		self.assertEqual(3, len(edges))

		self.assertEqual(1, edges[('A', 'C')].get_alpha())
		self.assertEqual(0.5, edges[('A', 'B')].get_alpha())
		self.assertEqual(0.5, edges[('C', 'B')].get_alpha())

	@MultiplexTest.temporary_plot
	def test_draw_graph_undirected_inherit_edge_style(self):
		"""
		Test that when providing a custom style for an edge, it overwrites only the same parameters in the default style.
		"""

		E = [ ('A', 'C'), ('B', 'A'), ('C', 'B') ]
		G = nx.from_edgelist(E)

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		edge_style = { 'alpha': 0.5, 'color': '#FF0000' }
		G.edges[('C', 'A')]['style'] = { 'alpha': 1 }
		nodes, node_names, edges = viz.draw_graph(G, edge_style=edge_style)
		self.assertEqual(3, len(nodes))
		self.assertEqual(3, len(edges))

		self.assertEqual(1, edges[('A', 'C')].get_alpha())
		self.assertEqual(0.5, edges[('A', 'B')].get_alpha())
		self.assertEqual(0.5, edges[('C', 'B')].get_alpha())
		self.assertTrue(all( edge.get_color() == '#FF0000' for edge in edges.values() ))

	@MultiplexTest.temporary_plot
	def test_draw_graph_directed_edge_type(self):
		"""
		Test that when plotting a directed graph, the edges are drawn as text annotations.
		"""

		E = [ ('A', 'C'), ('B', 'A') ]
		G = nx.from_edgelist(E, create_using=nx.DiGraph)

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		edge_style = { 'alpha': 0.5, 'color': '#ff0000', 'linewidth': 0.5 }
		nodes, node_names, edges = viz.draw_graph(G, edge_style=edge_style)
		self.assertEqual(3, len(nodes))
		self.assertEqual(2, len(edges))
		self.assertTrue(all(type(edge) == matplotlib.text.Annotation for edge in edges.values()))

	@MultiplexTest.temporary_plot
	def test_draw_graph_directed_edge_style(self):
		"""
		Test that when providing the edge style, it is used when creating edges.
		"""

		E = [ ('A', 'C'), ('B', 'A') ]
		G = nx.from_edgelist(E, create_using=nx.DiGraph)

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		edge_style = { 'alpha': 0.5, 'color': '#ff0000', 'linewidth': 0.5 }
		nodes, node_names, edges = viz.draw_graph(G, edge_style=edge_style)
		self.assertEqual(3, len(nodes))
		self.assertEqual(2, len(edges))

		self.assertTrue(all(edge.arrow_patch.get_edgecolor()[3] == edge_style['alpha'] for edge in edges.values()))
		self.assertTrue(all(edge.arrow_patch.get_edgecolor()[:3] == (1, 0, 0) for edge in edges.values()))
		self.assertTrue(all(edge.arrow_patch.get_linewidth() == edge_style['linewidth'] for edge in edges.values()))

	@MultiplexTest.temporary_plot
	def test_draw_graph_directed_override_edge_style(self):
		"""
		Test that when providing a custom style for an edge, it overwrites the default style.
		"""

		E = [ ('A', 'C'), ('B', 'A'), ('C', 'B') ]
		G = nx.from_edgelist(E, create_using=nx.DiGraph)

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		edge_style = { 'alpha': 0.5 }
		G.edges[('A', 'C')]['style'] = { 'alpha': 1 }
		nodes, node_names, edges = viz.draw_graph(G, edge_style=edge_style)
		self.assertEqual(3, len(nodes))
		self.assertEqual(3, len(edges))

		self.assertEqual(1, edges[('A', 'C')].arrow_patch.get_edgecolor()[3])
		self.assertEqual(0.5, edges[('B', 'A')].arrow_patch.get_edgecolor()[3])
		self.assertEqual(0.5, edges[('C', 'B')].arrow_patch.get_edgecolor()[3])

	@MultiplexTest.temporary_plot
	def test_draw_graph_directed_inherit_edge_style(self):
		"""
		Test that when providing a custom style for an edge, it overwrites only the same parameters in the default style.
		"""

		E = [ ('A', 'C'), ('B', 'A'), ('C', 'B') ]
		G = nx.from_edgelist(E, create_using=nx.DiGraph)

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		edge_style = { 'alpha': 0.5, 'color': '#FF0000' }
		G.edges[('A', 'C')]['style'] = { 'alpha': 1 }
		nodes, node_names, edges = viz.draw_graph(G, edge_style=edge_style)
		self.assertEqual(3, len(nodes))
		self.assertEqual(3, len(edges))

		self.assertEqual(1, edges[('A', 'C')].arrow_patch.get_edgecolor()[3])
		self.assertEqual(0.5, edges[('B', 'A')].arrow_patch.get_edgecolor()[3])
		self.assertEqual(0.5, edges[('C', 'B')].arrow_patch.get_edgecolor()[3])
		self.assertTrue(all( edge.arrow_patch.get_edgecolor()[:3] == (1, 0, 0) for edge in edges.values() ))

	@MultiplexTest.temporary_plot
	def test_draw_graph_no_node_names(self):
		"""
		Test that when no nodes have names, no names are drawn.
		"""

		E = [ ('A', 'C'), ('B', 'A') ]
		G = nx.from_edgelist(E)

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		nodes, node_names, edges = viz.draw_graph(G)
		self.assertEqual(3, len(nodes))
		self.assertFalse(node_names)
		self.assertEqual(2, len(edges))

	@MultiplexTest.temporary_plot
	def test_draw_graph_node_names(self):
		"""
		Test that when a node has a name, it is drawn.
		"""

		E = [ ('A', 'C'), ('B', 'A') ]
		G = nx.from_edgelist(E)
		G.nodes['A']['name'] = 'A'

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		nodes, node_names, edges = viz.draw_graph(G)
		self.assertEqual(3, len(nodes))
		self.assertEqual(2, len(edges))
		self.assertEqual(1, len(node_names))
		self.assertEqual('A', str(node_names['A']).strip())

	@MultiplexTest.temporary_plot
	def test_draw_graph_node_name_style(self):
		"""
		Test that when providing the node name style, it is used when creating annotations.
		"""

		E = [ ('A', 'C'), ('B', 'A') ]
		G = nx.from_edgelist(E)
		G.nodes['A']['name'] = 'A'
		G.nodes['B']['name'] = 'B'

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		name_style = { 'color': '#CC00BB' }
		nodes, node_names, edges = viz.draw_graph(G, name_style=name_style)
		self.assertEqual(3, len(nodes))
		self.assertEqual(2, len(edges))
		self.assertEqual(2, len(node_names))
		self.assertTrue(all(name.lines[-1][0].get_color() == name_style['color'] for name in node_names.values()))

	@MultiplexTest.temporary_plot
	def test_draw_graph_override_node_name_style(self):
		"""
		Test that when providing a custom style for an edge, it overwrites the default style.
		"""

		E = [ ('A', 'C'), ('B', 'A') ]
		G = nx.from_edgelist(E)
		G.nodes['A']['name'] = 'A'
		G.nodes['A']['name_style'] = { 'color': '#BBCC00' }
		G.nodes['B']['name'] = 'B'

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		name_style = { 'color': '#CC00BB' }
		nodes, node_names, edges = viz.draw_graph(G, name_style=name_style)
		self.assertEqual(3, len(nodes))
		self.assertEqual(2, len(edges))
		self.assertEqual(2, len(node_names))
		self.assertEqual('#BBCC00', node_names['A'].lines[-1][0].get_color())
		self.assertEqual(name_style['color'], node_names['B'].lines[-1][0].get_color())

	@MultiplexTest.temporary_plot
	def test_draw_graph_inherit_node_name_style(self):
		"""
		Test that when providing a custom style for an edge, it overwrites only the same parameters in the default style.
		"""

		E = [ ('A', 'C'), ('B', 'A'), ('C', 'B') ]
		G = nx.from_edgelist(E)
		G.nodes['A']['name'] = 'A'
		G.nodes['A']['name_style'] = { 'facecolor': '#3322FF' }
		G.nodes['B']['name'] = 'B'

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		name_style = { 'facecolor': '#CC00BB', 'color': '#FFFFFF' }
		nodes, node_names, edges = viz.draw_graph(G, name_style=name_style)
		self.assertEqual(3, len(nodes))
		self.assertEqual(3, len(edges))
		self.assertEqual(2, len(node_names))
		self.assertTrue(all(name.lines[-1][0].get_color() == name_style['color'] for name in node_names.values()))

		self.assertEqual(0.2, node_names['A'].lines[-1][0].get_bbox_patch().get_facecolor()[0])
		self.assertEqual(round(0.1 + 1/30., 10),
						 round(node_names['A'].lines[-1][0].get_bbox_patch().get_facecolor()[1], 10))
		self.assertEqual(1, node_names['A'].lines[-1][0].get_bbox_patch().get_facecolor()[2])

		self.assertEqual(0.8, node_names['B'].lines[-1][0].get_bbox_patch().get_facecolor()[0])
		self.assertEqual(0, node_names['B'].lines[-1][0].get_bbox_patch().get_facecolor()[1])
		self.assertEqual(round(0.7 + 1/30., 10),
						 round(node_names['B'].lines[-1][0].get_bbox_patch().get_facecolor()[2], 10))

	@MultiplexTest.temporary_plot
	def test_draw_graph_loop_undirected(self):
		"""
		Test that when drawing a looped undirected edge, only a line is returned.
		"""

		E = [ ('A', 'A') ]
		G = nx.from_edgelist(E)

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		nodes, node_names, edges = viz.draw_graph(G)
		self.assertEqual(1, len(edges))
		self.assertEqual(1, len(edges[('A', 'A')]))
		self.assertEqual(matplotlib.lines.Line2D, type(edges[('A', 'A')][0][0]))

	@MultiplexTest.temporary_plot
	def test_draw_graph_loop_directed(self):
		"""
		Test that when drawing a looped directed edge, a line and arrow are returned.
		"""

		E = [ ('A', 'A') ]
		G = nx.from_edgelist(E, create_using=nx.DiGraph)

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		nodes, node_names, edges = viz.draw_graph(G)
		self.assertEqual(1, len(edges))
		self.assertEqual(2, len(edges[('A', 'A')]))
		self.assertEqual(matplotlib.lines.Line2D, type(edges[('A', 'A')][0][0]))
		self.assertEqual(matplotlib.text.Annotation, type(edges[('A', 'A')][1]))

	@MultiplexTest.temporary_plot
	def test_get_distance_same(self):
		"""
		Test that when getting the distance between the same point, 0 is returned.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		graph = Graph(viz)
		self.assertEqual(0, round(graph._get_distance((1, 1), (1, 1)), 5))

	@MultiplexTest.temporary_plot
	def test_get_distance_same_x(self):
		"""
		Test that when getting the distance between two points with the same x-coordinate, the y-distance is returned.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		graph = Graph(viz)
		self.assertEqual(1, round(graph._get_distance((0, 0), (0, 1)), 5))

	@MultiplexTest.temporary_plot
	def test_get_distance_same_y(self):
		"""
		Test that when getting the distance between two points with the same y-coordinate, the x-distance is returned.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		graph = Graph(viz)
		self.assertEqual(1, round(graph._get_distance((0, 0), (1, 0)), 5))

	@MultiplexTest.temporary_plot
	def test_get_distance_positive(self):
		"""
		Test getting the distance between two points.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		graph = Graph(viz)
		self.assertEqual(round(math.sqrt(2), 5), round(graph._get_distance((0, 0), (1, 1)), 5))
		self.assertEqual(round(math.sqrt(5), 5), round(graph._get_distance((0, 0), (2, 1)), 5))
		self.assertEqual(1, round(graph._get_distance((1, 2), (1, 1)), 5))
		self.assertEqual(round(math.sqrt(2), 5), round(graph._get_distance((3, 2), (2, 1)), 5))

	@MultiplexTest.temporary_plot
	def test_get_distance_negative(self):
		"""
		Test getting the distance between two points.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		graph = Graph(viz)
		self.assertEqual(round(math.sqrt(2), 5), round(graph._get_distance((0, 0), (-1, -1)), 5))
		self.assertEqual(round(math.sqrt(5), 5), round(graph._get_distance((0, 0), (-2, -1)), 5))
		self.assertEqual(1, round(graph._get_distance((-1, -2), (-1, -1)), 5))
		self.assertEqual(round(math.sqrt(2), 5), round(graph._get_distance((-3, -2), (-2, -1)), 5))

	@MultiplexTest.temporary_plot
	def test_get_distance_symmetric(self):
		"""
		Test that the distance between two points is symmetric.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		graph = Graph(viz)
		self.assertEqual(round(graph._get_distance((-1, -1), (0, 0)), 5),
						 round(graph._get_distance((0, 0), (-1, -1)), 5))
		self.assertEqual(round(graph._get_distance((-2, -1), (0, 0)), 5),
						 round(graph._get_distance((0, 0), (-2, -1)), 5))

	@MultiplexTest.temporary_plot
	def test_get_angle_same(self):
		"""
		Test that when the same points are given to calculate the angle, an angle of 0 is returned.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		graph = Graph(viz)
		self.assertEqual(0, round(graph._get_angle((1, 1), (1, 1)), 5))

	@MultiplexTest.temporary_plot
	def test_get_angle(self):
		"""
		Test getting the angle between two points.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		graph = Graph(viz)
		self.assertEqual(round(math.pi / 4., 5), round(graph._get_angle((1, 0), (1, 1)), 5))
		self.assertEqual(round(math.pi / 2., 5), round(graph._get_angle((1, 0), (0, 1)), 5))
		self.assertEqual(round(3 * math.pi / 4., 5), round(graph._get_angle((1, 0), (-1, 1)), 5))
		self.assertEqual(round(math.pi, 5), round(graph._get_angle((1, 0), (-1, 0)), 5))
		self.assertEqual(round(- 3 * math.pi / 4, 5), round(graph._get_angle((1, 0), (-1, -1)), 5))
		self.assertEqual(round(- math.pi / 2., 5), round(graph._get_angle((1, 0), (0, -1)), 5))
		self.assertEqual(round(- math.pi / 4., 5), round(graph._get_angle((1, 0), (1, -1)), 5))

	@MultiplexTest.temporary_plot
	def test_get_angle_different_dimensions(self):
		"""
		Test that when getting the angle between two points, the magnitude is normalized.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		graph = Graph(viz)
		self.assertEqual(round(math.pi / 4., 5), round(graph._get_angle((1, 0), (2, 2)), 5))
		self.assertEqual(round(math.pi / 2., 5), round(graph._get_angle((2, 0), (0, 1)), 5))
		self.assertEqual(round(3 * math.pi / 4., 5), round(graph._get_angle((2, 0), (-1, 1)), 5))
		self.assertEqual(round(math.pi, 5), round(graph._get_angle((1, 0), (-2, 0)), 5))
		self.assertEqual(round(- 3 * math.pi / 4, 5), round(graph._get_angle((2, 0), (-2, -2)), 5))
		self.assertEqual(round(- math.pi / 2., 5), round(graph._get_angle((2, 0), (0, -1)), 5))
		self.assertEqual(round(- math.pi / 4., 5), round(graph._get_angle((1, 0), (2, -2)), 5))

	@MultiplexTest.temporary_plot
	def test_get_radius_same_aspect_ratio(self):
		"""
		Test that when getting the radius, the correct radii are returned.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))

		graph = Graph(viz)
		point = viz.scatter(0, 0, s=1000)
		bb = util.get_bb(viz.figure, viz.axis, point)
		self.assertEqual(round(bb.width/2, 10), round(graph._get_radius(point, s=1000)[0], 10))
		self.assertEqual(round(bb.height/2, 10), round(graph._get_radius(point, s=1000)[1], 10))

	@MultiplexTest.temporary_plot
	def test_get_radius_unequal_display_ratio(self):
		"""
		Test that when getting the radius, the correct radii are used even if the display ratio is not equal.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))

		graph = Graph(viz)
		point = viz.scatter(0, 0, s=1000)
		viz.set_xlim((-1, 1))
		viz.set_ylim((-1, 1))

		bb = util.get_bb(viz.figure, viz.axis, point)
		self.assertEqual(round(bb.width/2, 10), round(graph._get_radius(point, s=1000)[0], 10))
		self.assertEqual(round(bb.height/2, 10), round(graph._get_radius(point, s=1000)[1], 10))

		viz = drawable.Drawable(plt.figure(figsize=(5, 10)))

		graph = Graph(viz)
		point = viz.scatter(0, 0, s=1000)
		viz.set_xlim((-1, 1))
		viz.set_ylim((-1, 1))

		bb = util.get_bb(viz.figure, viz.axis, point)
		self.assertEqual(round(bb.width/2, 10), round(graph._get_radius(point, s=1000)[0], 10))
		self.assertEqual(round(bb.height/2, 10), round(graph._get_radius(point, s=1000)[1], 10))

	@MultiplexTest.temporary_plot
	def test_get_radius_unequal_data_ratio(self):
		"""
		Test that when getting the radius, the correct radii are used even if the data ratio is not equal.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))

		graph = Graph(viz)
		point = viz.scatter(0, 0, s=1000)
		viz.set_xlim((-2, 2))
		viz.set_ylim((-1, 1))

		bb = util.get_bb(viz.figure, viz.axis, point)
		self.assertEqual(round(bb.width/2, 10), round(graph._get_radius(point, s=1000)[0], 10))
		self.assertEqual(round(bb.height/2, 10), round(graph._get_radius(point, s=1000)[1], 10))

		viz.set_xlim((-1, 1))
		viz.set_ylim((-2, 2))

		bb = util.get_bb(viz.figure, viz.axis, point)
		self.assertEqual(round(bb.width/2, 10), round(graph._get_radius(point, s=1000)[0], 10))
		self.assertEqual(round(bb.height/2, 10), round(graph._get_radius(point, s=1000)[1], 10))
