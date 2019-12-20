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

		self._draw_tokens(data, *args, **kwargs)

	def _draw_tokens(self, tokens, wordspacing=0.005, linespacing=0.6, *args, **kwargs):
		"""
		Draw the tokens on the plot.

		:param tokens: The text tokens to draw.
					   The method expects a list of tokens.
		:type tokens: list of str
		:param wordspacing: The space between words.
		:type wordspacing: float
		:param linespacing: The space between lines.
		:type linespacing: float
		"""

		axis = self.drawable.axis
		figure = self.drawable.figure

		punctuation = [ ',', '.', '?', '!', '\'', '"', ')' ]
		x_lim = axis.get_xlim()[1]

		"""
		Go through each token and draw it on the axis.
		"""
		offset, lines = 0, 0
		for token in tokens:
			"""
			If the token is a punctuation mark, do not add wordspacing to it.
			"""
			if token in punctuation:
				offset -= wordspacing * 1.5

			text = axis.text(offset, lines * linespacing, token)
			bb = util.get_bb(figure, axis, text)

			"""
			If the token exceeds the x-limit, break line.
			The offset is reset to the left, and a new line is added.
			The token is moved to this new line.
			Lines do not break on certain types of punctuation.
			"""
			if bb.x1 > x_lim and token not in punctuation:
				offset = 0
				lines += 1
				text.set_position((offset, lines * linespacing))

			offset += bb.width + wordspacing

		"""
		Re-draw the axis and the figure dimensions.
		The axis and the figure are made to fit the text tightly.
		"""
		axis.set_ylim(-linespacing, lines * linespacing + 0.1)
		axis.invert_yaxis()
		self.drawable.figure.set_figheight(lines * linespacing)
