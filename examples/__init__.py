"""
Functions used to draw the showcase.
"""

import networkx as nx
import nltk
import numpy as np

def draw_timeseries(viz):
	"""
	Draw a timeseries on the provided visualization.

	:param viz: The visualization where the timeseries will be drawn.
	:type viz: :class:`multiple.drawable.Drawable`
	"""

	viz.set_xlim(-0.5, 10.5)
	viz.set_ylim(0.2, 0.8)
	viz.set_xlabel('Time')
	viz.set_ylabel('Value')

	for i, label in zip(range(2), [ 'A', 'B' ]):
		np.random.seed(i)
		x = range(11)
		y = np.linspace(0.4, 0.7 - 0.15 * i, num=11) + np.random.normal(0, 0.03, 11)
		viz.draw_time_series(x, y,
							 color=('C0' if i == 1 else 'C1'), label=label, with_legend=True)

	viz.set_title('Time series', loc='left')
	viz.set_caption('A simple time series.')

def draw_text(viz, dark=False):
	"""
	Draw annotated text on the provided visualization.

	:param viz: The visualization where the text annotation will be drawn.
	:type viz: :class:`multiple.drawable.Drawable`
	:param dark: A boolean indicating whether the theme is dark or not.
				 This influences the highlight color.
	:type dark: boolean
	"""

	paragraph = "Anthony Lopes is a Portuguese professional footballer who plays for \
Olympique Lyonnais as a goalkeeper. He came through the youth ranks at Lyon, being \
called to the first team in 2011 and making his debut the following year. \
He made over 300 appearances for the club, including the 2014 Coupe de la Ligue Final. \
Born in France, Lopes represented Portugal internationally, \
totalling 36 caps at youth level including 11 for the under-21 team. \
He made his senior debut for the country in March 2015, \
and was chosen for Euro 2016 and the 2018 World Cup."
	tokens = nltk.word_tokenize(paragraph)
	pos_tags = nltk.pos_tag(tokens)
	chunks = [ entity for entity in nltk.ne_chunk(pos_tags, binary=True) ]

	tokens = []
	for chunk in chunks:
		if type(chunk) == nltk.tree.Tree:
			for entity_chunk in chunk:
				entity, _ = entity_chunk
				tokens.append({
					'style': {
						'facecolor': 'C1',
						'color': 'C0' if dark else 'C4',
					},
					'text': entity
				})
		else:
			token, _ = chunk
			tokens.append(token)

	viz.draw_text_annotation(tokens, align='justify', alpha=0.8, fontfamily='serif', lpad=0.05, rpad=0.05, tpad=0.1)
	viz.axes.set_ylim(-0.55, 0.05)
	viz.set_title('Text annotation', loc='left')
	viz.set_caption('A simple text annotation visualization.')

def draw_graph(viz, node_style=None, edge_style=None, name_style=None, highlight_node_style=None):
	"""
	Draw a network graph on the given visualization.

	:param viz: The visualization where the text annotation will be drawn.
	:type viz: :class:`multiple.drawable.Drawable`
	:param node_style: The style of the nodes.
	:type node_style: None or dict
	:param edge_style: The style of the edges.
	:type edge_style: None or dict
	:param name_style: The style of the names.
	:type name_style: None or dict
	:param highlight_node_style: The style of the highlight nodes.
	:type highlight_node_style: None or dict
	"""

	E = [ ('A', 'A'), ('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A') ]
	G = nx.from_edgelist(E, nx.DiGraph)
	G.edges[('A', 'A')]['name'] = 'A-A'
	G.edges[('A', 'B')]['name'] = 'A-B'
	G.edges[('B', 'C')]['name'] = 'B-C'
	G.edges[('C', 'D')]['name'] = 'C-D'
	G.edges[('D', 'A')]['name'] = 'D-A'
	for node in G.nodes:
		G.nodes[node]['label'] = 'Node'
	for edge in G.edges:
		G.edges[edge]['label'] = 'Edge'
	G.nodes['B']['style'] = { 'edgecolor': 'C1', 'linewidth': 5, 's': 2000 }
	G.nodes['B']['style'].update(highlight_node_style or { })
	G.nodes['B']['label'] = 'Special Node'
	positions = { 'A': (-1, 0), 'B': (0, 1), 'C': (1, 0), 'D': (0, -1) }
	default_node_style = { 's': 1000, 'color': 'C0', 'alpha': 1 }
	default_node_style.update(node_style or { })
	default_edge_style = { 'color': 'C0', 'linewidth': 2.5 }
	default_edge_style.update(edge_style or { })
	default_name_style = { 'facecolor': 'C4', 'color': 'C0', 'fontweight': 900 }
	default_name_style.update(name_style or { })
	viz.draw_graph(G, positions=positions,
				   node_style=default_node_style, edge_style=default_edge_style,
				   name_style=default_name_style, seed=24)
	viz.set_title('Network graph', loc='left')
	viz.set_caption('A simple network graph visualization.')

def draw_bar_100(viz, bar_style=None):
	"""
	Draw a 100% bar chart on the given visualization.

	:param viz: The visualization where the text annotation will be drawn.
	:type viz: :class:`multiple.drawable.Drawable`
	:param bar_style: The style of the bars.
	:type bar_style: None or dict
	"""

	np.random.seed(9)
	for i in range(1, 20):
		values = list(np.random.normal(30, 5, 5))
		highest = max(values)
		index = values.index(highest)
		default_bar_style = { 'color': 'C0', 'alpha': 0.5 }
		default_bar_style.update(bar_style or { })
		values[index] = { 'value': values[index], 'style': { 'color': 'C1', 'alpha': 1 } }
		viz.draw_bar_100(values, f"Bar { i }", **default_bar_style)

	viz.set_xlabel('Percentage of total')
	viz.set_title('100% bar chart', loc='left')
	viz.set_caption('A simple 100% bar chart visualization.')
