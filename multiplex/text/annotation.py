"""
A class of visualization that allows text annotations.
The annotation class is mainly concerned with organizing text.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
import util

class TextAnnotation():
	"""
	A class of visualization that allows text annotations.
	The :class:`text.annotation.TextAnnotation` is mainly concered with organizing text.

	:ivar drawable: The axis where the text annotation visualization will be drawn.
	:vartype drawable: :class:`drawable.Drawable`
	"""

	def __init__(self, drawable):
		"""
		Initialize the text annotation with the figure and axis.
		The figure is used to get the renderer.
		The visualization is drawn on the given axis.

		:param drawable: The axis where the text annotation visualization will be drawn.
		:type drawable: :class:`drawable.Drawable`
		"""

		self.drawable = drawable

	def draw(self, data, *args, **kwargs):
		"""
		Draw the text annotation visualization.
		The method receives text as a list of tokens and draws them as text.

		:param data: The text data.
					 The visualization expects a list of tokens.
		:type data: list of str
		"""

		axis = self.drawable.axis
		axis.axis('off')
		axis.invert_yaxis()

		self._draw_tokens(data, *args, **kwargs)

	def _draw_tokens(self, tokens, word_spacing=0.005, *args, **kwargs):
		"""
		Draw the tokens on the plot.

		:param tokens: The text tokens to draw.
					   The method expects a list of tokens.
		:type tokens: list of str
		:param word_spacing: The space between words.
		:type word_spacing: float
		"""

		axis = self.drawable.axis
		figure = self.drawable.figure

		axis.set_ylim(0, 0)
		self.drawable.figure.set_figheight(1)

		"""
		Go through each token and draw it on the axis.
		"""
		offset = 0
		for token in tokens:
			text = axis.text(offset, 0, token)
			bb = util.get_bb(figure, axis, text)
			offset += bb.width + word_spacing
