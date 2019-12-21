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
		line_tokens = []
		for token in tokens:
			"""
			If the token is a punctuation mark, do not add wordspacing to it.
			"""
			if token in punctuation:
				offset -= wordspacing * 1.5

			text = self._draw_token(token, offset, lines, linespacing)
			line_tokens.append(text)
			bb = util.get_bb(figure, axis, text)

			"""
			If the token exceeds the x-limit, break line.
			The offset is reset to the left, and a new line is added.
			The token is moved to this new line.
			Lines do not break on certain types of punctuation.
			"""
			if bb.x1 > x_lim and token not in punctuation:
				self._organize_tokens(line_tokens, lines, linespacing)
				offset, lines = 0, lines + 1
				line_tokens = []

			offset += bb.width + wordspacing

		"""
		Re-draw the axis and the figure dimensions.
		The axis and the figure are made to fit the text tightly.
		"""
		axis.set_ylim(-linespacing, lines * linespacing + 0.1)
		axis.invert_yaxis()
		self.drawable.figure.set_figheight(max(1, lines * linespacing))

	def _draw_token(self, token, offset, line, linespacing, *args, **kwargs):
		"""
		Draw the token on the plot.

		:param token: The text token to draw.
		:type token: str
		:param offset: The token's offset.
		:type offset: float
		:param line: The line number of the token.
		:type line: int
		:param linespacing: The space between lines.
		:type linespacing: float

		:return: The drawn text box.
		:rtype: :class:`matplotlib.text.Text`
		"""

		axis = self.drawable.axis
		text = axis.text(offset, line * linespacing, token, *args, **kwargs)
		return text

	def _organize_tokens(self, tokens, line, linespacing,
						 *args, **kwargs):
		"""
		Organize the line tokens.
		This function is used when the line overflows.

		:param tokens: The list of tokens added to the line
		:type tokens: list of str
		:param line: The line number of the tokens.
		:type line: int
		:param linespacing: The space between lines.
		:type linespacing: float
		"""

		tokens[-1].set_position((0, (line + 1) * linespacing))
