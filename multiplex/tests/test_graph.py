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

