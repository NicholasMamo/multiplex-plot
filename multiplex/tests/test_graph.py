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
		nodes, edges = viz.draw_graph(G)
		self.assertFalse(len(nodes.get_offsets()))
		self.assertFalse(edges)

	@MultiplexTest.temporary_plot
	def test_draw_graph_single_node(self):
		"""
		Test drawing a graph with one node.
		"""

		G = nx.Graph()
		G.add_node(1)

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		nodes, edges = viz.draw_graph(G)
		self.assertEqual(1, len(nodes.get_offsets()))
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
		nodes, edges = viz.draw_graph(G)
		self.assertEqual(2, len(nodes.get_offsets()))
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
		nodes, edges = viz.draw_graph(G)
		self.assertEqual(3, len(nodes.get_offsets()))
		self.assertEqual(1, len(edges))
		self.assertEqual(nodes.get_offsets()[0][0], edges[0].get_xdata()[0])
		self.assertEqual(nodes.get_offsets()[0][1], edges[0].get_ydata()[0])
		self.assertEqual(nodes.get_offsets()[2][0], edges[0].get_xdata()[1])
		self.assertEqual(nodes.get_offsets()[2][1], edges[0].get_ydata()[1])

	@MultiplexTest.temporary_plot
	def test_draw_graph_with_multiple_edges(self):
		"""
		Test that when drawing a graph with one edge, the correct nodes are connected.
		"""

		E = [ ('A', 'C'), ('B', 'A') ]
		G = nx.from_edgelist(E)

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		nodes, edges = viz.draw_graph(G)
		self.assertEqual(3, len(nodes.get_offsets()))
		self.assertEqual(2, len(edges))
		indices = [ (0, 1), (0, 2) ]
		for i, edge in enumerate(edges):
			source, target = indices[i]
			self.assertEqual(nodes.get_offsets()[source][0], edge.get_xdata()[0])
			self.assertEqual(nodes.get_offsets()[source][1], edge.get_ydata()[0])
			self.assertEqual(nodes.get_offsets()[target][0], edge.get_xdata()[1])
			self.assertEqual(nodes.get_offsets()[target][1], edge.get_ydata()[1])

	@MultiplexTest.temporary_plot
	def test_draw_graph_edge_style(self):
		"""
		Test that when providing the edge style, it is used when creating edges.
		"""

		E = [ ('A', 'C'), ('B', 'A') ]
		G = nx.from_edgelist(E)

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		edge_style = { 'alpha': 0.5, 'color': '#ff0000', 'linewidth': 0.5 }
		nodes, edges = viz.draw_graph(G, edge_style=edge_style)
		self.assertEqual(3, len(nodes.get_offsets()))
		self.assertEqual(2, len(edges))

		self.assertTrue(all(edge.get_alpha() == edge_style['alpha'] for edge in edges))
		self.assertTrue(all(edge.get_color() == edge_style['color'] for edge in edges))
		self.assertTrue(all(edge.get_linewidth() == edge_style['linewidth'] for edge in edges))
