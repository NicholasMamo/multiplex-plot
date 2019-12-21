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

	def _draw_tokens(self, tokens, wordspacing=0.005, linespacing=0.6,
					 align='left', *args, **kwargs):
		"""
		Draw the tokens on the plot.

		:param tokens: The text tokens to draw.
					   The method expects a list of tokens.
		:type tokens: list of str
		:param wordspacing: The space between words.
		:type wordspacing: float
		:param linespacing: The space between lines.
		:type linespacing: float
		:param align: The text's alignment.
					  Possible values:
					  	- left
						- right
						- justify
		:type align: str
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
				self._newline(line_tokens.pop(-1), lines, linespacing)
				self._organize_tokens(line_tokens, lines, wordspacing, linespacing, align)
				offset, lines = 0, lines + 1
				line_tokens = [ text ]

			offset += bb.width + wordspacing

		"""
		Re-draw the axis and the figure dimensions.
		The axis and the figure are made to fit the text tightly.
		"""
		if align != 'justify':
			self._organize_tokens(line_tokens, lines, wordspacing, linespacing, align)
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

	def _newline(self, token, line, linespacing):
		"""
		Create a new line with the given token.

		:param token: The text token to move to the next line.
		:type token: :class:`matplotlib.text.Text`
		:param line: The new line number of the token.
		:type line: int
		:param linespacing: The space between lines.
		:type linespacing: float
		"""

		token.set_position((0, (line + 1) * linespacing))

	def _organize_tokens(self, tokens, line, wordspacing, linespacing, align='left',
						 *args, **kwargs):
		"""
		Organize the line tokens.
		This function is used when the line overflows.

		:param tokens: The list of tokens added to the line.
		:type tokens: list of :class:`matplotlib.text.Text`
		:param line: The line number of the tokens.
		:type line: int
		:param wordspacing: The space between words.
		:type wordspacing: float
		:param linespacing: The space between lines.
		:type linespacing: float
		:param align: The text's alignment.
					  Possible values:
					  	- left
						- right
						- justify
		:type align: str
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis

		x_lim = axis.get_xlim()[1]

		"""
		If the text is left-aligned or justify, move the last token to the next line.

		Otherwise, if the text is right-aligned, move the last token to the next line.
		Then align all the tokens in the last line to the right.
		"""
		if align == 'left':
			pass
		elif align == 'justify':
			"""
			If the alignment is justified, add space between text tokens to fill the line.
			"""
			punctuation = [ ',', '.', '?', '!', '\'', '"', ')' ]
			text_tokens = [ token for token in tokens if token.get_text() not in punctuation ]

			"""
			Calculate the total space between tokens.

			Use this space to calculate the total projected space after justification.
			The process therefore first calculates the space between tokens.
			Then, it calculates the empty space to fill the line.
			"""
			space = 0
			for i in range(len(text_tokens) - 1):
				space += (util.get_bb(figure, axis, text_tokens[i + 1]).x0 -
						  util.get_bb(figure, axis, text_tokens[i]).x1)

			last = util.get_bb(figure, axis, tokens[-1])
			space = space + x_lim - last.x1
			space = space / (len(text_tokens) - 1)

			"""
			Re-position the tokens.
			"""
			offset = 0
			for token in tokens:
				if token.get_text() in punctuation:
					token.set_position((offset - space * 1.25, line * linespacing))
				else:
					token.set_position((offset, line * linespacing))
					bb = util.get_bb(figure, axis, token)
					offset += bb.width + space

		elif align == 'right':
			if len(tokens):
				"""
				Offset each token in the line to move it to the end of the line.
				"""
				last = tokens[-1]
				offset = x_lim - util.get_bb(figure, axis, last).x1

				for token in tokens:
					bb = util.get_bb(figure, axis, token)
					token.set_position((bb.x0 + offset, line * linespacing))
