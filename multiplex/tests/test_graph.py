"""
Unit tests for the :class:`~graph.graph.Graph` class.
"""

import matplotlib.pyplot as plt
import networkx as nx
import os
import sys

path = os.path.join(os.path.dirname(__file__), '..')
if path not in sys.path:
	sys.path.insert(1, path)

from .test import MultiplexTest
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
		self.assertFalse(edges)

	@MultiplexTest.temporary_plot
	def test_draw_graph_with_single_edge(self):
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
		self.assertEqual(nodes[0].get_offsets()[0][0], edges[0].get_xdata()[0])
		self.assertEqual(nodes[0].get_offsets()[0][1], edges[0].get_ydata()[0])
		self.assertEqual(nodes[2].get_offsets()[0][0], edges[0].get_xdata()[1])
		self.assertEqual(nodes[2].get_offsets()[0][1], edges[0].get_ydata()[1])

	@MultiplexTest.temporary_plot
	def test_draw_graph_with_multiple_edges(self):
		"""
		Test that when drawing a graph with one edge, the correct nodes are connected.
		"""

		E = [ ('A', 'C'), ('B', 'A') ]
		G = nx.from_edgelist(E)

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		nodes, node_names, edges = viz.draw_graph(G)
		self.assertEqual(3, len(nodes))
		self.assertEqual(2, len(edges))
		indices = [ (0, 1), (0, 2) ]
		for i, edge in enumerate(edges):
			source, target = indices[i]
			self.assertEqual(nodes[source].get_offsets()[0][0], edge.get_xdata()[0])
			self.assertEqual(nodes[source].get_offsets()[0][1], edge.get_ydata()[0])
			self.assertEqual(nodes[target].get_offsets()[0][0], edge.get_xdata()[1])
			self.assertEqual(nodes[target].get_offsets()[0][1], edge.get_ydata()[1])

	@MultiplexTest.temporary_plot
	def test_draw_graph_edge_style(self):
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

		self.assertTrue(all(edge.get_alpha() == edge_style['alpha'] for edge in edges))
		self.assertTrue(all(edge.get_color() == edge_style['color'] for edge in edges))
		self.assertTrue(all(edge.get_linewidth() == edge_style['linewidth'] for edge in edges))

	@MultiplexTest.temporary_plot
	def test_draw_graph_override_edge_style(self):
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

		self.assertEqual(1, edges[0].get_alpha())
		self.assertEqual(0.5, edges[1].get_alpha())
		self.assertEqual(0.5, edges[2].get_alpha())

	@MultiplexTest.temporary_plot
	def test_draw_graph_inherit_edge_style(self):
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

		self.assertEqual(1, edges[0].get_alpha())
		self.assertEqual(0.5, edges[1].get_alpha())
		self.assertEqual(0.5, edges[2].get_alpha())
		self.assertTrue(all( edge.get_color() == '#FF0000' for edge in edges ))

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
		self.assertEqual(2, len(edges))
		self.assertFalse(node_names)

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
		self.assertEqual('A', str(node_names[0]))

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
		self.assertTrue(all(name.lines[0][0].get_color() == name_style['color'] for name in node_names))

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
		self.assertEqual('#BBCC00', node_names[0].lines[0][0].get_color())
		self.assertEqual(name_style['color'], node_names[1].lines[0][0].get_color())

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
		self.assertTrue(all(name.lines[0][0].get_color() == name_style['color'] for name in node_names))
		self.assertEqual(0.2, node_names[0].lines[0][0].get_bbox_patch().get_facecolor()[0])
		self.assertEqual(round(0.1 + 1/30., 10), round(node_names[0].lines[0][0].get_bbox_patch().get_facecolor()[1], 10))
		self.assertEqual(1, node_names[0].lines[0][0].get_bbox_patch().get_facecolor()[2])
		self.assertEqual(0.8, node_names[1].lines[0][0].get_bbox_patch().get_facecolor()[0])
		self.assertEqual(0, node_names[1].lines[0][0].get_bbox_patch().get_facecolor()[1])
		self.assertEqual(round(0.7 + 1/30., 10), round(node_names[1].lines[0][0].get_bbox_patch().get_facecolor()[2], 10))
