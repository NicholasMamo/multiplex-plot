"""
The :class:`text.annotation.Annotation` class is used to draw text on visualizations.
In and of itself, it is not a visualization type.
To create text-only visualizations, use the :class:`text.text.TextAnnotation` class.
"""

import os
import sys
import re

sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
import util

class Annotation():
	"""
	An annotation is a text-only description that is added to visualizations.
	Therefore it is not a visualization in and of itself.
	Text-only visualizations can be created using the :class:`text.text.TextAnnotation` class.

	:ivar drawable: The :class:`drawable.Drawable` where the time series visualization will be drawn.
	:vartype drawable: :class:`drawable.Drawable`
	"""

	def __init__(self, drawable):
		"""
		Initialize the text annotation with the figure and axis.
		The figure is used to get the renderer.
		The visualization is drawn on the given axis.

		:param drawable: The :class:`drawable.Drawable` where the text visualization will be drawn.
		:type drawable: :class:`drawable.Drawable`
		"""

		self.drawable = drawable

	def draw(self, annotation, x, y, wordspacing=0.005, lineheight=1.25,
			 align='left', *args, **kwargs):
		"""
		Draw the text annotation visualization.
		The method receives text as a list of tokens and draws them as text.

		The text can be provided either as strings or as dictionaries.
		If strings are provided, the function converts them into dictionaries.
		Dictionaries should have the following format:

		.. code-block:: python

			{
			  'style': { 'facecolor': 'None' },
			  'text': 'token',
			}

		Of these keys, only `text` is required.
		The correct styling options are those accepted by the :class:`matplotlib.text.Text` class.
		Anything not given uses default values.

		Any other styling options, common to all tokens, should be provided as keyword arguments.

		:param annotation: The text data.
						   The visualization expects a string, a `list` of tokens, or a `list` of `dict` instances as shown above.
		:type annotation: str or list of str or list of dict
		:param x: The x-position of the annotation.
				  The function expects either a float or a tuple.
				  If a float is given, it is taken to be the start x-position of the annotation.
				  The end x-position is taken from the axis limit.
				  If a tuple is given, the first two values are the start and end x-position of the annotation.
		:type x: float or tuple
		:param y: The starting y-position of the annotation.
		:type y: float
		:param wordspacing: The space between words.
		:type wordspacing: float
		:param lineheight: The space between lines.
		:type lineheight: float
		:param align: The text's alignment.
					  Possible values:

					    - left
					    - center
					    - right
					    - justify
					    - justify-start (or justify-left)
					    - justify-center
					    - justify-end or (justify-right)
		:type align: str

		:return: The drawn annotation's lines.
				 The second list in each tuple is the list of actual tokens.
		:rtype: list of :class:`matplotlib.text.Text`
		"""

		if type(x) is float:
			x = (x, self.drawable.axis.get_xlim()[1])

		if type(annotation) is str:
			tokens = annotation.split()
		else:
			tokens = annotation

		"""
		If text tokens are provided, convert them into a dictionary.
		"""
		for i, token in enumerate(tokens):
			if type(token) is str:
				tokens[i] = { 'text': token }

		return self._draw_tokens(tokens, x, y, wordspacing, lineheight, align, *args, **kwargs)

	def _draw_tokens(self, tokens, x, y, wordspacing, lineheight, align, *args, **kwargs):
		"""
		Draw the tokens on the plot.

		:param tokens: The text tokens to draw.
					   The method expects a `list` of tokens, each one a `dict`.
		:type tokens: list of str
		:param x: The start and end x-position of the annotation.
		:type x: tuple
		:param y: The starting y-position of the annotation.
		:type y: float
		:param wordspacing: The space between words.
		:type wordspacing: float
		:param lineheight: The space between lines.
		:type lineheight: float
		:param align: The text's alignment.
					  Possible values:

					    - left
					    - center
					    - right
					    - justify
					    - justify-start (or justify-left)
					    - justify-center
					    - justify-end or (justify-right)
		:type align: str

		:return: The drawn lines.
				 Each line is made up of the text tokens.
		:rtype: list of list of :class:`matplotlib.text.Text`
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis

		punctuation = [ ',', '.', '?', '!', '\'', '"', ')' ]

		"""
		Go through each token and draw it on the axis.
		"""
		drawn_lines = []
		linespacing = util.get_linespacing(figure, axis, wordspacing, *args, **kwargs) * lineheight
		offset, lines = x[0], 0
		line_tokens, labels, line_labels = [], [], []
		for token in tokens:
			"""
			If the token is a punctuation mark, do not add wordspacing to it.
			"""
			if token.get('text') in punctuation:
				offset -= wordspacing * 1.5

			"""
			Draw the text token.
			"""
			text = self._draw_token(
				token.get('text'), token.get('style', {}), offset, lines,
				wordspacing, linespacing, va='top', *args, **kwargs
			)
			line_tokens.append(text)

			"""
			If the token exceeds the x-limit, break line.
			The offset is reset to the left, and a new line is added.
			The token is moved to this new line.
			Lines do not break on certain types of punctuation.
			"""
			bb = util.get_bb(figure, axis, text)
			if bb.x1 > x[1] and token.get('text') not in punctuation:
				self._newline(line_tokens.pop(-1), lines, linespacing, x[0])
				self._align(
					line_tokens, lines, wordspacing, linespacing,
					self._get_alignment(align), x
				)
				offset, lines = x[0], lines + 1
				drawn_lines.append((line_labels, line_tokens))
				line_tokens, line_labels = [ text ], []

			offset += bb.width + wordspacing

		"""
		Align the last line.
		"""
		drawn_lines.append((line_labels, line_tokens))
		self._align(
			line_tokens, lines, wordspacing, linespacing,
			self._get_alignment(align, last=True), x
		)

		return drawn_lines

	def _draw_token(self, text, style, offset, line, wordspacing, linespacing, *args, **kwargs):
		"""
		Draw the token on the plot.

		:param text: The text token to draw.
		:type text: str
		:param style: The style information for the token.
		:type style: dict
		:param offset: The token's offset.
		:type offset: float
		:param line: The line number of the token.
		:type line: int
		:param wordspacing: The space between words.
		:type wordspacing: float
		:param linespacing: The space between lines.
		:type linespacing: float

		:return: The drawn text box.
		:rtype: :class:`matplotlib.text.Text`
		"""

		axis = self.drawable.axis

		kwargs.update(style)
		"""
		Some styling are set specifically for the bbox.
		"""
		bbox_kwargs = { 'facecolor': 'None', 'edgecolor': 'None' }
		for arg in bbox_kwargs:
			if arg in kwargs:
				bbox_kwargs[arg] = kwargs.get(arg)
				del kwargs[arg]

		"""
		The bbox's padding is calculated in pixels.
		Therefore it is transformed from the provided axis coordinates to pixels.
		"""
		wordspacing_px = (axis.transData.transform((wordspacing, 0))[0] -
						  axis.transData.transform((0, 0))[0])
		text = axis.text(offset, line * linespacing, text,
						 bbox=dict(pad=wordspacing_px / 2., **bbox_kwargs),
						 *args, **kwargs)
		return text

	def _newline(self, token, line, linespacing, line_start):
		"""
		Create a new line with the given token.

		:param token: The text token to move to the next line.
		:type token: :class:`matplotlib.text.Text`
		:param line: The new line number of the token.
		:type line: int
		:param linespacing: The space between lines.
		:type linespacing: float
		:param line_start: The x-coordinate where the line starts.
		:type line_start: float
		"""

		token.set_position((line_start, (line + 1) * linespacing))

	def _get_alignment(self, align, last=False):
		"""
		Get the proper alignment value for the current line.

		:param align: The provided alignment value.
		:type align: str
		:param last: A boolean indicating whether this is the last line.
					 If it is the last line, alignments like `justify-left` transform into `left`.
					 Otherwise, `justify` is returned.
		:type last: bool

		:return: The alignment value for the current line.
		:rtype: str
		"""

		align = align.lower()
		map = { 'start': 'left', 'end': 'right' }

		alignment = re.findall('(justify)?-?(.+?)$', align)[0]
		if last:
			return 'left' if alignment[1] == 'justify' else map.get(alignment[1], alignment[1])
		else:
			return alignment[0] if alignment[0] else alignment[1]

	def _align(self, tokens, line, wordspacing, linespacing, align='left',
			   x_lim=None, *args, **kwargs):
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
					    - center
					    - right
					    - justify
					    - justify-start (or justify-left)
					    - justify-center
					    - justify-end or (justify-right)
		:type align: str
		:param x_lim: The x-limit relative to which to align the tokens.
					  If it is not given, the axis' x-limit is used instead.
					  The x-limit is a tuple limiting the start and end.
		:type x_lim: tuple

		:raises: ValueError
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis

		punctuation = [ ',', '.', '?', '!', '\'', '"', ')' ]
		x_lim = axis.get_xlim() if x_lim is None else x_lim

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
			space = space + x_lim[1] - last.x1
			space = space / (len(text_tokens) - 1)

			wordspacing_px = (axis.transData.transform((space, 0))[0] -
							  axis.transData.transform((0, 0))[0])

			"""
			Re-position the tokens.
			"""
			offset = x_lim[0]
			for token in tokens:
				if token.get_text() in punctuation:
					token.set_position((offset - space * 1.25, line * linespacing))
				else:
					token.set_position((offset, line * linespacing))
					bb = token.get_bbox_patch()
					token.set_bbox(dict(
						facecolor=bb.get_facecolor(), edgecolor=bb.get_edgecolor(),
						pad=wordspacing_px / 2.))
					bb = util.get_bb(figure, axis, token)
					offset += bb.width + space
		elif align == 'right':
			if len(tokens):
				"""
				Start moving the tokens to the back of the line in reverse.
				"""

				offset = 0
				for token in tokens[::-1]:
					bb = util.get_bb(figure, axis, token)
					offset += bb.width
					token.set_position((x_lim[1] - offset, bb.y1))

					"""
					Do not add to the offset if the token is a punctuation mark.
					"""
					if token.get_text() not in punctuation:
						offset += wordspacing
		elif align == 'center':
			if len(tokens):
				"""
				Calculate the space that is left in the line.
				Then, halve it and move all tokens by that value.
				"""

				bb = util.get_bb(figure, axis, tokens[-1])
				offset = (x_lim[1] - bb.x1)/2.

				for token in tokens:
					bb = util.get_bb(figure, axis, token)
					token.set_position((bb.x0 + offset, bb.y1))
		else:
			raise ValueError("Unsupported alignment %s" % align)
