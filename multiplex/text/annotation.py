"""
The :class:`text.annotation.TextAnnotation` class is mainly concerned with organizing text.
You can do just about anything with these visualizations, including—unsurprisingly enough—annotating the text.

To get started with a :class:`text.annotation.TextAnnotation` visualization, create an instance of it and call the :meth:`text.annotation.TextAnnotation.draw` method.
This method expects, at the very least, a `list` of text tokens.
Alternatively, you can provide a `list` of `dict` of tokens containing at least a `text` attribute and any of the other keys:

.. code-block:: python

	{
	  'label': None,
	  'style': { 'facecolor': 'None' },
	  'text': 'token',
	}

Instructions on how the text should be formatted can be passed on to the :meth:`text.annotation.TextAnnotation.draw` method.
Among others, these attributes include alignment and the line height.
The text can also be styled by passing on any attributes supported by the :class:`matplotlib.text.Text` class.
The same attributes can be passed on to the `style` key in the code block above.
You can find examples to help you get started `here <https://github.com/NicholasMamo/multiplex-plot/blob/master/examples/2.%20Text.ipynb>`_.
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

	def draw(self, data, wordspacing=0.005, lineheight=1.25,
			 align='left', *args, **kwargs):
		"""
		Draw the text annotation visualization.
		The method receives text as a list of tokens and draws them as text.

		The text can be provided either as strings or as dictionaries.
		If strings are provided, the function converts them into dictionaries.
		Dictionaries should have the following format:

		.. code-block:: python

			{
			  'label': None,
			  'style': { 'facecolor': 'None' },
			  'text': 'token',
			}

		Of these keys, only `text` is required.
		The correct styling options are those accepted by the :class:`matplotlib.text.Text` class.
		Anything not given uses default values.

		Any other styling options, common to all tokens, should be provided as keyword arguments.

		:param data: The text data.
					 The visualization expects a `list` of tokens, or a `list` of `dict` instances as shown above.
		:type data: list of str or list of dict
		:param wordspacing: The space between words.
		:type wordspacing: float
		:param lineheight: The space between lines.
		:type lineheight: float
		:param align: The text's alignment.
					  Possible values:

					    - left
					    - right
					    - justify
		:type align: str
		"""

		axis = self.drawable.axis
		axis.axis('off')

		"""
		If text tokens are provided, convert them into a dictionary.
		"""
		for i, token in enumerate(data):
			if type(token) is str:
				data[i] = { 'text': token }

		self._draw_tokens(data, wordspacing, lineheight, align, *args, **kwargs)

	def _draw_tokens(self, tokens, wordspacing, lineheight,
					 align, *args, **kwargs):
		"""
		Draw the tokens on the plot.

		:param tokens: The text tokens to draw.
					   The method expects a `list` of tokens, each one a `dict`.
		:type tokens: list of str
		:param wordspacing: The space between words.
		:type wordspacing: float
		:param lineheight: The space between lines.
		:type lineheight: float
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
		drawn_lines = []
		linespacing = self._get_linespacing(*args, **kwargs) * lineheight
		offset, lines = 0, 0
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
			if bb.x1 > x_lim and token.get('text') not in punctuation:
				self._newline(line_tokens.pop(-1), lines, linespacing)
				self._align(line_tokens, lines, wordspacing, linespacing, align)
				offset, lines = 0, lines + 1
				drawn_lines.append((line_labels, line_tokens))
				line_tokens, line_labels = [ text ], []

			"""
			If the token has a label associated with it, draw it on the first instance.
			The labels are ordered left-to-right according to when they appeared.
			"""
			if 'label' in token and token.get('label') not in labels:
				labels.append(token.get('label'))
				label = self._draw_token(
					token.get('label'), token.get('style', {}), 0, lines,
					wordspacing, linespacing, va='top', *args, **kwargs
				)
				line_labels.append(label)
				self._align(line_labels, lines, wordspacing * 2, linespacing, align='right', x_lim=- wordspacing * 8)

			offset += bb.width + wordspacing

		"""
		Align the last line.
		"""
		drawn_lines.append((line_labels, line_tokens))
		if align != 'justify':
			self._align(line_tokens, lines, wordspacing, linespacing, align)

		"""
		Move the plot so that it starts from x-coordinate 0.
		Then, re-draw the axis and the figure dimensions.
		The axis and the figure are made to fit the text tightly.
		"""
		self._move_plot(drawn_lines)
		axis.set_ylim(- linespacing, lines * linespacing)
		axis.invert_yaxis()
		self.drawable.figure.set_figheight(lines * lineheight / 2)

	def _get_linespacing(self, *args, **kwargs):
		"""
		Calculate the line spacing.
		The line spacing is calculated by creating a token and getting its height.
		The token is immediately removed.
		The token's styling have to be provided as keyword arguments.

		:return: The line spacing.
		:rtype: float
		"""

		axis = self.drawable.axis
		figure = self.drawable.figure

		"""
		Draw a dummy token and get its height.
		Then, remove that token.
		"""
		token = self._draw_token('None', {}, 0, 0, 0, 0, *args, **kwargs)
		bb = util.get_bb(figure, axis, token)
		height = bb.height
		token.remove()
		return height

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
					    - right
					    - justify
		:type align: str
		:param x_lim: The x-limit relative to which to align the tokens.
					  If it is not given, the axis' x-limit is used instead.
		:type x_lim: float
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis

		punctuation = [ ',', '.', '?', '!', '\'', '"', ')' ]
		x_lim = axis.get_xlim()[1] if x_lim is None else x_lim

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
			space = space + x_lim - last.x1
			space = space / (len(text_tokens) - 1)

			wordspacing_px = (axis.transData.transform((space, 0))[0] -
							  axis.transData.transform((0, 0))[0])

			"""
			Re-position the tokens.
			"""
			offset = 0
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
					token.set_position((x_lim - offset, bb.y1))

					"""
					Do not add to the offset if the token is a punctuation mark.
					"""
					if token.get_text() not in punctuation:
						offset += wordspacing

	def _move_plot(self, drawn_lines):
		"""
		Move the plot so that it starts from x-coordinate 0.
		This offsets the legend labels so that they start at 0.

		:param drawn_lines: A list of drawn lines.
						   The function expects lines to be tuples of legend labels and tokens.
		:type drawn_lines: list of float
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis

		"""
		Calculate the necessary offset.
		"""
		offset = 0
		for (labels, tokens) in drawn_lines:
			for label in labels:
				bb = util.get_bb(figure, axis, label)
				offset = min(offset, bb.x0)

		"""
		Move all tokens by this offset.
		"""
		for (labels, tokens) in drawn_lines:
			tokens = labels + tokens
			for token in tokens:
				bb = util.get_bb(figure, axis, token)
				token.set_position((bb.x0 - offset, bb.y0))
